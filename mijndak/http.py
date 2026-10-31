from __future__ import annotations

import asyncio
import base64
import re
import time
from collections.abc import Callable
from email.utils import parsedate_to_datetime
from http.cookies import SimpleCookie
from typing import TYPE_CHECKING, Final, TypedDict, override
from urllib.parse import unquote

import aiohttp
import msgspec
from yarl import URL

from ._types import (
    ActionInputs,
    ChangePasswordInputs,
    ClientVariables,
    DataActionPayload,
    DeleteDocumentInputs,
    DisplayPreferencesInputs,
    HideInputs,
    LoginInputs,
    LogoutInputs,
    OfferDisplayInputs,
    PointsCounterInputs,
    PublicationInputs,
    ReactInputs,
    RemovePersonInputs,
    SaveBindingsInputs,
    SaveGroupsInputs,
    SaveIndicationsInputs,
    SaveInputs,
    ServerActionPayload,
    SetDataSharingInputs,
    SetSubscriptionInputs,
    UpdateCurrentHousingInputs,
    UpdatePersonInputs,
    UploadDocumentInputs,
    VersionInfoPayload,
    WishesFilterInputs,
)
from ._types.envelope.response import Envelope, ModuleInfo
from ._types.listings.details import ListingDetailPayload
from .endpoints import Account, Auth, ListingDetails, Listings, Profile, Reactions, Settings
from .errors import EndpointNotFoundError, HTTPError, NotLoggedInError, ServerError, VersionChangedError

if TYPE_CHECKING:
    from types import TracebackType

    from ._types import (
        AccountStatusPayload,
        ActionResultPayload,
        AggregatePayload,
        ApplicantPayload,
        ChangePasswordPayload,
        ConfigurationResponsePayload,
        CurrentHousingPayload,
        CurrentHousingResponsePayload,
        DataSharingConsentPayload,
        DataSharingPayload,
        DisplayPreferencesResponsePayload,
        DocumentsPayload,
        EligibilityPayload,
        EnrolmentInformationPayload,
        FileItemPayload,
        HouseholdResponsePayload,
        HousingCostsResponsePayload,
        ListingExtrasPayload,
        ListingsPayload,
        MFADetailsPayload,
        MutationResultPayload,
        OpenPaymentPayload,
        PaymentsPayload,
        PersonalDetailsPayload,
        PersonPayload,
        PersonResultPayload,
        PointsLinesPayload,
        PointsPayload,
        PriorityFlagPayload,
        PrioritySchemesPayload,
        PrioritySetPayload,
        ReactionsPayload,
        RegistrationItemPayload,
        SavedAndHiddenPayload,
        SubscriptionPayload,
        SubscriptionsPayload,
        UserItemPayload,
        WishesPayload,
    )
    from .endpoints import DataAction, ServerAction


__all__ = ("HTTPClient", "SessionCookie", "SessionCookieData")

type _PayloadBuilder = Callable[[VersionInfoPayload], DataActionPayload | ServerActionPayload]


#: Public, well-known token OutSystems uses for anonymous requests before a session cookie exists.
ANONYMOUS_CSRF_TOKEN: Final = "T6C+9iB49TLra4jEsMeSckDMNhQ="
_CRF_RE: Final = re.compile(r"crf=([^;]+)")
_HASH_RE: Final = re.compile(r'"(screenservices/[^"]+)", "([^"]+)"')
_NOT_LOGGED_IN_MARKERS: Final = ("NotRegistered", "No role validation", "geen inschrijving")

USER_AGENT: Final = "mijndak.py (+https://github.com/Soheab/mijndak.py)"


class SessionCookieData(TypedDict):
    name: str
    value: str
    domain: str
    path: str
    expires_at: float | None
    secure: bool
    http_only: bool


