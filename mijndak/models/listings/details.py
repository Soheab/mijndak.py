from __future__ import annotations

import base64
import binascii
from typing import TYPE_CHECKING, override

from ..actions import ActionResult, Result
from ..base import Items, Model, Nested, field, parse_datetime, parse_decimal, records

if TYPE_CHECKING:
    import datetime as dt
    from decimal import Decimal

    import msgspec

    from ...http import HTTPClient

__all__ = (
    "Applicant",
    "BaseListing",
    "Criterion",
    "DetailAddress",
    "DetailCluster",
    "DetailPublication",
    "DetailUnit",
    "EligibilityResponse",
    "EligibilityRule",
    "EnrolmentInformation",
    "Facility",
    "File",
    "FileItem",
    "HousingCosts",
    "HousingCostsResponse",
    "ListingDetail",
    "ListingExtras",
    "PartialListing",
    "PriceComponent",
    "RankingRule",
    "Room",
)


def decode_html(value: str | None) -> str | None:
    """Decode a rich-text field, which the API sends as base64-encoded HTML.

    Parameters
    ----------
    value: :class:`str` | :data:`None`
        The base64-encoded HTML.

    Returns
    -------
    :class:`str` | :data:`None`
        The HTML, ``value`` unchanged if it is not valid base64, or :data:`None` if it is empty.
    """
    if not value:
        return None
    try:
        return base64.b64decode(value).decode("utf-8")
    except (binascii.Error, UnicodeDecodeError):
        return value


class BaseListing(Model):
    """A listing that can make requests about itself, such as ``await listing.downloads()``.

    This is the base class of :class:`Listing`, :class:`ListingDetail` and :class:`PartialListing`.
    """

    @property
    def publication_id(self) -> int:
        """The listing's ID.

        Returns
        -------
        :class:`int`
            The ID.
        """
        raise NotImplementedError

    #: The exact record a :class:`ListingDetail` was decoded from; the web-block calls take it as input.
    _source: msgspec.Raw | None = None

    async def _record(self) -> msgspec.Raw | None:
        if self._source is not None:
            return self._source
        found = records(await self.state.get_listing(self.publication_id))
        return found[0] if found else None

    async def fetch(self) -> ListingDetail | None:
        """Fetch the listing's full details.

        Returns
        -------
        :class:`ListingDetail` | :data:`None`
            The listing, or :data:`None` if it no longer exists.

        Raises
        ------
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        found = records(await self.state.get_listing(self.publication_id))
        if not found:
            return None
        detail = ListingDetail(self.state.decode_listing(found[0]), self.state)
        detail._source = found[0]
        return detail

    async def photos(self) -> list[FileItem]:
        """Fetch the listing's photos.

        Returns
        -------
        list[:class:`FileItem`]
            Each photo, in the order the website shows them.

        Raises
        ------
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        response = await self.state.get_listing_photos(self.publication_id)
        return [FileItem(item, self.state) for item in records(response)]

    async def extras(self) -> ListingExtras | None:
        """Fetch the listing's description, costs, criteria, rooms and facilities.

        Returns
        -------
        :class:`ListingExtras` | :data:`None`
            :data:`None` if the listing no longer exists.

        Raises
        ------
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        record = await self._record()
        return ListingExtras(await self.state.get_listing_extras(record), self.state) if record else None

    async def downloads(self) -> list[FileItem]:
        """Fetch the files attached to the listing, such as brochures.

        Returns
        -------
        list[:class:`FileItem`]
            An empty list if the listing no longer exists.

        Raises
        ------
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        record = await self._record()
        if record is None:
            return []
        response = await self.state.get_listing_downloads(record)
        return [FileItem(item, self.state) for item in records(response)]

    async def vr_floorplans(self) -> list[FileItem]:
        """Fetch the listing's interactive floor plans.

        Returns
        -------
        list[:class:`FileItem`]
            An empty list if the listing no longer exists.

        Raises
        ------
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        record = await self._record()
        if record is None:
            return []
        response = await self.state.get_listing_vr_floorplans(record)
        return [FileItem(item, self.state) for item in records(response)]

    async def housing_costs(self) -> HousingCostsResponse | None:
        """Fetch the estimated monthly costs of living in the home.

        Returns
        -------
        :class:`HousingCostsResponse` | :data:`None`
            :data:`None` if the listing no longer exists.

        Raises
        ------
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        record = await self._record()
        return HousingCostsResponse(await self.state.get_housing_costs(record), self.state) if record else None

    async def enrolment_information(self) -> EnrolmentInformation:
        """Fetch how candidates are ranked, and whether the account qualifies.

        Returns
        -------
        :class:`EnrolmentInformation`
            The ranking rules, each with whether the account meets it.

        Raises
        ------
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        applicant = await self.state.get_applicant(self.publication_id)
        response = await self.state.get_enrolment_information(self.publication_id, applicant.get("NatuurlijkPersoonId", "0"))
        return EnrolmentInformation(response, self.state)

    async def eligibility_rules(self) -> list[EligibilityRule]:
        """Fetch the listing's conditions, each with whether the account meets it.

        Returns
        -------
        list[:class:`EligibilityRule`]
            Each condition with whether the account meets it.

        Raises
        ------
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        response = await self.state.get_eligibility(self.publication_id)
        return EligibilityResponse(response, self.state).rules

    async def react(self) -> ActionResult:
        """React to the listing.

        **This places a real reaction on the account.**

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
        return ActionResult(await self.state.react(self.publication_id), self.state)

    async def withdraw_reaction(self) -> ActionResult:
        """Withdraw the account's reaction to the listing.

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
        return ActionResult(await self.state.withdraw_reaction(self.publication_id), self.state)

    async def set_saved(self, saved: bool = True) -> ActionResult:
        """Save the listing, or remove it from the saved listings.

        Parameters
        ----------
        saved: :class:`bool`, optional
            :data:`True` to save the listing, :data:`False` to remove it. Defaults to :data:`True`.

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
        return ActionResult(await self.state.set_saved(self.publication_id, saved), self.state)

    async def set_hidden(self, hidden: bool = True) -> ActionResult:
        """Hide the listing, or show it again.

        Parameters
        ----------
        hidden: :class:`bool`, optional
            :data:`True` to hide the listing, :data:`False` to show it again. Defaults to :data:`True`.

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
        return ActionResult(await self.state.set_hidden(self.publication_id, hidden), self.state)


