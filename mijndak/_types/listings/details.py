from __future__ import annotations

from typing import TypedDict

from ..common import OSListPayload, ResultPayload

__all__ = (
    "ApplicantPayload",
    "CriterionPayload",
    "DetailAddressPayload",
    "DetailClusterPayload",
    "DetailPublicationPayload",
    "DetailUnitPayload",
    "EligibilityPayload",
    "EligibilityRulePayload",
    "EnrolmentInformationPayload",
    "FacilityPayload",
    "FileItemPayload",
    "FilePayload",
    "HousingCostsPayload",
    "HousingCostsResponsePayload",
    "ListingDetailPayload",
    "ListingExtrasPayload",
    "PriceComponentPayload",
    "RankingRulePayload",
    "RoomPayload",
)


class DetailPublicationPayload(TypedDict, total=False):
    PublicatieId: str
    SamenwerkingsverbandId: str
    AantalEenhedenBeschikbaar: int
    BeginDatumTijd: str
    EindDatumTijd: str
    ContractVorm: str
    SpelregelSet: str
    Looptijd: str
    OpleverDatum: str
    ContractEindDatum: str
    PublicatieLabel: str
    PublicatieStatus: str
    PublicatieDetailStatus: str
    MetGepersonaliseerdeHuur: bool
    AdvertentieURL: str
    PublicatieModel: str
    PublicatieModule: str
    Oplevering: str
    AanbiedingProcesSoort: str
    IsPassendVoorIedereen: bool
    HeeftKandidatenLijst: bool


class DetailUnitPayload(TypedDict, total=False):
    Code: str
    Naam: str
    Omschrijving: str
    EenheidSoort: str
    DetailSoort: str
    EenheidStatus: str
    Eigenaar: str
    EtageBekend: bool
    Etage: int
    AantalKamers: int
    TotaleOppervlakte: str
    WoonVertrekkenTotOpp: str
    OverigeVertrekkenTotOppervla: str
    Bestemming: str
    Doelgroep: str
    AanvullendeDoelgroep: str
    Woonvorm: str
    IsZelfstandig: bool
    HeeftLift: bool
    OpleverDatum: str
    BrutoHuurBekend: bool
    BrutoHuur: str
    NettoHuurBekend: bool
    NettoHuur: str
    SubsidiabeleHuur: str
    IsNieuwbouw: bool
    EnergieLabel: str
    Lengtegraad: str
    Breedtegraad: str
    Toegankelijkheid: str


class DetailAddressPayload(TypedDict, total=False):
    Straatnaam: str
    Huisnummer: int
    Huisletter: str
    HuisnummerToevoeging: str
    Postcode: str
    Gemeente: str
    Woonplaats: str
    Wijk: str
    Buurt: str


class DetailClusterPayload(TypedDict, total=False):
    Naam: str
    BasisPublicatieTekst: str
    DetailSoort: str
    Eigenaar: str
    AantalEenheden: int
    AantalKamersMin: int
    AantalKamersMax: int
    PrijsMin: str
    PrijsMax: str


class ListingDetailPayload(TypedDict, total=False):
    Publicatie: DetailPublicationPayload
    Eenheid: DetailUnitPayload
    Adres: DetailAddressPayload
    Cluster: DetailClusterPayload


class FilePayload(TypedDict, total=False):
    """``Bestand``: a photo, floor plan or other download."""

    Id: str
    Titel: str
    Beschrijving: str
    Formaat: str
    Soort: str
    DetailSoort: str
    Primair: bool
    Volgordenummer: int
    Bestandsgrootte: int
    Bestandslocatie: str


class FileItemPayload(TypedDict, total=False):
    Bestand: FilePayload


class PriceComponentPayload(TypedDict, total=False):
    PrijscomponentSoort: str
    PrijscomponentDetailsoort: str
    Bedrag: str
    BedragBekend: bool


class CriterionPayload(TypedDict, total=False):
    Label: str
    Omschrijving: str


class RankingRulePayload(TypedDict, total=False):
    VolgordeNummer: int
    OmschrijvingWoonPortaal: str
    Waarde: bool


class ApplicantPayload(TypedDict, total=False):
    NatuurlijkPersoonId: str


class EnrolmentInformationPayload(TypedDict, total=False):
    PublicatieKandidaatSorteerTekst: OSListPayload[RankingRulePayload]
    IsPassendVoorKandidaat: bool | None


class EligibilityRulePayload(TypedDict, total=False):
    Label: str
    Omschrijving: str
    IsPassend: bool


class EligibilityPayload(TypedDict, total=False):
    UitlegLijst: OSListPayload[EligibilityRulePayload]
    IsGeenRedenGevonden: bool


class RoomPayload(TypedDict, total=False):
    Naam: str
    RuimteSoort: str
    Oppervlakte: str


class FacilityPayload(TypedDict, total=False):
    Soort: str
    DetailSoort: str
    Waarde: str


class _HtmlTextPayload(TypedDict, total=False):
    Tekst: str


class _ConditionsPayload(TypedDict, total=False):
    Voorwaarden: str


class ListingExtrasPayload(TypedDict, total=False):
    PrijsComponenten: OSListPayload[PriceComponentPayload]
    SorteerCriteriaList: OSListPayload[CriterionPayload]
    SelectieCriteriaList: OSListPayload[CriterionPayload]
    VertrekkenList: OSListPayload[RoomPayload]
    PublicatieVoorwaarden: _ConditionsPayload
    VoorzieningList: OSListPayload[FacilityPayload]
    PublicatieTekst: _HtmlTextPayload


class HousingCostsPayload(TypedDict, total=False):
    """``WoonlastenProfiel``: estimated monthly costs. Mostly empty unless the region enables it."""

    Huur: str
    Huursubsidie: str
    Servicekosten: str
    TotaleEnergielasten: str
    TotaleWoonlasten: str
    Betaalbaarheidscore: float


class HousingCostsResponsePayload(TypedDict, total=False):
    WoonlastenProfiel: HousingCostsPayload
    OphalenGelukt: ResultPayload
