from __future__ import annotations

from typing import TypedDict

from ..common import OSListPayload, ResultPayload

__all__ = (
    "AddressPayload",
    "ClusterPayload",
    "DescriptionPayload",
    "ListingPayload",
    "ListingsPayload",
    "SavedAndHiddenPayload",
    "UnitPayload",
)


class AddressPayload(TypedDict, total=False):
    Straatnaam: str
    Huisnummer: int
    Huisletter: str
    HuisnummerToevoeging: str
    Postcode: str
    Woonplaats: str
    Wijk: str
    PublicatieId: str


class UnitPayload(TypedDict, total=False):
    """``Eenheid``: the dwelling itself."""

    DetailSoort: str
    Bestemming: str
    AantalKamers: int
    TotaleOppervlakte: str
    WoonVertrekkenTotOpp: str
    Doelgroep: str
    NettoHuurBekend: bool
    NettoHuur: str
    BrutoHuurBekend: bool
    Brutohuur: str
    SubsidiabeleHuur: str
    Lengtegraad: str
    Breedtegraad: str
    Toegankelijkheid: str
    Toegankelijkheidstag: str
    SoortBouw: str
    EnergieLabel: str
    EnergieIndex: float
    Eigenaar: str


class ClusterPayload(TypedDict, total=False):
    """Set of units published as one listing (new-build projects)."""

    Naam: str
    DetailSoort: str
    Doelgroep: str
    AantalEenheden: int
    AantalKamersMin: int
    AantalKamersMax: int
    PrijsMin: str
    PrijsMax: str
    Eigenaar: str


class DescriptionPayload(TypedDict, total=False):
    Id: str
    Tekst: str


class ListingPayload(TypedDict, total=False):
    Id: str
    EinddatumTijd: str
    PublicatieDatum: str
    PublicatieModel: str
    PublicatieModule: str
    PublicatieLabel: str
    Foto_Locatie: str
    Matchpercentage: float
    VoorlopigePositie: str
    Slaagkans: float
    GepersonaliseerdeHuur: str
    IsCluster: bool
    EenheidSoort: str
    Adres: AddressPayload
    Eenheid: UnitPayload
    Cluster: ClusterPayload
    ContractVorm: str
    PublicatieOmschrijving: DescriptionPayload
    IsBewaard: bool
    IsVerborgen: bool
    HeeftGereageerd: bool
    IsIntrekkenReactieToegestaan: bool
    RedenNietIntrekkenReactie: str
    AantalReactiesOpPublicatie: str
    PositieAanbiedingsproces: str
    VirtuelePositie: int
    Opleverdatum: str
    HeeftLift: bool
    Verdieping: str
    AanbiedingProcesSoort: str


class ListingsPayload(TypedDict, total=False):
    PublicatieLijst: OSListPayload[ListingPayload]
    Result: ResultPayload
    InschrijvingId: str


class SavedAndHiddenPayload(TypedDict, total=False):
    FavorietenLijst: OSListPayload[ListingPayload]
    FavorietenResult: ResultPayload
    VerborgenLijst: OSListPayload[ListingPayload]
    VerborgenResult: ResultPayload