class PartialListing(BaseListing):
    """A listing of which only the ID is known.

    Use it to call a listing's methods without fetching it first. Get one with
    :meth:`ListingsClient.partial`.

    Parameters
    ----------
    publication_id: :class:`int`
        The listing's ID.
    state: :class:`HTTPClient`
        The HTTP client to make requests with.
    """

    def __init__(self, publication_id: int, state: HTTPClient) -> None:
        super().__init__({}, state)
        self._publication_id = publication_id

    @property
    @override
    def publication_id(self) -> int:
        """The listing's ID.

        Returns
        -------
        :class:`int`
            The ID.
        """
        return self._publication_id

    @override
    def __repr__(self) -> str:
        return f"PartialListing(publication_id={self._publication_id})"


class DetailPublication(Model):
    """The listing itself, as shown on its detail page.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The listing's ID. (*publicatie id*)
    region_id: :class:`str` | :data:`None`
        The ID of the region. (*samenwerkingsverband id*)
    available_units: :class:`int` | :data:`None`
        The number of homes available. (*aantal eenheden beschikbaar*)
    contract_type: :class:`str` | :data:`None`
        The type of rental contract, such as temporary or permanent. (*contract vorm*)
    rule_set: :class:`str` | :data:`None`
        The set of allocation rules that applies. (*spelregel set*)
    duration: :class:`str` | :data:`None`
        How long the rental contract runs, for temporary contracts. (*looptijd*)
    contract_end_date: :class:`str` | :data:`None`
        The end date of a temporary contract, as an ISO 8601 string. (*contract eind datum*)
    status: :class:`str` | :data:`None`
        The status of the listing. (*publicatie status*)
    detail_status: :class:`str` | :data:`None`
        The detailed status of the listing. (*publicatie detail status*)
    has_personalised_rent: :class:`bool`
        Whether the rent depends on the household's income. (*met gepersonaliseerde huur*)
    advertisement_url: :class:`str` | :data:`None`
        The URL of the landlord's own advertisement. (*advertentie url*)
    allocation_model: :class:`str` | :data:`None`
        How the listing is allocated, such as by waiting time or by lottery. (*publicatie model*)
    listing_type: :class:`str` | :data:`None`
        The kind of listing, such as social rent or mid-rent. (*publicatie module*)
    delivery: :class:`str` | :data:`None`
        How the home is delivered, such as with or without flooring. (*oplevering*)
    allocation_process: :class:`str` | :data:`None`
        The kind of allocation process. (*aanbieding proces soort*)
    is_open_to_everyone: :class:`bool`
        Whether every household qualifies for the home. (*is passend voor iedereen*)
    has_candidate_list: :class:`bool`
        Whether a list of candidates has been made. (*heeft kandidaten lijst*)
    """

    id = field(str, "PublicatieId")
    region_id = field(str, "SamenwerkingsverbandId")
    available_units = field(int, "AantalEenhedenBeschikbaar")
    _published_at = field(str, "BeginDatumTijd")
    _deadline = field(str, "EindDatumTijd")
    contract_type = field(str, "ContractVorm")
    rule_set = field(str, "SpelregelSet")
    duration = field(str, "Looptijd")
    _available_from = field(str, "OpleverDatum")
    contract_end_date = field(str, "ContractEindDatum")
    _labels = field(str, "PublicatieLabel")
    status = field(str, "PublicatieStatus")
    detail_status = field(str, "PublicatieDetailStatus")
    has_personalised_rent = field(bool, "MetGepersonaliseerdeHuur", default=False)
    advertisement_url = field(str, "AdvertentieURL")
    allocation_model = field(str, "PublicatieModel")
    listing_type = field(str, "PublicatieModule")
    delivery = field(str, "Oplevering")
    allocation_process = field(str, "AanbiedingProcesSoort")
    is_open_to_everyone = field(bool, "IsPassendVoorIedereen", default=False)
    has_candidate_list = field(bool, "HeeftKandidatenLijst", default=False)

    @property
    def labels(self) -> list[str]:
        """The listing's labels, such as ``['Met situatiepunten', 'Jongerenwoning']``.

        Returns
        -------
        list[:class:`str`]
            The labels, or an empty list if the listing has none.
        """
        return [part.strip() for part in (self._labels or "").split("~") if part.strip()]

    @property
    def published_at(self) -> dt.datetime | None:
        """When the listing was published.

        Returns
        -------
        :class:`~datetime.datetime` | :data:`None`
            The date and time, or :data:`None` if it is not known.
        """
        return parse_datetime(self._published_at)

    @property
    def deadline(self) -> dt.datetime | None:
        """When reactions close.

        Returns
        -------
        :class:`~datetime.datetime` | :data:`None`
            The date and time, or :data:`None` if it is not known.
        """
        return parse_datetime(self._deadline)

    @property
    def available_from(self) -> dt.datetime | None:
        """When the home becomes available.

        Returns
        -------
        :class:`~datetime.datetime` | :data:`None`
            The date, or :data:`None` if it is not known.
        """
        return parse_datetime(self._available_from)


