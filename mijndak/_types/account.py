from __future__ import annotations

from typing import TypedDict

from .common import LongInteger, OSListPayload, ResultPayload

__all__ = (
    "AccountStatusPayload",
    "CodeNamePayload",
    "ConfigurationPayload",
    "ConfigurationResponsePayload",
    "ContactDetailsPayload",
    "CurrentHousingPayload",
    "CurrentHousingResponsePayload",
    "DataSharingPayload",
    "DisplayPreferencesPayload",
    "DisplayPreferencesResponsePayload",
    "DocumentPayload",
    "DocumentTypePayload",
    "DocumentsPayload",
    "HouseholdPayload",
    "HouseholdResponsePayload",
    "IncomePayload",
    "LinkPayload",
    "MFADetailsPayload",
    "OpenPaymentPayload",
    "PaymentInformationPayload",
    "PaymentPayload",
    "PaymentsPayload",
    "PersonDocumentsPayload",
    "PersonPayload",
    "PersonalDetailsPayload",
    "PointsLinePayload",
    "PointsLineTypePayload",
    "PointsLinesPayload",
    "PriorityFlagPayload",
    "PriorityRulePayload",
    "PrioritySchemesPayload",
    "PrioritySetItemPayload",
    "PrioritySetPayload",
    "PrioritySetsPayload",
    "ProfilePanelPayload",
    "RegistrationItemPayload",
    "RegistrationPayload",
    "SubscriptionPayload",
    "SubscriptionsPayload",
    "VSHIncomePayload",
    "WoonadresPayload",
)


class WoonadresPayload(TypedDict, total=False):
    Id: LongInteger
    Straatnaam: str
    Huisnummer: int
    HuisnummerToevoeging: str
    Postcode: str
    WoonplaatsCode: str
    WoonplaatsNaam: str
    BuurtCode: str
    BuurtNaam: str
    WijkCode: str
    WijkNaam: str
    GemeenteCode: str
    GemeenteNaam: str
    ProvincieCode: str
    ProvincieNaam: str
    LandCode: str
    LandNaam: str


class ContactDetailsPayload(TypedDict, total=False):
    Emailadres: str
    EmailadresStatusCode: str
    EmailadresCC: str
    EmailadresCCStatusCode: str
    EmailadresBackup: str
    EmailadresBackupStatusCode: str
    Telefoonnummer: str
    TelefoonnummerStatusCode: str
    Telefoonnummer2: str
    Telefoonnummer2StatusCode: str


class IncomePayload(TypedDict, total=False):
    BrutoJaarinkomen: float
    Bron: str
    InkomensverklaringCode: str
    Inkomensverklaring: str
    Mutatiedatum: str
    Jaar: int
    Omschrijving: str
    Inkomensdocumenten: str
    MoetGewijzigd: bool
    KeuzeBronInkomen: str


class VSHIncomePayload(TypedDict, total=False):
    """Income used for mid-rent (``vrije sector huur``) eligibility."""

    Jaar: int
    Bedrag: float
    InkomenBekend: bool


class PersonPayload(TypedDict, total=False):
    """``NatuurlijkPersoon``: an applicant or household member."""

    NatuurlijkPersoonId: LongInteger
    Voorletters: str
    Tussenvoegsel: str
    Achternaam: str
    Roepnaam: str
    Geslacht: str
    Geboortedatum: str
    GebruikgegevensOenA: bool
    Inschrijfdatum: str
    GecorrigeerdeInschrijfdatum: str
    HeeftGevalideerdePersoonsgegevens: bool
    HeeftGevalideerdWoonadres: bool
    HeeftGevalideerdInkomen: bool
    IsInkomenSociaalOK: bool
    IsInkomenVshOK: bool
    Woonadres: WoonadresPayload
    Contactgegevens: ContactDetailsPayload
    Inkomen: IncomePayload
    InkomenVSH: VSHIncomePayload


class LinkPayload(TypedDict, total=False):
    """Link with an external organisation (e.g. Woonmatch)."""

    OrganisatieKoppeling: str
    StatusKoppeling: str
    BegindatumKoppeling: str


class PersonalDetailsPayload(TypedDict, total=False):
    NatuurlijkPersoonGegevens: PersonPayload
    ResultHuisHouden: ResultPayload
    IsQiiVerwerkt: bool
    ResultQii: ResultPayload
    WoonmatchKoppeling: LinkPayload
    IsVrijeSectorInschrijving: bool


class ConfigurationPayload(TypedDict, total=False):
    SamenwerkingsverbandId: LongInteger
    Inschrijfkosten: str
    Verlengingsfkosten: str
    MinimaleLeeftijdInMaanden: int
    HeeftVrijeSector: bool


