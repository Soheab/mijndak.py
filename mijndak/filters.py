from __future__ import annotations

import collections
import enum
from dataclasses import dataclass, field, fields
from typing import TYPE_CHECKING, Final, Self, override
from urllib.parse import parse_qs, quote, urlsplit

if TYPE_CHECKING:
    from collections.abc import Callable, Iterable
    from decimal import Decimal

    from .models import Listing
    from .region import Region

__all__ = ("ListingFilters", "ListingKind", "SortBy", "filter_options", "sort_listings")

NO_TARGET_GROUP: Final = "Geen doelgroep"


class ListingKind(enum.StrEnum):
    """The kind of listing, as the website's *Soort* filter groups them.

    Each value is the name the website shows, which is also what share links use.
    """

    REGULAR = "Aanbod"
    """A home allocated in the usual way, by waiting time, points or priority (*aanbod*)."""
    LOTTERY = "Loting"
    """A home allocated by drawing lots (*loting*)."""
    PARKING_AND_OTHER = "Parkeren & Overige"
    """A parking space or anything else that is not a home (*parkeren & overige*)."""

    @classmethod
    def of(cls, listing: Listing) -> ListingKind:
        """The kind of a listing.

        Parameters
        ----------
        listing: :class:`Listing`
            The listing.

        Returns
        -------
        :class:`ListingKind`
            The kind the website files the listing under.
        """
        if listing.kind and listing.kind != "Woonruimte":
            return cls.PARKING_AND_OTHER
        if listing.allocation_model == "Lotingmodel":
            return cls.LOTTERY
        return cls.REGULAR


class SortBy(enum.Enum):
    """The ways the website can sort listings (*sorteer op*)."""

    MATCH = "match"
    """How well the listing matches the account's housing wishes, best match first (*match met je wensen*)."""
    POSITION = "position"
    """The account's provisional position, best position first (*positie*)."""
    TIME_LEFT = "time_left"
    """The time left to react, closing soonest first (*tijd over om te reageren*)."""
    PRICE = "price"
    """The rent, cheapest first (*prijs*)."""
    ADDED = "added"
    """When the listing was published, newest first (*toegevoegd*)."""
    AREA = "area"
    """The living area, largest first (*oppervlakte*)."""


_SORT_KEYS: Final[dict[SortBy, tuple[Callable[[Listing], object], bool]]] = {
    SortBy.MATCH: (lambda listing: listing.match_percentage, True),
    SortBy.POSITION: (lambda listing: listing.position, False),
    SortBy.TIME_LEFT: (lambda listing: listing.deadline, False),
    SortBy.PRICE: (lambda listing: listing.rent, False),
    SortBy.ADDED: (lambda listing: listing.published_at, True),
    SortBy.AREA: (lambda listing: listing.unit.living_area, True),
}


def sort_listings(listings: Iterable[Listing], by: SortBy = SortBy.MATCH, *, reverse: bool = False) -> list[Listing]:
    """Sort listings the way the website's *sorteer op* menu does.

    Listings without a value for the chosen sort, such as a listing without a position, always go last.

    Parameters
    ----------
    listings: Iterable[:class:`Listing`]
        The listings to sort.
    by: :class:`SortBy`, optional
        What to sort by. Defaults to :attr:`SortBy.MATCH`.
    reverse: :class:`bool`, optional
        Reverse the order, like the website's arrow button. For example, :attr:`SortBy.PRICE` with ``reverse=True``
        puts the most expensive listing first. Defaults to :data:`False`.

    Returns
    -------
    list[:class:`Listing`]
        A new list with the listings in order.
    """
    key, largest_first = _SORT_KEYS[by]
    descending = largest_first != reverse
    items = list(listings)
    known = [listing for listing in items if key(listing) is not None]
    unknown = [listing for listing in items if key(listing) is None]
    known.sort(key=key, reverse=descending)  # pyright: ignore[reportArgumentType]
    return known + unknown


def _target_groups(listing: Listing) -> list[str]:
    return listing.labels or [NO_TARGET_GROUP]