class DetailUnit(Model):
    """The home offered in a listing (*eenheid*), as shown on its detail page.

    It has more fields than :class:`Unit`, which is used in the overview.

    Attributes
    ----------
    code: :class:`str` | :data:`None`
        The home's code.
    name: :class:`str` | :data:`None`
        The home's name. (*naam*)
    description: :class:`str` | :data:`None`
        The home's description. (*omschrijving*)
    kind: :class:`str` | :data:`None`
        The kind of home, such as a dwelling or a parking space. (*eenheid soort*)
    housing_type: :class:`str` | :data:`None`
        The type of home, such as ``Eengezinswoning``. (*detail soort*)
    status: :class:`str` | :data:`None`
        The status of the home. (*eenheid status*)
    landlord: :class:`str` | :data:`None`
        The landlord that owns the home. (*eigenaar*)
    rooms: :class:`int` | :data:`None`
        The number of rooms. (*aantal kamers*)
    total_area: :class:`str` | :data:`None`
        The total floor area in square metres, as a decimal string. (*totale oppervlakte*)
    other_rooms_area: :class:`str` | :data:`None`
        The area of the other rooms in square metres, as a decimal string. (*overige vertrekken tot oppervla*)
    purpose: :class:`str` | :data:`None`
        What the home is intended for, such as living or parking. (*bestemming*)
    target_group: :class:`str` | :data:`None`
        The target group, such as seniors or young people. (*doelgroep*)
    extra_target_group: :class:`str` | :data:`None`
        An additional target group. (*aanvullende doelgroep*)
    housing_form: :class:`str` | :data:`None`
        The form of housing, such as shared housing. (*woonvorm*)
    is_self_contained: :class:`bool`
        Whether the home is self-contained, with its own kitchen and bathroom. (*is zelfstandig*)
    has_lift: :class:`bool`
        Whether the building has a lift. (*heeft lift*)
    eligible_rent: :class:`str` | :data:`None`
        The part of the rent that counts for housing benefit, as a decimal string. (*subsidiabele huur*)
    is_new_build: :class:`bool`
        Whether the home is new-build. (*is nieuwbouw*)
    energy_label: :class:`str` | :data:`None`
        The energy label, such as ``A``. (*energie label*)
    accessibility: :class:`str` | :data:`None`
        How accessible the home is. (*toegankelijkheid*)
    """

    code = field(str, "Code")
    name = field(str, "Naam")
    description = field(str, "Omschrijving")
    kind = field(str, "EenheidSoort")
    housing_type = field(str, "DetailSoort")
    status = field(str, "EenheidStatus")
    landlord = field(str, "Eigenaar")
    _floor_known = field(bool, "EtageBekend", default=False)
    _floor = field(int, "Etage")
    rooms = field(int, "AantalKamers")
    total_area = field(str, "TotaleOppervlakte")
    _living_area = field(str, "WoonVertrekkenTotOpp")
    other_rooms_area = field(str, "OverigeVertrekkenTotOppervla")
    purpose = field(str, "Bestemming")
    target_group = field(str, "Doelgroep")
    extra_target_group = field(str, "AanvullendeDoelgroep")
    housing_form = field(str, "Woonvorm")
    is_self_contained = field(bool, "IsZelfstandig", default=False)
    has_lift = field(bool, "HeeftLift", default=False)
    _built_on = field(str, "OpleverDatum")
    _gross_rent_known = field(bool, "BrutoHuurBekend", default=False)
    _gross_rent = field(str, "BrutoHuur")
    _net_rent_known = field(bool, "NettoHuurBekend", default=False)
    _net_rent = field(str, "NettoHuur")
    eligible_rent = field(str, "SubsidiabeleHuur")
    is_new_build = field(bool, "IsNieuwbouw", default=False)
    energy_label = field(str, "EnergieLabel")
    _longitude = field(str, "Lengtegraad")
    _latitude = field(str, "Breedtegraad")
    accessibility = field(str, "Toegankelijkheid")

    @property
    def net_rent(self) -> Decimal | None:
        """The net rent per month.

        Returns
        -------
        :class:`~decimal.Decimal` | :data:`None`
            :data:`None` if the rent is not known.
        """
        return parse_decimal(self._net_rent) if self._net_rent_known else None

    @property
    def gross_rent(self) -> Decimal | None:
        """The gross rent per month.

        Returns
        -------
        :class:`~decimal.Decimal` | :data:`None`
            :data:`None` if the rent is not known.
        """
        return parse_decimal(self._gross_rent) if self._gross_rent_known else None

    @property
    def living_area(self) -> Decimal | None:
        """The living area in square metres.

        Returns
        -------
        :class:`~decimal.Decimal` | :data:`None`
            The area, or :data:`None` if it is not known.
        """
        return parse_decimal(self._living_area)

    @property
    def floor(self) -> int | None:
        """The floor the home is on.

        Returns
        -------
        :class:`int` | :data:`None`
            :data:`None` if the floor is not known.
        """
        return self._floor if self._floor_known else None

    @property
    def build_year(self) -> int | None:
        """The year the home was built.

        Returns
        -------
        :class:`int` | :data:`None`
            The year, or :data:`None` if it is not known.
        """
        built = parse_datetime(self._built_on)
        return built.year if built else None

    @property
    def coordinates(self) -> tuple[float, float] | None:
        """The home's location.

        Returns
        -------
        tuple[:class:`float`, :class:`float`] | :data:`None`
            The latitude and longitude, or :data:`None` if the location is not known.
        """
        lat, lon = float(self._latitude or 0), float(self._longitude or 0)
        return (lat, lon) if lat and lon else None


