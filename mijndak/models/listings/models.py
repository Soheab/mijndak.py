from __future__ import annotations

from typing import TYPE_CHECKING, override

from ..base import Model, Nested, field, parse_datetime, parse_decimal
from .details import BaseListing

if TYPE_CHECKING:
    import datetime as dt
    from decimal import Decimal

__all__ = ("Address", "Cluster", "Listing", "ListingDescription", "Unit")


def _street_line(street: str | None, number: int | None, letter: str | None, addition: str | None) -> str:
    house = "".join(p for p in (str(number) if number else None, letter) if p)
    return " ".join(p for p in (street, house, addition) if p)


class Address(Model):
    """The address of a listing.

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
    city: :class:`str` | :data:`None`
        The town or city. (*woonplaats*)
    district: :class:`str` | :data:`None`
        The district. (*wijk*)
    listing_id: :class:`str` | :data:`None`
        The ID of the listing the address belongs to. (*publicatie id*)
    """

    street = field(str, "Straatnaam")
    house_number = field(int, "Huisnummer")
    house_letter = field(str, "Huisletter")
    house_number_addition = field(str, "HuisnummerToevoeging")
    postcode = field(str, "Postcode")
    city = field(str, "Woonplaats")
    district = field(str, "Wijk")
    listing_id = field(str, "PublicatieId")

    @property
    def street_line(self) -> str:
        """The street, house number, letter and addition on one line, such as ``Damstraat 12A 2``.

        Returns
        -------
        :class:`str`
            The address line, or an empty string if the address is not known.
        """
        return _street_line(self.street, self.house_number, self.house_letter, self.house_number_addition)

    @override
    def __str__(self) -> str:
        locality = " ".join(p for p in (self.postcode, self.city) if p)
        return ", ".join(p for p in (self.street_line, locality) if p)


class Unit(Model):
    """The home offered in a listing (*eenheid*), as shown in the overview.

    Attributes
    ----------
    housing_type: :class:`str` | :data:`None`
        The type of home, such as ``Eengezinswoning``. (*detail soort*)
    purpose: :class:`str` | :data:`None`
        What the home is intended for, such as living or parking. (*bestemming*)
    rooms: :class:`int` | :data:`None`
        The number of rooms. (*aantal kamers*)
    total_area: :class:`str` | :data:`None`
        The total floor area in square metres, as a decimal string. (*totale oppervlakte*)
    target_group: :class:`str` | :data:`None`
        The target group, such as seniors or young people. (*doelgroep*)
    eligible_rent: :class:`str` | :data:`None`
        The part of the rent that counts for housing benefit, as a decimal string. (*subsidiabele huur*)
    accessibility: :class:`str` | :data:`None`
        How accessible the home is. (*toegankelijkheid*)
    accessibility_tag: :class:`str` | :data:`None`
        A short label for how accessible the home is. (*toegankelijkheidstag*)
    building_type: :class:`str` | :data:`None`
        The type of building. (*soort bouw*)
    energy_label: :class:`str` | :data:`None`
        The energy label, such as ``A``. (*energie label*)
    energy_index: :class:`float` | :data:`None`
        The energy index. (*energie index*)
    landlord: :class:`str` | :data:`None`
        The landlord that owns the home. (*eigenaar*)
    """

    housing_type = field(str, "DetailSoort")
    purpose = field(str, "Bestemming")
    rooms = field(int, "AantalKamers")
    total_area = field(str, "TotaleOppervlakte")
    _living_area = field(str, "WoonVertrekkenTotOpp")
    target_group = field(str, "Doelgroep")
    _net_rent_known = field(bool, "NettoHuurBekend", default=False)
    _net_rent = field(str, "NettoHuur")
    _gross_rent_known = field(bool, "BrutoHuurBekend", default=False)
    _gross_rent = field(str, "Brutohuur")
    eligible_rent = field(str, "SubsidiabeleHuur")
    _longitude = field(str, "Lengtegraad")
    _latitude = field(str, "Breedtegraad")
    accessibility = field(str, "Toegankelijkheid")
    accessibility_tag = field(str, "Toegankelijkheidstag")
    building_type = field(str, "SoortBouw")
    energy_label = field(str, "EnergieLabel")
    energy_index = field(float, "EnergieIndex")
    landlord = field(str, "Eigenaar")

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
    def coordinates(self) -> tuple[float, float] | None:
        """The home's location.

        Returns
        -------
        tuple[:class:`float`, :class:`float`] | :data:`None`
            The latitude and longitude, or :data:`None` if the location is not known.
        """
        lat, lon = float(self._latitude or 0), float(self._longitude or 0)
        return (lat, lon) if lat and lon else None