class ConfigurationResponsePayload(TypedDict, total=False):
    IsValiderenBeschikbaar: bool
    Configuratie: ConfigurationPayload


class PriorityFlagPayload(TypedDict, total=False):
    HeeftVoorrangsregelingen: bool


class HouseholdPayload(TypedDict, total=False):
    NatuurlijkPersoonId: LongInteger
    Gebruikersnaam: str
    RelatiegroepId: LongInteger
    AantalVolwassenen: int
    AantalKinderen: int
    VerzamelInkomen: float
    VerzamelInkomenVSH: float
    HeeftVerzamelInkomenVSH: bool
    IsVerwijderenMedeaanvragerToegestaan: bool
    IsHuishoudenDeelsGevalideerd: bool
    IsHuishoudenVolledigGevalideerd: bool
    Hoofdaanvrager: PersonPayload
    Medeaanvrager: PersonPayload
    OverigeVolwassenen: OSListPayload[PersonPayload]
    Kinderen: OSListPayload[PersonPayload]


class _HouseholdWrapperPayload(TypedDict, total=False):
    Huishouden: HouseholdPayload
    OvereenkomstKoppeling: LinkPayload


class HouseholdResponsePayload(TypedDict, total=False):
    Huishouden: _HouseholdWrapperPayload
    ResultHuishouden: ResultPayload
    IsQiiVerwerkt: bool
    ResultQii: ResultPayload
    QiiHandmatigAanpassen: bool


class CodeNamePayload(TypedDict, total=False):
    Code: str
    Naam: str


class _OwnerPayload(TypedDict, total=False):
    VestigingId: LongInteger
    VestigingNaam: str


class CurrentHousingPayload(TypedDict, total=False):
    EigenaarVestiging: _OwnerPayload
    EenheidDetailsoort: CodeNamePayload
    KamersAantal: int
    TotaleOppervlakte: str
    Etage: int
    LaatZelfstandigEenheidAchter: bool
    Overeenkomstsoort: CodeNamePayload
    OvereenkomstDetailSoort: CodeNamePayload
    SocialehuurIndicator: CodeNamePayload
    OvereenkomstBedrag: float
    OvereenkomstBegindatum: str
    BRPInschrijfdatum: str


class _CurrentHousingWrapperPayload(TypedDict, total=False):
    HuidigeWoonsituatie: CurrentHousingPayload
    lstOvereenkomstDetailSoort: OSListPayload[CodeNamePayload]


class CurrentHousingResponsePayload(TypedDict, total=False):
    Response: _CurrentHousingWrapperPayload
    Result: ResultPayload


class PriorityRulePayload(TypedDict, total=False):
    VoorrangDetailSoort: CodeNamePayload
    VoorrangSubDetailSoort: CodeNamePayload
    Naam: str
    Omschrijving: str
    Begindatum: str
    Einddatum: str
    IsActief: bool
    IsWijzigbaar: bool
    IsToegewezen: bool


class PrioritySetPayload(TypedDict, total=False):
    Id: LongInteger
    Naam: str
    Omschrijving: str
    IsExclusief: bool
    IsZichtbaarVoorWozo: bool
    IsWijzigbaarDoorWozo: bool
    IsIngangsdatumWijzigbaarDoorWozo: bool
    Voorrangsregelingen: OSListPayload[PriorityRulePayload]


class PrioritySetItemPayload(TypedDict, total=False):
    VoorrangsregelingenSets: PrioritySetPayload


class PrioritySetsPayload(TypedDict, total=False):
    Urgentie: OSListPayload[PrioritySetItemPayload]
    Indicatie: OSListPayload[PrioritySetItemPayload]
    Binding: OSListPayload[PrioritySetItemPayload]
    Groep: OSListPayload[PrioritySetItemPayload]


class PrioritySchemesPayload(TypedDict, total=False):
    Voorrangsregelingen: PrioritySetsPayload
    Result: ResultPayload


class ProfilePanelPayload(TypedDict, total=False):
    ProfielPanelenId: int
    WeerTeGevenNaam: str
    WRBNaam: str
    WRBOmschrijving: str
    IsCompleet: bool
    BinnenkortBeschikbaar: bool


class AccountStatusPayload(TypedDict, total=False):
    ProfielPanelenVisualisatieList: OSListPayload[ProfilePanelPayload]
    QiiInProfiel: bool
    Result: ResultPayload


