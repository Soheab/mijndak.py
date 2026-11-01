from typing import Final

from .._types.common import AggregatePayload
from .._types.flows import (
    AccessibilityWishInputs,
    BanksPayload,
    CityWishInputs,
    DistrictWishInputs,
    EmptyInputs,
    EmptyResponse,
    HousingSubtypeWishInputs,
    HousingTypeWishInputs,
    MandateInputs,
    MandateRedirectPayload,
    MandateStatusInputs,
    MandateStatusPayload,
    MaximumWishInputs,
    MFABackupInputs,
    MFACodeInputs,
    MFAResultPayload,
    MFASetupPayload,
    MFAStatusPayload,
    MinimumWishInputs,
    PaymentOptionsPayload,
    PaymentRedirectPayload,
    RecalculateWishesInputs,
    RemoveCityWishInputs,
    StartPaymentInputs,
    WishOptionPayload,
    WizardPayload,
)
from .base import EP, EP_CW, EP_REUSABLE, DataAction, ServerAction

_WIZARD: Final = f"{EP}/Wizard"
_MFA: Final = f"{EP_CW}/MultiFactorAuthentication"
_PAY: Final = f"{EP_REUSABLE}/Inschrijven_CW/Betalen_CW"
_MANDATE: Final = f"{EP}/Profiel/MachtigingAfgeven"


class HousingWishes:
    WIZARD: Final = DataAction(f"{_WIZARD}/Kamers/DataActionHaalWizard", WizardPayload)
    MINIMUM_ROOMS: Final = ServerAction(f"{_WIZARD}/Kamers/ActionKamersMinimaalOpslaan", MinimumWishInputs, EmptyResponse)
    MAXIMUM_RENT: Final = ServerAction(
        f"{_WIZARD}/Huurprijs/ActionHuurprijsMaximaalOpslaan", MaximumWishInputs, EmptyResponse
    )
    MINIMUM_AREA: Final = ServerAction(
        f"{_WIZARD}/Afmeting/ActionOppervlakteMinimaalOpslaan", MinimumWishInputs, EmptyResponse
    )
    RECALCULATE: Final = ServerAction(
        f"{_WIZARD}/Samenvatting/ActionBerekenMatchPercentagePassendAanbodEnFilter", RecalculateWishesInputs, EmptyResponse
    )
    CITIES: Final = DataAction(
        f"{_WIZARD}/Locatie/ScreenDataSetAlleWoonplaatsen", AggregatePayload[WishOptionPayload], page_size=10000
    )
    DISTRICTS: Final = DataAction(
        f"{_WIZARD}/Wijken/ScreenDataSetHaalWijken", AggregatePayload[WishOptionPayload], page_size=10000
    )
    TYPES: Final = DataAction(
        f"{_WIZARD}/WoningType/ScreenDataSetAlleWoningtypes", AggregatePayload[WishOptionPayload], page_size=10000
    )
    SUBTYPES: Final = DataAction(
        f"{_WIZARD}/WoningSubType/ScreenDataSetHaalSubtype", AggregatePayload[WishOptionPayload], page_size=10000
    )
    ACCESSIBILITY: Final = DataAction(
        f"{_WIZARD}/Toegankelijkheid/ScreenDataSetGetToegankelijkheid", AggregatePayload[WishOptionPayload], page_size=10000
    )
    SET_CITIES: Final = ServerAction(f"{_WIZARD}/Locatie/ActionWoonplaatsenOpslaan", CityWishInputs, EmptyResponse)
    SET_DISTRICTS: Final = ServerAction(f"{_WIZARD}/Wijken/ActionWijkenOpslaan", DistrictWishInputs, EmptyResponse)
    REMOVE_CITY: Final = ServerAction(
        f"{_WIZARD}/Wijken/ActionWijken_GeenActiefUpdateWoonplaats", RemoveCityWishInputs, EmptyResponse
    )
    SET_TYPES: Final = ServerAction(f"{_WIZARD}/WoningType/ActionWoontypeOpslaan", HousingTypeWishInputs, EmptyResponse)
    SET_SUBTYPES: Final = ServerAction(
        f"{_WIZARD}/WoningSubType/ActionWoonSubtypeOpslaan", HousingSubtypeWishInputs, EmptyResponse
    )
    SET_ACCESSIBILITY: Final = ServerAction(
        f"{_WIZARD}/Toegankelijkheid/ActionToegankelijkheidOpslaan", AccessibilityWishInputs, EmptyResponse
    )


class MFA:
    SETUP: Final = DataAction(f"{EP}/Instellingen/MultiFactorAuthenticatie/DataActionHaalMFADetails", MFASetupPayload)
    ACTIVATE: Final = ServerAction(
        f"{_MFA}/MFA_KoppelstappenWeb/ActionActiveerNaInvoerenCode",
        MFACodeInputs,
        MFAResultPayload,
        view="Instellingen.MultiFactorAuthenticatie",
    )
    STATUS: Final = DataAction(
        f"{_MFA}/MFA_Gekoppeldpagina/DataActionGetMFADetails", MFAStatusPayload, view="Instellingen.MultiFactorAuthenticatie"
    )
    REQUEST_DEACTIVATION: Final = ServerAction(
        f"{_MFA}/MFA_Gekoppeldpagina/ActionTriggerDeactivatieViaDevice",
        EmptyInputs,
        MFAResultPayload,
        view="Instellingen.MultiFactorAuthenticatie",
    )
    DEACTIVATE: Final = ServerAction(
        f"{_MFA}/MFA_Gekoppeldpagina/ActionDeactiveerMFA",
        MFACodeInputs,
        MFAResultPayload,
        view="Instellingen.MultiFactorAuthenticatie",
    )
    BACKUP_DEACTIVATE: Final = ServerAction(
        f"{_MFA}/MFA_ViaBackupEmail/ActionDeactiveerMFAViaBackupCode",
        MFABackupInputs,
        MFAResultPayload,
        view="Instellingen.MultiFactorAuthenticatie",
    )


class Payments:
    OPTIONS: Final = DataAction(f"{_PAY}/DataActionHaalBetaalActies", PaymentOptionsPayload, view="Inschrijven.Betalen")
    START: Final = ServerAction(
        f"{_PAY}/ActionBetalenActie", StartPaymentInputs, PaymentRedirectPayload, view="Inschrijven.Betalen"
    )
    BANKS: Final = DataAction(f"{_MANDATE}/DataActionHaalBanken", BanksPayload)
    START_MANDATE: Final = ServerAction(f"{_MANDATE}/ActionBetaalgegevensAanpassen", MandateInputs, MandateRedirectPayload)
    MANDATE_STATUS: Final = ServerAction(
        f"{EP}/Profiel/MachtigingAfgevenReturn/ActionGUIDNaarStatusEnId", MandateStatusInputs, MandateStatusPayload
    )