class Cluster(Model):
    """A group of homes offered as one listing, such as a new-build project.

    Attributes
    ----------
    name: :class:`str` | :data:`None`
        The name of the project. (*naam*)
    housing_type: :class:`str` | :data:`None`
        The type of home, such as ``Eengezinswoning``. (*detail soort*)
    target_group: :class:`str` | :data:`None`
        The target group, such as seniors or young people. (*doelgroep*)
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
    landlord: :class:`str` | :data:`None`
        The landlord that owns the home. (*eigenaar*)
    """

    name = field(str, "Naam")
    housing_type = field(str, "DetailSoort")
    target_group = field(str, "Doelgroep")
    unit_count = field(int, "AantalEenheden")
    minimum_rooms = field(int, "AantalKamersMin")
    maximum_rooms = field(int, "AantalKamersMax")
    minimum_price = field(str, "PrijsMin")
    maximum_price = field(str, "PrijsMax")
    landlord = field(str, "Eigenaar")


class ListingDescription(Model):
    """The short description of a listing.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The description's ID.
    text: :class:`str` | :data:`None`
        The description. (*tekst*)
    """

    id = field(str, "Id")
    text = field(str, "Tekst")


class Listing(BaseListing):
    """A housing listing (*publicatie*), as shown in the overview.

    It has every method of :class:`BaseListing`, such as :meth:`~BaseListing.fetch` and
    :meth:`~BaseListing.react`.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The listing's ID. See also ``publication_id``.
    allocation_model: :class:`str` | :data:`None`
        How the listing is allocated, such as by waiting time or by lottery. (*publicatie model*)
    listing_type: :class:`str` | :data:`None`
        The kind of listing, such as social rent or mid-rent. (*publicatie module*)
    photo_url: :class:`str` | :data:`None`
        The URL of the main photo. (*foto locatie*)
    match_percentage: :class:`float` | :data:`None`
        How well the home matches the account's housing wishes, as a percentage. (*matchpercentage*)
    success_chance: :class:`float` | :data:`None`
        The estimated chance of getting the home, as a percentage. (*slaagkans*)
    is_cluster: :class:`bool`
        Whether the listing is a group of homes. (*is cluster*)
    kind: :class:`str` | :data:`None`
        The kind of home, such as a dwelling or a parking space. (*eenheid soort*)
    address: :class:`Address`
        The address. (*adres*)
    unit: :class:`Unit`
        The home. (*eenheid*)
    cluster: :class:`Cluster`
        The group of homes, if the listing is one. (*cluster*)
    contract_type: :class:`str` | :data:`None`
        The type of rental contract, such as temporary or permanent. (*contract vorm*)
    summary: :class:`ListingDescription`
        The short description. (*publicatie omschrijving*)
    is_saved: :class:`bool`
        Whether the account saved the listing. (*is bewaard*)
    is_hidden: :class:`bool`
        Whether the account hid the listing. (*is verborgen*)
    has_reacted: :class:`bool`
        Whether the account reacted to the listing. (*heeft gereageerd*)
    can_withdraw: :class:`bool`
        Whether the account's reaction can still be withdrawn. (*is intrekken reactie toegestaan*)
    withdraw_blocked_reason: :class:`str` | :data:`None`
        Why the reaction can no longer be withdrawn. (*reden niet intrekken reactie*)
    allocation_stage: :class:`str` | :data:`None`
        The stage the allocation is in. (*positie aanbiedingsproces*)
    virtual_position: :class:`int` | :data:`None`
        The account's position as the website shows it. (*virtuele positie*)
    has_lift: :class:`bool`
        Whether the building has a lift. (*heeft lift*)
    floor: :class:`str` | :data:`None`
        The floor the home is on. (*verdieping*)
    allocation_process: :class:`str` | :data:`None`
        The kind of allocation process. (*aanbieding proces soort*)
    """

    id = field(str, "Id")
    _deadline = field(str, "EinddatumTijd")
    _published_at = field(str, "PublicatieDatum")
    allocation_model = field(str, "PublicatieModel")
    listing_type = field(str, "PublicatieModule")
    _labels = field(str, "PublicatieLabel")
    photo_url = field(str, "Foto_Locatie")
    match_percentage = field(float, "Matchpercentage")
    _position = field(str, "VoorlopigePositie")
    success_chance = field(float, "Slaagkans")
    _personalised_rent = field(str, "GepersonaliseerdeHuur")
    is_cluster = field(bool, "IsCluster", default=False)
    kind = field(str, "EenheidSoort")
    address = Nested(Address, "Adres")
    unit = Nested(Unit, "Eenheid")
    cluster = Nested(Cluster, "Cluster")
    contract_type = field(str, "ContractVorm")
    summary = Nested(ListingDescription, "PublicatieOmschrijving")
    is_saved = field(bool, "IsBewaard", default=False)
    is_hidden = field(bool, "IsVerborgen", default=False)
    has_reacted = field(bool, "HeeftGereageerd", default=False)
    can_withdraw = field(bool, "IsIntrekkenReactieToegestaan", default=False)
    withdraw_blocked_reason = field(str, "RedenNietIntrekkenReactie")
    _reaction_count = field(str, "AantalReactiesOpPublicatie")
    allocation_stage = field(str, "PositieAanbiedingsproces")
    virtual_position = field(int, "VirtuelePositie")
    _available_from = field(str, "Opleverdatum")
    has_lift = field(bool, "HeeftLift", default=False)
    floor = field(str, "Verdieping")
    allocation_process = field(str, "AanbiedingProcesSoort")

    @property
    @override
    def publication_id(self) -> int:
        """The listing's ID.

        Returns
        -------
        :class:`int`
            The ID.
        """
        return int(self.id or 0)

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
    def deadline(self) -> dt.datetime | None:
        """When reactions close.

        Returns
        -------
        :class:`~datetime.datetime` | :data:`None`
            The date and time, or :data:`None` if it is not known.
        """
        return parse_datetime(self._deadline)

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
    def available_from(self) -> dt.datetime | None:
        """When the home becomes available.

        Returns
        -------
        :class:`~datetime.datetime` | :data:`None`
            The date, or :data:`None` if it is not known.
        """
        return parse_datetime(self._available_from)

    @property
    def position(self) -> int | None:
        """The account's provisional position among the candidates.

        Returns
        -------
        :class:`int` | :data:`None`
            :data:`None` if DAK does not report a position.
        """
        return int(self._position or 0) or None

    @property
    def reaction_count(self) -> int:
        """The number of reactions to the listing.

        Returns
        -------
        :class:`int`
            The number, or ``0`` if it is not known.
        """
        return int(self._reaction_count or 0)

    @property
    def rent(self) -> Decimal | None:
        """The rent per month.

        This is the rent calculated for the account if DAK gives one, and the net rent otherwise.

        Returns
        -------
        :class:`~decimal.Decimal` | :data:`None`
            :data:`None` if the rent is not known.
        """
        return parse_decimal(self._personalised_rent) or self.unit.net_rent

    @property
    def url_path(self) -> str:
        """The path of the listing's page on the website, such as ``/HuisDetails?PublicatieId=123``.

        Returns
        -------
        :class:`str`
            The path, relative to the region's website.
        """
        return f"/HuisDetails?PublicatieId={self.id}"