_FILTERS: Final[dict[str, tuple[str, Callable[[Listing], Iterable[str | None]]]]] = {
    "cities": ("woonplaats", lambda listing: [listing.address.city]),
    "kinds": ("soort", lambda listing: [ListingKind.of(listing).value]),
    "housing_types": ("type", lambda listing: [listing.unit.housing_type]),
    "rooms": ("kamers", lambda listing: [None if listing.unit.rooms is None else str(listing.unit.rooms)]),
    "target_groups": ("doelgroep", _target_groups),
    "contract_types": ("contractvorm", lambda listing: [listing.contract_type]),
    "accessibility": ("toegankelijkheid", lambda listing: [listing.unit.accessibility]),
    "landlords": ("aanbieder", lambda listing: [listing.unit.landlord]),
}


@dataclass(frozen=True, slots=True)
class ListingFilters:
    """The filters from the website's filter panel (*filteren*).

    Each option takes the names the website shows, such as ``cities={"Amsterdam", "Zaandam"}``. A listing matches if
    it matches every filter that is set; within one filter, it must match any of the names given. Filters left empty
    match every listing. Use :func:`filter_options` to see which names the listings have.

    Parameters
    ----------
    cities: Iterable[:class:`str`], optional
        Towns or cities, such as ``"Amsterdam"`` (*woonplaats*).
    kinds: Iterable[:class:`ListingKind` | :class:`str`], optional
        Kinds of listing (*soort*).
    minimum_rent: :class:`~decimal.Decimal` | :class:`int` | :data:`None`, optional
        The lowest rent per month (*prijs van*).
    maximum_rent: :class:`~decimal.Decimal` | :class:`int` | :data:`None`, optional
        The highest rent per month (*prijs tot*).
    housing_types: Iterable[:class:`str`], optional
        Types of home, such as ``"Portiekflat"`` (*type woning*).
    rooms: Iterable[:class:`int`], optional
        Numbers of rooms (*aantal kamers*).
    target_groups: Iterable[:class:`str`], optional
        Target groups, such as ``"Jongerenwoning"``, or ``"Geen doelgroep"`` for listings without one (*doelgroep*).
    contract_types: Iterable[:class:`str`], optional
        Types of contract, such as ``"Onbepaalde tijd contract"`` (*contractvorm*).
    accessibility: Iterable[:class:`str`], optional
        How accessible the home is, such as ``"Gelijkvloerse woning"`` (*toegankelijkheid*).
    landlords: Iterable[:class:`str`], optional
        Landlords, such as ``"Ymere"`` (*aanbieder*).

    Examples
    --------
    ::

        filters = ListingFilters(cities={"Amsterdam"}, rooms={2, 3}, maximum_rent=900)
        for listing in filters.apply(await client.listings.matching()):
            print(listing.address, listing.rent)

        print(filters.to_url(client.region))
    """

    cities: frozenset[str] = field(default=frozenset())
    kinds: frozenset[str] = field(default=frozenset())
    minimum_rent: Decimal | int | None = None
    maximum_rent: Decimal | int | None = None
    housing_types: frozenset[str] = field(default=frozenset())
    rooms: frozenset[str] = field(default=frozenset())
    target_groups: frozenset[str] = field(default=frozenset())
    contract_types: frozenset[str] = field(default=frozenset())
    accessibility: frozenset[str] = field(default=frozenset())
    landlords: frozenset[str] = field(default=frozenset())

    def __init__(
        self,
        *,
        cities: Iterable[str] = (),
        kinds: Iterable[ListingKind | str] = (),
        minimum_rent: Decimal | int | None = None,
        maximum_rent: Decimal | int | None = None,
        housing_types: Iterable[str] = (),
        rooms: Iterable[int | str] = (),
        target_groups: Iterable[str] = (),
        contract_types: Iterable[str] = (),
        accessibility: Iterable[str] = (),
        landlords: Iterable[str] = (),
    ) -> None:
        values: dict[str, object] = {
            "cities": frozenset(cities),
            "kinds": frozenset(str(kind) for kind in kinds),
            "minimum_rent": minimum_rent,
            "maximum_rent": maximum_rent,
            "housing_types": frozenset(housing_types),
            "rooms": frozenset(str(count) for count in rooms),
            "target_groups": frozenset(target_groups),
            "contract_types": frozenset(contract_types),
            "accessibility": frozenset(accessibility),
            "landlords": frozenset(landlords),
        }
        for name, value in values.items():
            object.__setattr__(self, name, value)

    def matches(self, listing: Listing) -> bool:
        """Check whether a listing matches every filter.

        Parameters
        ----------
        listing: :class:`Listing`
            The listing to check.

        Returns
        -------
        :class:`bool`
            :data:`True` if the listing matches.
        """
        for name, (_, values) in _FILTERS.items():
            wanted: frozenset[str] = getattr(self, name)
            if wanted and not any(value in wanted for value in values(listing)):
                return False
        if self.minimum_rent is not None or self.maximum_rent is not None:
            rent = listing.rent
            if rent is None:
                return False
            if self.minimum_rent is not None and rent < self.minimum_rent:
                return False
            if self.maximum_rent is not None and rent > self.maximum_rent:
                return False
        return True

    def apply(self, listings: Iterable[Listing]) -> list[Listing]:
        """Keep only the listings that match every filter.

        Parameters
        ----------
        listings: Iterable[:class:`Listing`]
            The listings to filter.

        Returns
        -------
        list[:class:`Listing`]
            The matching listings, in their original order.
        """
        return [listing for listing in listings if self.matches(listing)]

    def to_url(self, region: Region, *, logged_in: bool = True) -> str:
        """The link the website's *URL kopiëren* button makes for these filters.

        The website does not put the rent in its links, so :attr:`minimum_rent` and :attr:`maximum_rent` are left out.

        Parameters
        ----------
        region: :class:`Region`
            The region whose website the link is for.
        logged_in: :class:`bool`, optional
            Link to the overview for logged-in visitors. Use :data:`False` for the public overview. Defaults to
            :data:`True`.

        Returns
        -------
        :class:`str`
            The link, such as ``https://amsterdam.mijndak.nl/WoningOverzicht?woonplaats=Amsterdam&kamers=2,3``.
        """
        page = "WoningOverzicht" if logged_in else "Woningaanbod"
        parameters = [
            f"{parameter}={','.join(quote(value, safe='') for value in sorted(getattr(self, name)))}"
            for name, (parameter, _) in _FILTERS.items()
            if getattr(self, name)
        ]
        query = f"?{'&'.join(parameters)}" if parameters else ""
        return f"{region.base_url.rstrip('/')}/{page}{query}"

    @classmethod
    def from_url(cls, url: str) -> Self:
        """Read the filters from a link the website's *URL kopiëren* button made.

        Parameters
        ----------
        url: :class:`str`
            The link, or only its query string.

        Returns
        -------
        :class:`ListingFilters`
            The filters in the link. Filters the link does not set are left empty.
        """
        query = urlsplit(url).query if "://" in url or url.startswith("/") else url.removeprefix("?")
        parsed = parse_qs(query)

        def values(name: str) -> list[str]:
            parameter = _FILTERS[name][0]
            return [value for part in parsed.get(parameter, []) for value in part.split(",") if value]

        return cls(
            cities=values("cities"),
            kinds=values("kinds"),
            housing_types=values("housing_types"),
            rooms=values("rooms"),
            target_groups=values("target_groups"),
            contract_types=values("contract_types"),
            accessibility=values("accessibility"),
            landlords=values("landlords"),
        )

    @override
    def __repr__(self) -> str:
        shown = [
            f"{f.name}={getattr(self, f.name)!r}" for f in fields(self) if getattr(self, f.name) not in {frozenset(), None}
        ]
        return f"ListingFilters({', '.join(shown)})"


def filter_options(listings: Iterable[Listing]) -> dict[str, dict[str, int]]:
    """The options of each filter and how many listings have each, like the website's filter panel.

    Parameters
    ----------
    listings: Iterable[:class:`Listing`]
        The listings to count.

    Returns
    -------
    dict[:class:`str`, dict[:class:`str`, :class:`int`]]
        For each :class:`ListingFilters` option, such as ``"cities"``, the names to choose from and how many listings
        have each, most common first.
    """
    items = list(listings)
    options: dict[str, dict[str, int]] = {}
    for name, (_, values) in _FILTERS.items():
        counts = collections.Counter(value for listing in items for value in set(values(listing)) if value is not None)
        options[name] = dict(counts.most_common())
    return options