class OpenPaymentPayload(TypedDict, total=False):
    OpenstaandeBetaling: bool
    HeeftBetalingInBehandeling: bool
    Bedrag: str
    IsVerlengingsKosten: bool
    IsBetaaldeVerlenging: bool


class PaymentPayload(TypedDict, total=False):
    Id: LongInteger
    BetaalperiodeBeginDatum: str
    BetaalperiodeEindDatum: str
    Bedrag: str
    Betaalwijze: str
    VerzoekVerzondenDatumTijd: str
    BetalingVerwerktDatumTijd: str
    BuckarooFactuurNummer: str
    BetaalStatusCode: str
    BetaalStatus: str
    Omschrijving: str


class PaymentInformationPayload(TypedDict, total=False):
    VolgendeFactuurdatum: str
    Betaalwijze: str
    Betalingen: OSListPayload[PaymentPayload]


class PaymentsPayload(TypedDict, total=False):
    BetaalInformatie: PaymentInformationPayload
    Result: ResultPayload


class DocumentPayload(TypedDict, total=False):
    DocumentId: LongInteger
    Titel: str
    Documentnaam: str
    Mimetype: str
    OntvangstDatumTijd: str
    Status: str


class DocumentTypePayload(TypedDict, total=False):
    BenodigdheidCode: str
    BenodigdheidNaam: str
    Documenten: OSListPayload[DocumentPayload]


class PersonDocumentsPayload(TypedDict, total=False):
    NatuurlijkPersoonId: LongInteger
    HeeftInkomenDocument: bool
    Documenttypes: OSListPayload[DocumentTypePayload]


class DocumentsPayload(TypedDict, total=False):
    HoofdAanvragerDocumenten: OSListPayload[PersonDocumentsPayload]
    MedeaanvragerDocumenten: OSListPayload[PersonDocumentsPayload]
    OverigeVolwassenenDocumenten: OSListPayload[PersonDocumentsPayload]
    ResultDocument: ResultPayload
    Huishouden: _HouseholdWrapperPayload
    ResultHuishouden: ResultPayload


class SubscriptionPayload(TypedDict, total=False):
    SoortCode: str
    Naam: str
    Email: str
    IsGeabonneerd: bool


class SubscriptionsPayload(TypedDict, total=False):
    Abonnementen: OSListPayload[SubscriptionPayload]
    Result: ResultPayload


class DataSharingPayload(TypedDict, total=False):
    #: Item shape unknown: the list was empty on the account it was captured from.
    Gegevensdeling: OSListPayload[dict[str, object]]
    Result: ResultPayload


class PointsLineTypePayload(TypedDict, total=False):
    Code: str
    Naam: str
    Datum: str
    Begindatum: str
    Tekstregel1: str
    Tekstregel2: str
    Zoekpunten: float
    Situatiepunten: float
    Startpunten: float
    Icoon: int


class PointsLinePayload(TypedDict, total=False):
    Soort: PointsLineTypePayload


class _PointsTabPayload(TypedDict, total=False):
    RelatieContextId: int
    PuntenContextId: int
    TabbladContextId: int
    LstItems: OSListPayload[PointsLinePayload]


class PointsLinesPayload(TypedDict, total=False):
    Puntendashboardregels: OSListPayload[_PointsTabPayload]
    Result: ResultPayload


class RegistrationPayload(TypedDict, total=False):
    Id: LongInteger
    UserId: int
    NatuurlijkPersoonId: LongInteger
    SamenwerkingsverbandId: LongInteger
    NatuurlijkPersoon: LongInteger
    Samenwerkingsverband: LongInteger
    IsActiefSamenwerkingsverband: bool
    VerloopDatum: str
    ProductCode: str
    Hoofdaanvrager: LongInteger


class RegistrationItemPayload(TypedDict, total=False):
    Inschrijving: RegistrationPayload


class MFADetailsPayload(TypedDict, total=False):
    IsActief_VoorGebruiker: bool
    IsActief_MFA: bool


class DisplayPreferencesPayload(TypedDict, total=False):
    Id: LongInteger
    UserId: int
    IsVerbergenVraagNietWeer: bool
    IsDAKP: bool
    IsDAK: bool
    IsKaartVerborgen: bool
    IsUitgebreidZoeken: bool
    IsWoonwensFilter: bool
    LaatsteInlog: str
    LaatsteReview: str
    IsMijnOverheidVraagNietWeer: bool
    IsTelValidatieNietMeerTonen: bool
    IsAppDownloadVraagNietWeer: bool


class DisplayPreferencesResponsePayload(TypedDict, total=False):
    Voorkeuren: DisplayPreferencesPayload
