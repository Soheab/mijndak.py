from typing import Required, TypedDict

from .common import OSListPayload, ResultPayload


class EmptyInputs(TypedDict):
    pass


class EmptyResponse(TypedDict):
    pass


class WizardRegistrationPayload(TypedDict, total=False):
    Id: str
    UserId: int
    NatuurlijkPersoonId: str
    SamenwerkingsverbandId: str
    NatuurlijkPersoon: str
    Samenwerkingsverband: str
    IsActiefSamenwerkingsverband: bool
    VerloopDatum: str
    ProductCode: str
    Hoofdaanvrager: str


class WizardWishPayload(TypedDict, total=False):
    Id: Required[str]
    SamenwerkingsverbandId: str
    NatuurlijkPersoonId: str
    MinKamers: int
    MaxKamers: int
    MinHuurprijs: int
    MaxHuurprijs: int
    MinOppervlakte: int
    MaxOppervlakte: int
    LaatstGewijzigdOp: str


class WizardPayload(TypedDict, total=False):
    Woonwens: Required[WizardWishPayload]
    WoonwensId: str
    Inschrijving: Required[WizardRegistrationPayload]


class MinimumWishInputs(TypedDict):
    MinimaalAantal: int
    WoonwensWizardId: str


class MaximumWishInputs(TypedDict):
    MaximaalAantal: int
    WoonwensWizardId: str


class RecalculateWishesInputs(TypedDict):
    Inschrijving: WizardRegistrationPayload
    WoonwensFilterIsEis: bool


class WishReferencePayload(TypedDict, total=False):
    WoonplaatsId: str
    WijkId: str
    EenheidDetailsoortGroepId: str
    EenheidDetailsoortId: str
    ToegankelijkheidId: str
    Naam: str
    Code: str


class WishSelectionPayload(TypedDict, total=False):
    Id: str
    WoonWensWizardId: str
    WoonplaatsId: str
    WijkId: str
    EenheidDetailsoortGroepId: str
    EenheidDetailsoortId: str
    ToegankelijkheidId: str


class WishOptionPayload(TypedDict, total=False):
    IsSelected: bool
    Woonplaats: WishReferencePayload
    Wijk: WishReferencePayload
    EenheidDetailsoortGroep: WishReferencePayload
    EenheidDetailsoort: WishReferencePayload
    Toegankelijkheid: WishReferencePayload
    WoonWensWoonplaats: WishSelectionPayload
    WoonWensWijk: WishSelectionPayload
    EenheidDetailsoortGroepWoonwens: WishSelectionPayload
    EenheidDetailsoortWoonwens: WishSelectionPayload
    ToegankelijkheidWoonwens: WishSelectionPayload


class CityWishInputs(TypedDict):
    ActieveWoonplaatsen: list[WishSelectionPayload]
    InactieveWoonplaatsen: list[WishSelectionPayload]
    WoonwenswizardId: str


class DistrictWishInputs(TypedDict):
    ActieveWoonwensWijk: list[WishSelectionPayload]
    InactieveWoonwensWijk: list[WishSelectionPayload]


class RemoveCityWishInputs(TypedDict):
    WoonplaatsId: str
    WoonwensId: str


class HousingTypeWishInputs(TypedDict):
    ActieveWoontype: list[WishSelectionPayload]
    InactieveWoontype: list[WishSelectionPayload]
    WoonwenswizardId: str


class HousingSubtypeWishInputs(TypedDict):
    ActieveWoonsubtype: list[WishSelectionPayload]
    InactieveWoonsubtype: list[WishSelectionPayload]


class AccessibilityWishInputs(TypedDict):
    ActieveToegankelijkheid: list[WishSelectionPayload]
    WoonwensWizardId: str


class MFASetupPayload(TypedDict, total=False):
    IsActief: bool
    QRcode: str
    IsSuccess: bool
    IsSuccessReden: str
    HeeftDeAppNogNiet: bool
    DeeplinkEnvironment: str


class MFACodeInputs(TypedDict):
    InvoerCode: str


class MFAResultPayload(TypedDict, total=False):
    IsSuccess: bool
    IsSuccessReden: str


class MFADevicePayload(TypedDict, total=False):
    DatumTijdAangemaakt: str
    DatumTijdGekoppeld: str
    DatumTijdGeactiveerd: str
    DatumTijdDeactivatieGestart: str
    DatumTijdGedeactiveerd: str
    DeviceName: str
    LastLogin: str
    IsActief: bool


class MFAStatusPayload(TypedDict, total=False):
    MFADetails: MFADevicePayload
    HeeftBackupEmailadres: bool
    EmailadresGebruikt: str


class MFABackupInputs(TypedDict):
    InvoerCode: str
    NatuurlijkPersoonId: str
    SamenwerkingsVerbandId: str


class BankPayload(TypedDict, total=False):
    Code: str
    Naam: str


class BanksPayload(TypedDict, total=False):
    Banken: OSListPayload[BankPayload]
    ErrorMessage: str


class PaymentActionPayload(TypedDict, total=False):
    Id: int
    Naam: str
    Omschrijving: str
    VolgordeNummer: int
    IsActief: bool


class PaymentActionListPayload(TypedDict, total=False):
    BetaalActies: OSListPayload[PaymentActionPayload]
    Banken: OSListPayload[BankPayload]


class PaymentOptionsPayload(BanksPayload, total=False):
    BetaalActies: PaymentActionListPayload


class StartPaymentInputs(TypedDict):
    NatuurlijkPersoonId: str
    SamenwerkingsverbandId: str
    BetaalActieId: str
    BankCode: str
    GUID: str


class PaymentRedirectPayload(TypedDict, total=False):
    Result: ResultPayload
    BetaalURL: str
    StatusMessage: str


class MandateInputs(TypedDict):
    BankCodeLocal: str
    SamenwerkingsverbandId: str
    Natuurlijkpersoonid: str


class MandateRedirectPayload(TypedDict, total=False):
    BetaalUrl: str
    Statusmessage: str


class MandateStatusInputs(TypedDict):
    GUID: str


class MandateStatusPayload(TypedDict, total=False):
    Status: str
    UserId: int
