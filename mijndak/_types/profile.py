from __future__ import annotations

from typing import TypedDict

from .common import OSListPayload, ResultPayload
from .listings.payloads import ListingPayload

__all__ = (
    "AccessibilityPayload",
    "DistrictPayload",
    "HousingTypeGroupPayload",
    "NamedEntityPayload",
    "NavigationLocationPayload",
    "NavigationOptionPayload",
    "NavigationTypePayload",
    "PlaceWithDistrictsPayload",
    "PointsCategoryPayload",
    "PointsDashboardPayload",
    "PointsPayload",
    "ReactionItemPayload",
    "ReactionPayload",
    "ReactionsPayload",
    "SearchPointsMonthPayload",
    "SearchPointsPayload",
    "TimedPointsCategoryPayload",
    "WishesPayload",
    "WoonwensPayload",
)


class ReactionPayload(TypedDict, total=False):
    """``ReactieV11``: the state of one of your reactions."""

    PublicatieId: str
    AanbiedingId: str
    AanbiedingStatus: str
    AanbiedingDetailstatus: str
    ReactieStatus: str
    ReactieSoort: str
    ReactiePositie: int
    PositieAanbiedingsproces: str
    AantalReactiesOpPublicatie: str
    Omschrijving: str
    OpenstaandeActie: str
    OpenstaandeActieGuid: str


class ReactionItemPayload(TypedDict, total=False):
    Publicatie_Portaal: ListingPayload
    ReactieV11: ReactionPayload


class ReactionsPayload(TypedDict, total=False):
    Response: OSListPayload[ReactionItemPayload]
    Result: ResultPayload


class PointsCategoryPayload(TypedDict, total=False):
    Aantal: float
    Tekstregel1: str
    Tekstregel2: str


class TimedPointsCategoryPayload(PointsCategoryPayload, total=False):
    Begindatum: str
    Einddatum: str
    Verlengdatum: str
    Tonen: bool


class SearchPointsMonthPayload(TypedDict, total=False):
    Maand: int
    Aantal: int
    MinAantal: int
    Tekstregel1: str


class SearchPointsPayload(PointsCategoryPayload, total=False):
    LstReacties: OSListPayload[SearchPointsMonthPayload]


class PointsDashboardPayload(TypedDict, total=False):
    Naam: str
    OvereenkomstBegindatum: str
    RelatieContextId: int
    Totaalpunten: PointsCategoryPayload
    Wachtpunten: PointsCategoryPayload
    Zoekpunten: SearchPointsPayload
    Situatiepunten: TimedPointsCategoryPayload
    Startpunten: TimedPointsCategoryPayload


class PointsPayload(TypedDict, total=False):
    Puntendashboardoverzicht: OSListPayload[PointsDashboardPayload]
    Result: ResultPayload


class WoonwensPayload(TypedDict, total=False):
    Id: str
    MinHuurprijs: float
    MaxHuurprijs: float
    MinKamers: int
    MaxKamers: int
    MinOppervlakte: float
    MaxOppervlakte: float
    LaatstGewijzigdOp: str


class NamedEntityPayload(TypedDict, total=False):
    """Generic ``{Id, Naam}`` lookup record (places, districts, housing types)."""

    Id: str
    Naam: str
    Code: str


class DistrictPayload(NamedEntityPayload, total=False):
    WoonplaatsId: str


class PlaceWithDistrictsPayload(TypedDict, total=False):
    Woonplaats: NamedEntityPayload
    WijkenLijst: OSListPayload[DistrictPayload]


class HousingTypeGroupPayload(TypedDict, total=False):
    EenheidDetailsoortGroep: NamedEntityPayload
    EenheidDetailsoortLijst: OSListPayload[NamedEntityPayload]


class AccessibilityPayload(TypedDict, total=False):
    ToegankelijkheidId: str
    Code: str
    Naam: str
    LaatstGewijzigdOp: str


class NavigationLocationPayload(TypedDict, total=False):
    Id: str
    WoonWensWizardId: str
    WoonWensNavigatieTypeId: int
    Straatnaam: str
    Huisnummer: int
    HuisnummerToevoeging: str
    Postcode: str
    WoonplaatsNaam: str


class NavigationTypePayload(TypedDict, total=False):
    Id: int
    Label: str
    Icon: str
    Order: int
    Is_Active: bool


class NavigationOptionPayload(TypedDict, total=False):
    WoonWensNavigatieOpties: NavigationLocationPayload
    WoonWensNavigatieType: NavigationTypePayload


class WishesPayload(TypedDict, total=False):
    Woonwens: WoonwensPayload
    WoonplaatsenMetWijkenLijst: OSListPayload[PlaceWithDistrictsPayload]
    WoonTypeMetSubWoonTypesLijst: OSListPayload[HousingTypeGroupPayload]
    ToegankelijkheidLijst: OSListPayload[AccessibilityPayload]
    WoonWensNavigatieOpties: OSListPayload[NavigationOptionPayload]