class DetailAddress(Model):
    """The address of a listing, as shown on its detail page.

    ``str(address)`` gives the full address on one line.

    Attributes
    ----------
    street: :class:`str` | :data:`None`
        The street name. (*straatnaam*)
    house_number: :class:`int` | :data:`None`
        The house number. (*huisnummer*)
    house_letter: :class:`str` | :data:`None`
        The letter after the house number, such as ``A``. (*huisletter*)
    house_number_addition: :class:`str` | :data:`None`
        The house number addition, such as ``2-hoog``. (*huisnummer toevoeging*)
    postcode: :class:`str` | :data:`None`
        The postcode.
    municipality: :class:`str` | :data:`None`
        The municipality. (*gemeente*)
    city: :class:`str` | :data:`None`
        The town or city. (*woonplaats*)
    district: :class:`str` | :data:`None`
        The district. (*wijk*)
    neighbourhood: :class:`str` | :data:`None`
        The neighbourhood. (*buurt*)
    """

    street = field(str, "Straatnaam")
    house_number = field(int, "Huisnummer")
    house_letter = field(str, "Huisletter")
    house_number_addition = field(str, "HuisnummerToevoeging")
    postcode = field(str, "Postcode")
    municipality = field(str, "Gemeente")
    city = field(str, "Woonplaats")
    district = field(str, "Wijk")
    neighbourhood = field(str, "Buurt")

    @property
    def street_line(self) -> str:
        """The street, house number, letter and addition on one line, such as ``Damstraat 12A 2``.

        Returns
        -------
        :class:`str`
            The address line, or an empty string if the address is not known.
        """
        house = "".join(p for p in (str(self.house_number) if self.house_number else None, self.house_letter) if p)
        return " ".join(p for p in (self.street, house, self.house_number_addition) if p)

    @override
    def __str__(self) -> str:
        locality = " ".join(p for p in (self.postcode, self.city) if p)
        return ", ".join(p for p in (self.street_line, locality) if p)


