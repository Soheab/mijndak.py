from __future__ import annotations

from typing import TYPE_CHECKING, Final

from .._types import DataSharingConsentPayload
from ..models import (
    AccountStatus,
    ActionResult,
    ConfigurationResponse,
    CurrentHousingResponse,
    DocumentsResponse,
    HouseholdResponse,
    MutationResult,
    OpenPayment,
    PaymentsResponse,
    PersonalDetails,
    PersonUpdateResult,
    PointsLinesResponse,
    PointsResponse,
    PrioritySchemes,
    SubscriptionsResponse,
    WishesResponse,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from .._types import CurrentHousingPayload, PersonPayload, PrioritySetPayload, SubscriptionPayload
    from ..http import HTTPClient
    from ..models import PointsDashboard, PointsTab, Subscription
    from ._client import Client

#: ``RelatieRolSoortCodeId`` the site sent for the main applicant (*hoofdaanvrager*).
MAIN_APPLICANT_ROLE_ID: Final = 4


class AccountClient:
    """Methods for the account's profile (*profiel*).

    This covers points, housing wishes, personal details, household, documents and payments. Use it
    through :attr:`Client.account` instead of creating it directly. Every method requires the client to
    be logged in and raises :class:`~mijndak.errors.NotLoggedInError` otherwise.

    Parameters
    ----------
    parent: :class:`Client`
        The client this belongs to.
    """

    def __init__(self, parent: Client, /) -> None:
        self._parent: Client = parent
        self.__http: HTTPClient = parent.http

    async def points(self) -> list[PointsDashboard]:
        """The account's points for each registration.

        Returns
        -------
        list[:class:`PointsDashboard`]
            The total, waiting (*wacht*), search (*zoek*), situation (*situatie*) and starter
            (*start*) points for each registration.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return PointsResponse(await self.__http.get_points(), self.__http).registrations

    async def points_lines(self) -> list[PointsTab]:
        """A line-by-line breakdown of the account's points for each registration.

        Returns
        -------
        list[:class:`PointsTab`]
            Each registration with the events that added or removed points.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return PointsLinesResponse(await self.__http.get_points_lines(), self.__http).registrations

    async def housing_wishes(self) -> WishesResponse:
        """The account's housing wishes (*woonwensen*) and the options to choose from.

        Returns
        -------
        :class:`WishesResponse`
            The wishes, plus the available towns, districts, housing types and accessibility options.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return WishesResponse(await self.__http.get_housing_wishes(), self.__http)

    async def personal_details(self) -> PersonalDetails:
        """The personal details of the account's main applicant.

        Returns
        -------
        :class:`PersonalDetails`
            Their name, address, contact details and income.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return PersonalDetails(await self.__http.get_personal_details(), self.__http)

    async def configuration(self) -> ConfigurationResponse:
        """The registration settings of this region.

        Returns
        -------
        :class:`ConfigurationResponse`
            The registration and renewal fees, the minimum age, and whether mid-rent housing is offered.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return ConfigurationResponse(await self.__http.get_configuration(), self.__http)

    async def has_priority_schemes(self) -> bool:
        """Whether the account has an active priority scheme.

        Returns
        -------
        :class:`bool`
            :data:`True` if the account has an urgency, indication, binding or group.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return (await self.__http.get_has_priority_schemes()).get("HeeftVoorrangsregelingen", False)

    async def household(self) -> HouseholdResponse:
        """The account's household (*huishouden en inkomen*).

        Returns
        -------
        :class:`HouseholdResponse`
            The household members, their incomes and the combined household income.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return HouseholdResponse(await self.__http.get_household(), self.__http)

    async def current_housing(self) -> CurrentHousingResponse:
        """The account's current housing situation (*huidige woonsituatie*).

        Returns
        -------
        :class:`CurrentHousingResponse`
            The landlord, type of home, number of rooms, type of contract and rent.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return CurrentHousingResponse(await self.__http.get_current_housing(), self.__http)

    async def priority_schemes(self) -> PrioritySchemes:
        """The account's priority schemes (*voorrangsregelingen*).

        Returns
        -------
        :class:`PrioritySchemes`
            Urgencies, indications, bindings and groups, each with the period it is valid for.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return PrioritySchemes(await self.__http.get_priority_schemes(), self.__http)

    async def status(self) -> AccountStatus:
        """Which sections of the account's profile are complete.

        Returns
        -------
        :class:`AccountStatus`
            Each section of the profile and whether it is complete.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return AccountStatus(await self.__http.get_account_status(), self.__http)

    async def open_payment(self) -> OpenPayment:
        """Whether the account has a payment due, such as a registration or renewal fee.

        Returns
        -------
        :class:`OpenPayment`
            Whether a payment is due or being processed, and the amount.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return OpenPayment(await self.__http.get_open_payment(), self.__http)

    async def payments(self) -> PaymentsResponse:
        """The account's payment information (*betaalinformatie*).

        Returns
        -------
        :class:`PaymentsResponse`
            The payment method, the date of the next invoice and the payment history.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return PaymentsResponse(await self.__http.get_payments(), self.__http)

    async def documents(self) -> DocumentsResponse:
        """The documents uploaded to the account.

        Returns
        -------
        :class:`DocumentsResponse`
            The documents for each household member and document type, and the household itself.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return DocumentsResponse(await self.__http.get_documents(), self.__http)

    async def subscriptions(self) -> list[Subscription]:
        """The account's categories of personal messages (*persoonlijke berichten*).

        Returns
        -------
        list[:class:`Subscription`]
            Each category and whether its messages are also sent by e-mail.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return SubscriptionsResponse(await self.__http.get_subscriptions(), self.__http).subscriptions

    async def update_personal_details(self, changes: PersonPayload) -> PersonUpdateResult:
        """Change the personal details of the account's main applicant.

        This fetches the current details first and applies ``changes`` on top of them. Nested records
        (``Woonadres``, ``Contactgegevens``, ``Inkomen`` and ``InkomenVSH``) are merged as well, so
        ``{"Contactgegevens": {"Telefoonnummer": "+31..."}}`` changes only the phone number.

        Parameters
        ----------
        changes: :class:`PersonPayload`
            The fields to change, using their names in the API.

        Returns
        -------
        :class:`PersonUpdateResult`
            The saved details and any message from DAK, for example that the change must be verified again.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        current = (await self.__http.get_personal_details()).get("NatuurlijkPersoonGegevens") or {}
        person = _merge(current, changes)
        data = await self.__http.update_personal_details(person, MAIN_APPLICANT_ROLE_ID)
        return PersonUpdateResult(data, self.__http)

    async def update_household_member(self, person: PersonPayload, role_id: int) -> PersonUpdateResult:
        """Add or update a household member.

        Parameters
        ----------
        person: :class:`PersonPayload`
            All of the member's details. Set ``NatuurlijkPersoonId`` to ``"0"`` to add a new member.
        role_id: :class:`int`
            The member's role in the household: co-applicant, child or other
            adult.

        Returns
        -------
        :class:`PersonUpdateResult`
            The saved details and any message from DAK.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return PersonUpdateResult(await self.__http.update_household_member(person, role_id), self.__http)

    async def remove_household_member(self, person_id: str) -> MutationResult:
        """Remove a member from the account's household.

        Parameters
        ----------
        person_id: :class:`str`
            The member's ID.

        Returns
        -------
        :class:`MutationResult`
            Check :attr:`ActionResult.is_success` to see whether it worked.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return MutationResult(await self.__http.remove_household_member(person_id), self.__http)

    async def update_current_housing(self, changes: CurrentHousingPayload) -> MutationResult:
        """Change the account's current housing situation.

        This fetches the current situation first and applies ``changes`` on top of it, including nested
        records.

        Parameters
        ----------
        changes: :class:`CurrentHousingPayload`
            The fields to change, using their names in the API.

        Returns
        -------
        :class:`MutationResult`
            Check :attr:`ActionResult.is_success` to see whether it worked.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        response = (await self.__http.get_current_housing()).get("Response") or {}
        housing = _merge(response.get("HuidigeWoonsituatie") or {}, changes)
        return MutationResult(await self.__http.update_current_housing(housing), self.__http)

    async def set_subscription(self, code: str, subscribed: bool) -> ActionResult:
        """Turn e-mail on or off for one category of personal messages.

        Parameters
        ----------
        code: :class:`str`
            The category's :attr:`Subscription.code`.
        subscribed: :class:`bool`
            :data:`True` to also receive this category by e-mail.

        Returns
        -------
        :class:`ActionResult`
            Check :attr:`ActionResult.is_success` to see whether it worked.

        Raises
        ------
        :exc:`ValueError`
            No category has this code.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        data = await self.__http.get_subscriptions()
        container = data.get("Abonnementen")
        current: list[SubscriptionPayload] = container.get("List", []) if container else []
        match = next((item for item in current if item.get("SoortCode") == code), None)
        if match is None:
            msg = f"No subscription with code {code!r}"
            raise ValueError(msg)
        record: SubscriptionPayload = {**match, "IsGeabonneerd": subscribed}
        return ActionResult(await self.__http.set_subscription(record), self.__http)

    async def set_data_sharing(self, consents: Mapping[str, bool]) -> ActionResult:
        """Give or withdraw consent to share the account's data (*gegevensdeling*).

        Parameters
        ----------
        consents: Mapping[:class:`str`, :class:`bool`]
            Maps each consent's ID to :data:`True` to give consent or :data:`False` to withdraw
            it.

        Returns
        -------
        :class:`ActionResult`
            Check :attr:`ActionResult.is_success` to see whether it worked.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        payload = [
            DataSharingConsentPayload(ToestemmingId=key, IsToestemmingVerleend=value) for key, value in consents.items()
        ]
        return ActionResult(await self.__http.set_data_sharing(payload), self.__http)

    async def save_bindings(self, priority_set: PrioritySetPayload) -> ActionResult:
        """Save a binding (*binding*) priority set.

        Parameters
        ----------
        priority_set: :class:`PrioritySetPayload`
            The complete set as returned by :meth:`priority_schemes`, with the changes applied.

        Returns
        -------
        :class:`ActionResult`
            Check :attr:`ActionResult.is_success` to see whether it worked.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return ActionResult(await self.__http.save_bindings(priority_set), self.__http)

    async def save_groups(self, priority_set: PrioritySetPayload) -> ActionResult:
        """Save a group (*groep*) priority set.

        Parameters
        ----------
        priority_set: :class:`PrioritySetPayload`
            The complete set as returned by :meth:`priority_schemes`, with the changes applied.

        Returns
        -------
        :class:`ActionResult`
            Check :attr:`ActionResult.is_success` to see whether it worked.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return ActionResult(await self.__http.save_groups(priority_set), self.__http)

    async def save_indications(self, priority_set: PrioritySetPayload) -> ActionResult:
        """Save an indication (*indicatie*) priority set.

        Parameters
        ----------
        priority_set: :class:`PrioritySetPayload`
            The complete set as returned by :meth:`priority_schemes`, with the changes applied.

        Returns
        -------
        :class:`ActionResult`
            Check :attr:`ActionResult.is_success` to see whether it worked.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return ActionResult(await self.__http.save_indications(priority_set), self.__http)

    async def upload_document(
        self,
        person_id: str,
        document_type: str,
        filename: str,
        content: bytes,
        mime_type: str,
        *,
        title: str = "",
    ) -> ActionResult:
        """Upload a document for a member of the household.

        Parameters
        ----------
        person_id: :class:`str`
            The member's ID.
        document_type: :class:`str`
            The document type's :attr:`DocumentType.code`.
        filename: :class:`str`
            The name to save the file under.
        content: :class:`bytes`
            The file's contents.
        mime_type: :class:`str`
            The file's MIME type, such as ``"application/pdf"``.
        title: :class:`str`, optional
            The title shown in the list of documents. Defaults to ``filename``.

        Returns
        -------
        :class:`ActionResult`
            Check :attr:`ActionResult.is_success` to see whether it worked.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        data = await self.__http.upload_document(
            person_id, document_type, filename, content, mime_type=mime_type, title=title
        )
        return ActionResult(data, self.__http)

    async def delete_document(self, person_id: str, document_id: str) -> ActionResult:
        """Delete an uploaded document.

        Parameters
        ----------
        person_id: :class:`str`
            The ID of the member the document belongs to.
        document_id: :class:`str`
            The document's ID (:attr:`Document.id`).

        Returns
        -------
        :class:`ActionResult`
            Check :attr:`ActionResult.is_success` to see whether it worked.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return ActionResult(await self.__http.delete_document(person_id, document_id), self.__http)


def _merge[T: Mapping[str, object]](current: Mapping[str, object], changes: T) -> T:
    """``current`` updated with ``changes``, merging nested records one level deep."""
    merged = dict(current)
    for key, value in changes.items():
        existing = merged.get(key)
        if isinstance(existing, dict) and isinstance(value, dict):
            merged[key] = {**existing, **value}
        else:
            merged[key] = value
    return merged  # pyright: ignore[reportReturnType]