class SessionCookie:
    """Sensitive session state. Encrypt before storing; never expose it to browsers or logs."""

    __slots__ = ("domain", "expires_at", "http_only", "name", "path", "secure", "value")

    def __init__(
        self,
        name: str,
        value: str,
        domain: str,
        path: str = "/",
        expires_at: float | None = None,
        *,
        secure: bool = True,
        http_only: bool = True,
    ) -> None:
        self.name = name
        self.value = value
        self.domain = domain
        self.path = path
        self.expires_at = expires_at
        self.secure = secure
        self.http_only = http_only

    @override
    def __repr__(self) -> str:
        return f"SessionCookie(name={self.name!r}, value=<redacted>)"

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, SessionCookie) and other.to_dict() == self.to_dict()

    @override
    def __hash__(self) -> int:
        return hash((self.name, self.domain, self.path, self.value))

    def to_dict(self) -> SessionCookieData:
        """JSON-serializable form for storage."""
        return SessionCookieData(
            name=self.name,
            value=self.value,
            domain=self.domain,
            path=self.path,
            expires_at=self.expires_at,
            secure=self.secure,
            http_only=self.http_only,
        )

    @classmethod
    def from_dict(cls, data: SessionCookieData) -> SessionCookie:
        return cls(
            data["name"],
            data["value"],
            data["domain"],
            data["path"],
            data["expires_at"],
            secure=data["secure"],
            http_only=data["http_only"],
        )