class DetailCluster(Model):
    """A group of homes offered as one listing, as shown on its detail page.

    Attributes
    ----------
    name: :class:`str` | :data:`None`
        The name of the project. (*naam*)
    housing_type: :class:`str` | :data:`None`
        The type of homes in the project. (*detail soort*)
    landlord: :class:`str` | :data:`None`
        The landlord that owns the home. (*eigenaar*)
    unit_count: :class:`int` | :data:`None`
        The number of homes in the complex. (*aantal eenheden*)
    minimum_rooms: :class:`int` | :data:`None`
        The smallest number of rooms of the homes in the complex. (*aantal kamers min*)
    maximum_rooms: :class:`int` | :data:`None`
        The largest number of rooms of the homes in the complex. (*aantal kamers max*)
    minimum_price: :class:`str` | :data:`None`
        The lowest rent of the homes in the complex, as a decimal string. (*prijs min*)
    maximum_price: :class:`str` | :data:`None`
        The highest rent of the homes in the complex, as a decimal string. (*prijs max*)
    """

    name = field(str, "Naam")
    _text = field(str, "BasisPublicatieTekst")
    housing_type = field(str, "DetailSoort")
    landlord = field(str, "Eigenaar")
    unit_count = field(int, "AantalEenheden")
    minimum_rooms = field(int, "AantalKamersMin")
    maximum_rooms = field(int, "AantalKamersMax")
    minimum_price = field(str, "PrijsMin")
    maximum_price = field(str, "PrijsMax")

    @property
    def text_html(self) -> str | None:
        """The project's description as HTML.

        Returns
        -------
        :class:`str` | :data:`None`
            The HTML, or :data:`None` if there is no description.
        """
        return decode_html(self._text)


class ListingDetail(BaseListing):
    """A listing as shown on its detail page.

    Get one with :meth:`ListingsClient.fetch` or :meth:`BaseListing.fetch`. It has every method of
    :class:`BaseListing`.

    Attributes
    ----------
    publication: :class:`DetailPublication`
        The listing itself. (*publicatie*)
    unit: :class:`DetailUnit`
        The home. (*eenheid*)
    address: :class:`DetailAddress`
        The address. (*adres*)
    cluster: :class:`DetailCluster`
        The group of homes, if the listing is one. See also ``is_cluster``. (*cluster*)
    """

    publication = Nested(DetailPublication, "Publicatie")
    unit = Nested(DetailUnit, "Eenheid")
    address = Nested(DetailAddress, "Adres")
    cluster = Nested(DetailCluster, "Cluster")

    @property
    @override
    def publication_id(self) -> int:
        """The listing's ID.

        Returns
        -------
        :class:`int`
            The ID.
        """
        return int(self.publication.id or 0)

    @property
    def is_cluster(self) -> bool:
        """Whether the listing is a group of homes.

        Returns
        -------
        :class:`bool`
            :data:`True` if the listing offers several homes at once.
        """
        return bool(self.cluster.name or self.cluster.unit_count)


class File(Model):
    """A file attached to a listing (*bestand*), such as a photo or floor plan.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The file's ID.
    title: :class:`str` | :data:`None`
        The title. (*titel*)
    description: :class:`str` | :data:`None`
        The description. (*beschrijving*)
    format: :class:`str` | :data:`None`
        The file format. (*formaat*)
    kind: :class:`str` | :data:`None`
        The kind of file, such as a photo. (*soort*)
    subkind: :class:`str` | :data:`None`
        The detailed kind of file. (*detail soort*)
    is_primary: :class:`bool`
        Whether this is the listing's main photo. (*primair*)
    order: :class:`int` | :data:`None`
        The position in the list of files. (*volgordenummer*)
    size: :class:`int` | :data:`None`
        The file size in bytes. (*bestandsgrootte*)
    """

    id = field(str, "Id")
    title = field(str, "Titel")
    description = field(str, "Beschrijving")
    format = field(str, "Formaat")
    kind = field(str, "Soort")
    subkind = field(str, "DetailSoort")
    is_primary = field(bool, "Primair", default=False)
    order = field(int, "Volgordenummer")
    size = field(int, "Bestandsgrootte")
    _url = field(str, "Bestandslocatie")

    @property
    def url(self) -> str | None:
        """The URL of the file.

        Returns
        -------
        :class:`str` | :data:`None`
            The URL, or :data:`None` if it is not known.
        """
        return self._url


class FileItem(Model):
    """A file attached to a listing, as the API wraps it.

    Attributes
    ----------
    file: :class:`File`
        The file. (*bestand*)
    """

    file = Nested(File, "Bestand")