class HTTPClient:
    """Async transport for one DAK region site, e.g. ``https://amsterdam.mijndak.nl``."""

    def __init__(
        self,
        base_url: str,
        client_variables: ClientVariables,
        swv_id: str,
        *,
        session: aiohttp.ClientSession | None = None,
        timeout: float = 20.0,
    ) -> None:
        self.base_url: Final = URL(base_url)
        self.client_variables: ClientVariables = client_variables
        #: ``SamenwerkingsverbandId`` of the region, sent in action inputs and screen variables.
        self.swv_id: Final = swv_id
        self._owns_session = session is None
        self._session = session or aiohttp.ClientSession(
            base_url=self.base_url,
            timeout=aiohttp.ClientTimeout(total=timeout),
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            cookie_jar=aiohttp.CookieJar(),
        )
        self._encoder: Final = msgspec.json.Encoder()
        self._module_version: str | None = None
        self._url_versions: dict[str, str] = {}
        self._hashes: dict[str, str] = {}
        self._loaded_scripts: set[str] = set()
        self._lock: Final = asyncio.Lock()
        self._cookie_deadlines: dict[tuple[str, str, str, str], float] = {}

    @property
    def session(self) -> aiohttp.ClientSession:
        return self._session

    async def close(self) -> None:
        if self._owns_session:
            await self._session.close()

    async def __aenter__(self) -> HTTPClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()

    def csrf_token(self) -> str:
        """CSRF token from the ``nr2Users`` cookie, or the anonymous token before login."""
        morsel = self._session.cookie_jar.filter_cookies(self.base_url).get("nr2Users")
        match = _CRF_RE.search(unquote(morsel.value)) if morsel else None
        return match.group(1) if match else ANONYMOUS_CSRF_TOKEN

    def is_authenticated(self) -> bool:
        return "nr1Users" in self._session.cookie_jar.filter_cookies(self.base_url)

    def export_session(self) -> list[SessionCookie]:
        """Export JSON-serializable cookies, keeping absolute expiry across restarts."""
        result: list[SessionCookie] = []
        now = time.time()
        host = self.base_url.host or ""
        for cookie in self.session.cookie_jar:
            domain = cookie["domain"].lstrip(".")
            if host != domain and not host.endswith("." + domain):
                continue
            expires_at = None
            if cookie["max-age"]:
                key = (cookie.key, domain, cookie["path"], cookie.value)
                expires_at = self._cookie_deadlines.setdefault(key, now + int(cookie["max-age"]))
            elif cookie["expires"]:
                expires_at = parsedate_to_datetime(cookie["expires"]).timestamp()
            if expires_at is not None and expires_at <= now:
                continue
            result.append(
                SessionCookie(
                    cookie.key,
                    cookie.value,
                    domain,
                    cookie["path"] or "/",
                    expires_at,
                    secure=bool(cookie["secure"]),
                    http_only=bool(cookie["httponly"]),
                )
            )
        return result

    def restore_session(self, cookies: list[SessionCookie]) -> None:
        """Restore cookies for this region only; does not prove the login is still valid."""
        self.session.cookie_jar.clear()
        self._cookie_deadlines.clear()
        host = self.base_url.host or ""
        now = time.time()
        for saved in cookies:
            domain = saved.domain.lstrip(".")
            if not domain or (host != domain and not host.endswith("." + domain)):
                raise ValueError("Session cookie belongs to another region")
            if saved.expires_at is not None and saved.expires_at <= now:
                continue
            jar: SimpleCookie = SimpleCookie()
            jar[saved.name] = saved.value
            cookie = jar[saved.name]
            cookie["domain"] = domain
            cookie["path"] = saved.path
            cookie["secure"] = saved.secure
            cookie["httponly"] = saved.http_only
            if saved.expires_at is not None:
                cookie["max-age"] = str(max(1, int(saved.expires_at - now)))
                self._cookie_deadlines[saved.name, domain, saved.path, saved.value] = saved.expires_at

            self.session.cookie_jar.update_cookies(jar, response_url=self.base_url)

    async def _get_text(self, path: str) -> str:
        # The session default ``Accept: application/json`` makes IIS answer 406 for ``.js`` files.
        async with self._session.get(path, headers={"Accept": "*/*"}) as resp:
            text = await resp.text()
            if resp.status >= 400:
                raise HTTPError(resp.status, str(resp.url), text)
            return text

    async def refresh_manifest(self) -> None:
        """(Re)load ``moduleinfo`` and drop all cached hashes."""
        info = msgspec.json.decode(await self._get_text("/moduleservices/moduleinfo"), type=ModuleInfo)
        self._module_version = info["manifest"].get("versionToken")
        self._url_versions = info["manifest"].get("urlVersions", {})
        self._hashes.clear()
        self._loaded_scripts.clear()

    @staticmethod
    def script_for(endpoint: str) -> str:
        """Map an endpoint to the script that declares it.

        ``screenservices/DAKWP/Overzicht/WoningOverzicht/DataActionX``
        → ``DAKWP.Overzicht.WoningOverzicht.mvc.js``.

        Module-level actions (``screenservices/DAKWP/ActionX``) live in ``DAKWP.controller.js``.
        """
        parts = endpoint.split("/")[1:-1]
        suffix = ".mvc.js" if len(parts) > 1 else ".controller.js"
        return ".".join(parts) + suffix

    async def _load_script(self, script: str) -> None:
        key = next((k for k in self._url_versions if k.endswith(f"/scripts/{script}")), None)
        self._loaded_scripts.add(script)
        if key is None:
            return
        text = await self._get_text(key + self._url_versions[key])
        self._hashes.update(_HASH_RE.findall(text))

    async def api_version(self, endpoint: str) -> tuple[str, str]:
        """Return ``(moduleVersion, apiVersion)`` for an endpoint, fetching its script on first use."""
        async with self._lock:
            if self._module_version is None:
                await self.refresh_manifest()
            script = self.script_for(endpoint)
            if endpoint not in self._hashes and script not in self._loaded_scripts:
                await self._load_script(script)
            module_version = self._module_version or ""
            api_version = self._hashes.get(endpoint)
        if api_version is None:
            raise EndpointNotFoundError(f"No apiVersion found for {endpoint!r} in {script}")
        return module_version, api_version

    @staticmethod
    def _decoder[T](model: type[T]) -> msgspec.json.Decoder[Envelope[T]]:
        return msgspec.json.Decoder(Envelope[model])

    async def _post(self, endpoint: str, payload: DataActionPayload | ServerActionPayload) -> bytes:
        headers = {
            "Content-Type": "application/json; charset=UTF-8",
            "X-CSRFToken": self.csrf_token(),
            "OutSystems-locale": "nl-NL",
        }
        async with self._session.post(f"/{endpoint}", data=self._encoder.encode(payload), headers=headers) as resp:
            body = await resp.read()
            if resp.status >= 400:
                raise HTTPError(resp.status, str(resp.url), body.decode(errors="replace"))
            return body

    @staticmethod
    def _unwrap[T](endpoint: str, envelope: Envelope[T]) -> T:
        exc = envelope.get("exception")
        if exc is not None:
            name, message = exc.get("name"), exc.get("message")
            error_cls = NotLoggedInError if any(m in f"{name} {message}" for m in _NOT_LOGGED_IN_MARKERS) else ServerError
            raise error_cls(name, message, exc.get("specificType"), endpoint)
        if "data" not in envelope:
            raise ServerError("EmptyResponse", "Response had neither data nor exception", None, endpoint)
        return envelope["data"]

    async def _call[T](
        self,
        endpoint: str,
        model: type[T],
        build: _PayloadBuilder,
    ) -> T:
        decoder = self._decoder(model)
        for attempt in range(2):
            module_version, api_version = await self.api_version(endpoint)
            payload = build(VersionInfoPayload(moduleVersion=module_version, apiVersion=api_version))
            envelope = decoder.decode(await self._post(endpoint, payload))
            version = envelope.get("versionInfo", {})
            stale = version.get("hasApiVersionChanged") or version.get("hasModuleVersionChanged")
            if not stale or "exception" not in envelope:
                return self._unwrap(endpoint, envelope)
            if attempt == 0:
                await self.refresh_manifest()
        raise VersionChangedError(f"{endpoint}: site was redeployed and retry failed")

    async def data_action[T](self, action: DataAction[T], *, variables: dict[str, object] | None = None) -> T:
        """Call a ``DataAction*``/``ScreenDataSet*`` endpoint.

        ``variables`` are the screen variables the server reads.
        """

        def build(version: VersionInfoPayload) -> DataActionPayload:
            payload = DataActionPayload(
                versionInfo=version,
                viewName=action.view_name,
                screenData={"variables": variables or {}},
                clientVariables=self.client_variables,
            )
            if action.page_size is not None:
                payload["inputParameters"] = {"StartIndex": 0, "MaxRecords": action.page_size}
            return payload

        return await self._call(action.path, action.payload, build)

    async def server_action[I: ActionInputs, T](self, action: ServerAction[I, T], inputs: I) -> T:
        """Call an ``Action*`` (mutating) endpoint with typed input parameters."""

        def build(version: VersionInfoPayload) -> ServerActionPayload:
            return ServerActionPayload(
                versionInfo=version,
                viewName=action.view_name,
                inputParameters=inputs,
                clientVariables=self.client_variables,
            )

        return await self._call(action.path, action.payload, build)

    async def login(self, username: str, password: str, *, remember: bool = False) -> None:
        inputs = LoginInputs(
            Gebruikersnaam=username,
            Wachtwoord=password,
            IsIngelogdBlijven=remember,
            SwvClient=self.swv_id,
            ReturnUrl="",
            ClientInputLastUrl="",
            WoningAanbodPublicatie="",
            IsVanContactformulier=False,
            IsKlantContactCode=False,
            RequestId_In="0",
            Request_In="",
        )
        await self.server_action(Auth.LOGIN, inputs)

    async def logout(self) -> None:
        await self.server_action(Auth.LOGOUT, LogoutInputs())

    async def get_public_listings(self) -> ListingsPayload:
        return await self.data_action(Listings.PUBLIC)

    async def get_matching_listings(self) -> ListingsPayload:
        return await self.data_action(Listings.MATCHING)

    async def get_non_matching_listings(self) -> ListingsPayload:
        return await self.data_action(Listings.NON_MATCHING)

    async def get_saved_and_hidden(self) -> SavedAndHiddenPayload:
        return await self.data_action(Listings.SAVED_AND_HIDDEN)

    def _publication(self, publication_id: int) -> PublicationInputs:
        return PublicationInputs(PublicatieId=str(publication_id), SamenwerkingsverbandId=self.swv_id)

    async def set_saved(self, publication_id: int, saved: bool) -> ActionResultPayload:
        inputs = SaveInputs(**self._publication(publication_id), IsBewaren=saved)
        return await self.server_action(Listings.SET_SAVED, inputs)

    async def set_hidden(self, publication_id: int, hidden: bool) -> ActionResultPayload:
        inputs = HideInputs(**self._publication(publication_id), IsVerbergen=hidden)
        return await self.server_action(Listings.SET_HIDDEN, inputs)

    def _detail_variables(self, publication_id: int, applicant_id: str = "0") -> dict[str, object]:
        """Screen variables of ``HuisDetails``; the server dereferences these records, so they must exist."""
        pid = str(publication_id)
        return {
            "PublicatieId": pid,
            "PublicatieIdLocal": pid,
            "_publicatieIdInDataFetchStatus": 1,
            "Tab": -1,
            "HaalSamenwerkingsverband": {
                "List": {"List": [{"Samenwerkingsverband": {"SamenwerkingsverbandId": self.swv_id}}]}
            },
            "GetPublicatie": {"List": {"List": []}},
            "HaalAanvrager": {"NatuurlijkPersoonId": applicant_id},
            "GetInformatieBijInschrijving": {
                "PublicatieKandidaatSorteerTekst": {"List": []},
                "PublicatieKandidaat": {},
                "WoonWensList": {"List": []},
            },
        }

    @staticmethod
    def decode_listing(record: msgspec.Raw) -> ListingDetailPayload:
        """Decode a record from :meth:`get_listing`; the raw record is what the web-block calls take."""
        return msgspec.json.decode(record, type=ListingDetailPayload)

    async def get_listing(self, publication_id: int) -> AggregatePayload[msgspec.Raw]:
        """The raw listing record; web-block calls below take it as input."""
        return await self.data_action(ListingDetails.LISTING, variables=self._detail_variables(publication_id))

    async def get_listing_photos(self, publication_id: int) -> AggregatePayload[FileItemPayload]:
        return await self.data_action(ListingDetails.PHOTOS, variables=self._detail_variables(publication_id))

    async def get_applicant(self, publication_id: int) -> ApplicantPayload:
        return await self.data_action(ListingDetails.APPLICANT, variables=self._detail_variables(publication_id))

    async def get_enrolment_information(self, publication_id: int, applicant_id: str) -> EnrolmentInformationPayload:
        return await self.data_action(
            ListingDetails.ENROLMENT_INFORMATION,
            variables=self._detail_variables(publication_id, applicant_id),
        )

    async def get_eligibility(self, publication_id: int) -> EligibilityPayload:
        return await self.data_action(
            ListingDetails.ELIGIBILITY,
            variables={
                "PublicatieId": str(publication_id),
                "_publicatieIdInDataFetchStatus": 1,
                "SamenwerkingsverbandId": self.swv_id,
                "_samenwerkingsverbandIdInDataFetchStatus": 1,
                "KanOpnieuwProberen": False,
                "LinksVervangenCordova": False,
            },
        )

    async def get_listing_extras(self, listing: msgspec.Raw) -> ListingExtrasPayload:
        return await self.data_action(ListingDetails.EXTRAS, variables={"Publicatie": listing})

    async def get_listing_downloads(self, listing: msgspec.Raw) -> AggregatePayload[FileItemPayload]:
        return await self.data_action(ListingDetails.DOWNLOADS, variables={"Publicatie": listing})

    async def get_listing_vr_floorplans(self, listing: msgspec.Raw) -> AggregatePayload[FileItemPayload]:
        return await self.data_action(ListingDetails.VR_FLOORPLANS, variables={"Publicatie": listing})

    async def get_housing_costs(self, listing: msgspec.Raw) -> HousingCostsResponsePayload:
        return await self.data_action(ListingDetails.HOUSING_COSTS, variables={"Publicatie": listing})

    async def get_current_reactions(self) -> ReactionsPayload:
        return await self.data_action(Reactions.CURRENT)

    async def get_ongoing_reactions(self) -> ReactionsPayload:
        return await self.data_action(Reactions.ONGOING)

    async def get_past_reactions(self) -> ReactionsPayload:
        return await self.data_action(Reactions.PAST)

    async def react(self, publication_id: int) -> ActionResultPayload:
        inputs = ReactInputs(**self._publication(publication_id), ToonMijNietMeer=False)
        return await self.server_action(Reactions.REACT, inputs)

    async def withdraw_reaction(self, publication_id: int) -> ActionResultPayload:
        return await self.server_action(Reactions.WITHDRAW, self._publication(publication_id))

    async def get_points(self) -> PointsPayload:
        return await self.data_action(Profile.POINTS)

    async def get_housing_wishes(self) -> WishesPayload:
        return await self.data_action(Profile.HOUSING_WISHES)

    async def get_points_lines(self) -> PointsLinesPayload:
        return await self.data_action(Account.POINTS_LINES)

    def _swv_variables(self) -> dict[str, object]:
        """Screen variables of the account web blocks, which read the region from the screen."""
        return {"SamenwerkingsverbandId": self.swv_id, "_samenwerkingsverbandIdInDataFetchStatus": 1}

    async def get_personal_details(self) -> PersonalDetailsPayload:
        return await self.data_action(Account.PERSONAL_DETAILS)

    async def get_configuration(self) -> ConfigurationResponsePayload:
        return await self.data_action(Account.CONFIGURATION)

    async def get_has_priority_schemes(self) -> PriorityFlagPayload:
        return await self.data_action(Account.HAS_PRIORITY_SCHEMES)

    async def get_household(self) -> HouseholdResponsePayload:
        return await self.data_action(Account.HOUSEHOLD)

    async def get_current_housing(self) -> CurrentHousingResponsePayload:
        return await self.data_action(Account.CURRENT_HOUSING)

    async def get_priority_schemes(self) -> PrioritySchemesPayload:
        return await self.data_action(Account.PRIORITY_SCHEMES)

    async def get_account_status(self) -> AccountStatusPayload:
        return await self.data_action(Account.STATUS)

    async def get_open_payment(self) -> OpenPaymentPayload:
        return await self.data_action(Account.OPEN_PAYMENT)

    async def get_payments(self) -> PaymentsPayload:
        return await self.data_action(Account.PAYMENTS, variables=self._swv_variables())

    async def get_documents(self) -> DocumentsPayload:
        return await self.data_action(Account.DOCUMENTS, variables=self._swv_variables())

    async def get_subscriptions(self) -> SubscriptionsPayload:
        return await self.data_action(Account.SUBSCRIPTIONS, variables=self._swv_variables())

    async def get_data_sharing(self) -> DataSharingPayload:
        return await self.data_action(Account.DATA_SHARING, variables=self._swv_variables())

    async def get_registrations(self) -> AggregatePayload[RegistrationItemPayload]:
        return await self.data_action(Settings.REGISTRATIONS)

    async def get_mfa_details(self) -> MFADetailsPayload:
        return await self.data_action(Settings.MFA)

    async def get_display_preferences(self) -> DisplayPreferencesResponsePayload:
        return await self.data_action(Settings.DISPLAY_PREFERENCES)

    async def get_user(self) -> AggregatePayload[UserItemPayload]:
        return await self.data_action(Account.USER)

    async def update_personal_details(self, person: PersonPayload, role_id: int) -> PersonResultPayload:
        inputs = UpdatePersonInputs(
            Locale="",
            NatuurlijkPersoon=person,
            RelatieRolSoortCodeId=role_id,
            SamenwerkingsverbandId=self.swv_id,
        )
        return await self.server_action(Account.UPDATE_PERSONAL_DETAILS, inputs)

    async def update_household_member(self, person: PersonPayload, role_id: int) -> PersonResultPayload:
        """Add (``NatuurlijkPersoonId`` ``"0"``) or update a household member."""
        inputs = UpdatePersonInputs(
            Locale="",
            NatuurlijkPersoon=person,
            RelatieRolSoortCodeId=role_id,
            SamenwerkingsverbandId=self.swv_id,
        )
        return await self.server_action(Account.UPDATE_HOUSEHOLD_MEMBER, inputs)

    async def remove_household_member(self, person_id: str) -> MutationResultPayload:
        inputs = RemovePersonInputs(Locale="", NatuurlijkPersoonId=person_id, SamenwerkingsverbandId=self.swv_id)
        return await self.server_action(Account.REMOVE_HOUSEHOLD_MEMBER, inputs)

    async def update_current_housing(self, housing: CurrentHousingPayload) -> MutationResultPayload:
        return await self.server_action(
            Account.UPDATE_CURRENT_HOUSING, UpdateCurrentHousingInputs(HuidigeWoonsituatie=housing)
        )

    async def set_subscription(self, subscription: SubscriptionPayload) -> ActionResultPayload:
        inputs = SetSubscriptionInputs(Locale="", Abonnement=subscription, SamenwerkingsverbandId=self.swv_id)
        return await self.server_action(Account.SET_SUBSCRIPTION, inputs)

    async def set_data_sharing(self, consents: list[DataSharingConsentPayload]) -> ActionResultPayload:
        inputs = SetDataSharingInputs(Locale="", SamenwerkingsverbandId=self.swv_id, Gegevensdeling=consents)
        return await self.server_action(Account.SET_DATA_SHARING, inputs)

    async def save_bindings(self, priority_set: PrioritySetPayload) -> ActionResultPayload:
        inputs = SaveBindingsInputs(SamenwerkingsverbandId=self.swv_id, Bindingen=priority_set)
        return await self.server_action(Account.SAVE_BINDINGS, inputs)

    async def save_groups(self, priority_set: PrioritySetPayload) -> ActionResultPayload:
        inputs = SaveGroupsInputs(SamenwerkingsverbandId=self.swv_id, Groepen=priority_set)
        return await self.server_action(Account.SAVE_GROUPS, inputs)

    async def save_indications(self, priority_set: PrioritySetPayload) -> ActionResultPayload:
        inputs = SaveIndicationsInputs(SamenwerkingsverbandId=self.swv_id, Indicaties=priority_set)
        return await self.server_action(Account.SAVE_INDICATIONS, inputs)

    async def upload_document(
        self,
        person_id: str,
        document_type: str,
        filename: str,
        content: bytes,
        *,
        mime_type: str,
        title: str = "",
    ) -> ActionResultPayload:
        inputs = UploadDocumentInputs(
            Document=base64.b64encode(content).decode(),
            SamenwerkingsverbandId=self.swv_id,
            NatuurlijkPersoonId=person_id,
            DocumentNaam=filename,
            Titel=title or filename,
            MimeType=mime_type,
            DocumentSoortCode=document_type,
        )
        return await self.server_action(Account.UPLOAD_DOCUMENT, inputs)

    async def delete_document(self, person_id: str, document_id: str) -> ActionResultPayload:
        inputs = DeleteDocumentInputs(
            Locale="",
            SamenwerkingsverbandId=self.swv_id,
            NatuurlijkpersoonId=person_id,
            DocumentId=document_id,
        )
        return await self.server_action(Account.DELETE_DOCUMENT, inputs)

    async def change_password(self, old_password: str, new_password: str) -> ChangePasswordPayload:
        inputs = ChangePasswordInputs(
            OudWachtwoord=old_password, NieuwWachtwoord=new_password, SamenwerkingsverbandId=self.swv_id
        )
        return await self.server_action(Settings.CHANGE_PASSWORD, inputs)

    async def set_display_preferences(self, *, is_dak: bool, hide_map: bool, extended_search: bool) -> ActionResultPayload:
        inputs = DisplayPreferencesInputs(IsDAK=is_dak, IsKaartVerbergen=hide_map, IsUitgebreidZoeken=extended_search)
        return await self.server_action(Settings.SET_DISPLAY_PREFERENCES, inputs)

    async def set_offer_end_date_display(self, show: bool) -> ActionResultPayload:
        return await self.server_action(Settings.SET_OFFER_END_DATE_DISPLAY, OfferDisplayInputs(IsWeergaveEinddatum=show))

    async def set_filter_by_wishes(self, enabled: bool) -> ActionResultPayload:
        return await self.server_action(Settings.SET_FILTER_BY_WISHES, WishesFilterInputs(IsWoonwensFilterByDefault=enabled))

    async def set_points_counter(self, start_on_points_overview: bool) -> ActionResultPayload:
        return await self.server_action(
            Settings.SET_POINTS_COUNTER,
            PointsCounterInputs(IsOpstartenPuntenoverzicht=start_on_points_overview),
        )