class PriceComponent(Model):
    """One part of a listing's rent, such as service charges.

    Attributes
    ----------
    kind: :class:`str` | :data:`None`
        The kind of cost. (*prijscomponent soort*)
    subkind: :class:`str` | :data:`None`
        The detailed kind of cost. (*prijscomponent detailsoort*)
    """

    kind = field(str, "PrijscomponentSoort")
    subkind = field(str, "PrijscomponentDetailsoort")
    _amount = field(str, "Bedrag")
    _amount_known = field(bool, "BedragBekend", default=False)

    @property
    def amount(self) -> Decimal | None:
        """The amount per month.

        Returns
        -------
        :class:`~decimal.Decimal` | :data:`None`
            :data:`None` if the amount is not known.
        """
        return parse_decimal(self._amount) if self._amount_known else None


class Criterion(Model):
    """A rule for who can react to a listing or how candidates are ranked.

    Attributes
    ----------
    label: :class:`str` | :data:`None`
        The rule's name.
    description: :class:`str` | :data:`None`
        What the rule means. (*omschrijving*)
    """

    label = field(str, "Label")
    description = field(str, "Omschrijving")


class RankingRule(Model):
    """A ranking rule of a listing, with whether the account meets it.

    The website shows these with a green tick.

    Attributes
    ----------
    order: :class:`int` | :data:`None`
        The rule's position in the ranking. (*volgorde nummer*)
    description: :class:`str` | :data:`None`
        The rule as the website describes it. (*omschrijving woon portaal*)
    is_met: :class:`bool`
        Whether the account meets the rule. (*waarde*)
    """

    order = field(int, "VolgordeNummer")
    description = field(str, "OmschrijvingWoonPortaal")
    is_met = field(bool, "Waarde", default=False)


class Applicant(Model):
    """The applicant a listing's details were fetched for.

    Attributes
    ----------
    person_id: :class:`str` | :data:`None`
        The person's ID. (*natuurlijk persoon id*)
    """

    person_id = field(str, "NatuurlijkPersoonId")


class EnrolmentInformation(Model):
    """How a listing's candidates are ranked, and whether the account qualifies.

    Attributes
    ----------
    ranking_rules: list[:class:`RankingRule`]
        The ranking rules, each with whether the account meets it. (*publicatie kandidaat sorteer tekst*)
    is_eligible: :class:`bool` | :data:`None`
        Whether the account may react, or :data:`None` if DAK does not say. (*is passend voor kandidaat*)
    """

    ranking_rules = Items(RankingRule, "PublicatieKandidaatSorteerTekst")
    is_eligible = field(bool, "IsPassendVoorKandidaat")


class EligibilityRule(Model):
    """A condition of a listing, with whether the account meets it.

    The website shows these with a tick or a cross for listings the account does not qualify for.

    Attributes
    ----------
    label: :class:`str` | :data:`None`
        The condition's name.
    description: :class:`str` | :data:`None`
        What the condition means. (*omschrijving*)
    is_met: :class:`bool`
        Whether the account meets the condition. (*is passend*)
    """

    label = field(str, "Label")
    description = field(str, "Omschrijving")
    is_met = field(bool, "IsPassend", default=False)


class EligibilityResponse(Model):
    """Why the account does or does not qualify for a listing.

    Attributes
    ----------
    rules: list[:class:`EligibilityRule`]
        The conditions, each with whether the account meets it. (*uitleg lijst*)
    no_reason_found: :class:`bool`
        Whether DAK found no reason why the account does not qualify. (*is geen reden gevonden*)
    """

    rules = Items(EligibilityRule, "UitlegLijst")
    no_reason_found = field(bool, "IsGeenRedenGevonden", default=False)


class Room(Model):
    """A room of the home in a listing.

    Attributes
    ----------
    name: :class:`str` | :data:`None`
        The room's name. (*naam*)
    kind: :class:`str` | :data:`None`
        The kind of room, such as a bedroom. (*ruimte soort*)
    """

    name = field(str, "Naam")
    kind = field(str, "RuimteSoort")
    _area = field(str, "Oppervlakte")

    @property
    def area(self) -> Decimal | None:
        """The room's area in square metres.

        Returns
        -------
        :class:`~decimal.Decimal` | :data:`None`
            The area, or :data:`None` if it is not known.
        """
        return parse_decimal(self._area)


class Facility(Model):
    """A facility of the home in a listing, such as a balcony.

    Attributes
    ----------
    kind: :class:`str` | :data:`None`
        The kind of facility. (*soort*)
    subkind: :class:`str` | :data:`None`
        The detailed kind of facility. (*detail soort*)
    value: :class:`str` | :data:`None`
        The facility's value, such as its size. (*waarde*)
    """

    kind = field(str, "Soort")
    subkind = field(str, "DetailSoort")
    value = field(str, "Waarde")


class _HtmlText(Model):
    text = field(str, "Tekst")


class _Conditions(Model):
    text = field(str, "Voorwaarden")


class ListingExtras(Model):
    """A listing's description, costs, criteria, rooms and facilities.

    Attributes
    ----------
    price_components: list[:class:`PriceComponent`]
        The parts of the rent. See also ``price_components``. (*prijs componenten*)
    sort_criteria: list[:class:`Criterion`]
        How candidates are ranked. See also ``sort_criteria``. (*sorteer criteria list*)
    selection_criteria: list[:class:`Criterion`]
        Who can react. See also ``selection_criteria``. (*selectie criteria list*)
    rooms: list[:class:`Room`]
        The rooms. See also ``rooms``. (*vertrekken list*)
    facilities: list[:class:`Facility`]
        The facilities. See also ``facilities``. (*voorziening list*)
    """

    price_components = Items(PriceComponent, "PrijsComponenten")
    sort_criteria = Items(Criterion, "SorteerCriteriaList")
    selection_criteria = Items(Criterion, "SelectieCriteriaList")
    rooms = Items(Room, "VertrekkenList")
    _conditions = Nested(_Conditions, "PublicatieVoorwaarden")
    facilities = Items(Facility, "VoorzieningList")
    _description = Nested(_HtmlText, "PublicatieTekst")

    @property
    def description_html(self) -> str | None:
        """The listing's full description as HTML.

        Returns
        -------
        :class:`str` | :data:`None`
            The HTML, or :data:`None` if there is no description.
        """
        return decode_html(self._description.text)

    @property
    def conditions_html(self) -> str | None:
        """The listing's conditions as HTML.

        Returns
        -------
        :class:`str` | :data:`None`
            The HTML, or :data:`None` if there are no conditions.
        """
        return decode_html(self._conditions.text)


class HousingCosts(Model):
    """The estimated monthly costs of living in a home.

    Most fields are empty unless the region offers this estimate.

    Attributes
    ----------
    rent: :class:`str` | :data:`None`
        The rent, as a decimal string. (*huur*)
    housing_benefit: :class:`str` | :data:`None`
        The estimated housing benefit, as a decimal string. (*huursubsidie*)
    service_charges: :class:`str` | :data:`None`
        The service charges, as a decimal string. (*servicekosten*)
    energy_costs: :class:`str` | :data:`None`
        The estimated energy costs, as a decimal string. (*totale energielasten*)
    total_costs: :class:`str` | :data:`None`
        The estimated total housing costs, as a decimal string. (*totale woonlasten*)
    affordability_score: :class:`float` | :data:`None`
        How affordable the home is for the account. (*betaalbaarheidscore*)
    """

    rent = field(str, "Huur")
    housing_benefit = field(str, "Huursubsidie")
    service_charges = field(str, "Servicekosten")
    energy_costs = field(str, "TotaleEnergielasten")
    total_costs = field(str, "TotaleWoonlasten")
    affordability_score = field(float, "Betaalbaarheidscore")


class HousingCostsResponse(Model):
    """The estimated monthly costs of living in a listing's home.

    Attributes
    ----------
    costs: :class:`HousingCosts`
        The estimated costs. (*woonlasten profiel*)
    result: :class:`Result`
        Whether fetching the estimate succeeded. (*ophalen gelukt*)
    """

    costs = Nested(HousingCosts, "WoonlastenProfiel")
    result = Nested(Result, "OphalenGelukt")
