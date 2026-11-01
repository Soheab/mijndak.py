from __future__ import annotations

from typing import Final

from .._types import (
    AccountStatusPayload,
    ActionResultPayload,
    AggregatePayload,
    ChangePasswordInputs,
    ChangePasswordPayload,
    ConfigurationResponsePayload,
    CurrentHousingResponsePayload,
    DataSharingPayload,
    DeleteDocumentInputs,
    DisplayPreferencesInputs,
    DisplayPreferencesResponsePayload,
    DocumentsPayload,
    HouseholdResponsePayload,
    MFADetailsPayload,
    MutationResultPayload,
    OfferDisplayInputs,
    OpenPaymentPayload,
    PaymentsPayload,
    PersonalDetailsPayload,
    PersonResultPayload,
    PointsCounterInputs,
    PointsLinesPayload,
    PriorityFlagPayload,
    PrioritySchemesPayload,
    RegistrationItemPayload,
    RemovePersonInputs,
    SaveBindingsInputs,
    SaveGroupsInputs,
    SaveIndicationsInputs,
    SetDataSharingInputs,
    SetSubscriptionInputs,
    SubscriptionsPayload,
    UpdateCurrentHousingInputs,
    UpdatePersonInputs,
    UploadDocumentInputs,
    UserItemPayload,
    WishesFilterInputs,
)
from .._types.account import HouseholdRoleItemPayload
from .base import EP, EP_REUSABLE, DataAction, ServerAction

__all__ = ("Account", "Settings")

_PROFILE: Final = f"{EP}/Profiel"
_PROFILE_CW: Final = f"{EP_REUSABLE}/Profiel_CW"
_SETTINGS: Final = f"{EP}/Instellingen"
_PRIORITY: Final = f"{EP_REUSABLE}/Profiel_CW_Voorrangsregelingen/VoorrangsregelingenSetWijzigen_CW"
_DOCUMENTS: Final = f"{EP_REUSABLE}/Profiel_CW_Documenten"


class Account:
    HOUSEHOLD_ROLES: Final = DataAction(
        f"{_PROFILE}/NatuurlijkPersoonToevoegenOfWijzigen/ScreenDataSetGetRelatieRolSoortCodes",
        AggregatePayload[HouseholdRoleItemPayload],
        page_size=100,
    )
    PERSONAL_DETAILS: Final = DataAction(
        f"{_PROFILE}/Persoonsgegevens/DataActionHaalPersoonsgegevensEnQii", PersonalDetailsPayload
    )
    CONFIGURATION: Final = DataAction(
        f"{_PROFILE}/Persoonsgegevens/DataActionHaalConfiguratie", ConfigurationResponsePayload
    )
    HAS_PRIORITY_SCHEMES: Final = DataAction(
        f"{_PROFILE}/Persoonsgegevens/DataActionHaalActiefVoorrangsregelingen", PriorityFlagPayload
    )
    HOUSEHOLD: Final = DataAction(f"{_PROFILE}/HuishoudenEnInkomen/DataActionHaalHuishoudenEnQii", HouseholdResponsePayload)
    CURRENT_HOUSING: Final = DataAction(
        f"{_PROFILE}/HuidigeWoonsituatie/DataActionHaalHuidigeWoonsituatie", CurrentHousingResponsePayload
    )
    PRIORITY_SCHEMES: Final = DataAction(
        f"{_PROFILE}/Voorrangsregelingen/DataActionHaalVoorrangsregelingen", PrioritySchemesPayload
    )
    STATUS: Final = DataAction(
        f"{_PROFILE}/ProfielPanelenMetData/DataActionHaalAccountStatusEnZichtbareVelden",
        AccountStatusPayload,
        view="Profiel.Persoonsgegevens",
    )
    OPEN_PAYMENT: Final = DataAction(f"{_PROFILE}/BetaalInformatie/DataActionBepaalOpenstaandeBetaling", OpenPaymentPayload)
    PAYMENTS: Final = DataAction(
        f"{_PROFILE_CW}/BetaalInformatie_CW/DataActionHaalBetaalInformatie",
        PaymentsPayload,
        view="Profiel.BetaalInformatie",
    )
    DOCUMENTS: Final = DataAction(
        f"{EP_REUSABLE}/Profiel_CW_Documenten/Documenten_CW/DataActionHaalAlleDocumentenEnHuishouden",
        DocumentsPayload,
        view="Profiel.Documenten",
    )
    SUBSCRIPTIONS: Final = DataAction(
        f"{_PROFILE_CW}/PersoonlijkeBerichten_CW/DataActionHaalAbonnementen",
        SubscriptionsPayload,
        view="Profiel.PersoonlijkeBerichten",
    )
    DATA_SHARING: Final = DataAction(
        f"{_PROFILE_CW}/Gegevensdeling_CW/DataActionHaalGegevensdeling",
        DataSharingPayload,
        view="Profiel.Gegevensdeling",
    )
    POINTS_LINES: Final = DataAction(f"{EP}/Woonpunten/PuntenOverzicht/DataActionHaalPuntenRegels", PointsLinesPayload)

    USER: Final = DataAction(
        f"{_PROFILE}/WB_Persoonsgegevens/ScreenDataSetGetUserById",
        AggregatePayload[UserItemPayload],
        view="Profiel.Persoonsgegevens",
        page_size=1,
    )

    # writes
    UPDATE_PERSONAL_DETAILS: Final = ServerAction(
        f"{_PROFILE}/PersoonsgegevensWijzigen/ActionNatuurlijkPersoonVerwerken",
        UpdatePersonInputs,
        PersonResultPayload,
    )
    UPDATE_HOUSEHOLD_MEMBER: Final = ServerAction(
        f"{_PROFILE_CW}/NatuurlijkPersoonToevoegenOfWijzigen_CW/ActionNatuurlijkPersoonVerwerken",
        UpdatePersonInputs,
        PersonResultPayload,
        view="Profiel.NatuurlijkPersoonToevoegenOfWijzigen",
    )
    REMOVE_HOUSEHOLD_MEMBER: Final = ServerAction(
        f"{_PROFILE_CW}/HuishoudenCardGroup/ActionNatuurlijkPersoonVerwijder",
        RemovePersonInputs,
        MutationResultPayload,
        view="Profiel.HuishoudenEnInkomen",
    )
    UPDATE_CURRENT_HOUSING: Final = ServerAction(
        f"{_PROFILE_CW}/WoonSituatieWijzigen_CW/ActionHuidigeWoonSituatieVerwerk_V1_2",
        UpdateCurrentHousingInputs,
        MutationResultPayload,
        view="Profiel.HuidigeWoonsituatieWijzigen",
    )
    SET_SUBSCRIPTION: Final = ServerAction(
        f"{_PROFILE_CW}/PersoonlijkeBerichten_CW/ActionAbonnementenVerwerk2",
        SetSubscriptionInputs,
        ActionResultPayload,
        view="Profiel.PersoonlijkeBerichten",
    )
    SET_DATA_SHARING: Final = ServerAction(
        f"{_PROFILE_CW}/Gegevensdeling_CW/ActionGegevensdelingVerwerk",
        SetDataSharingInputs,
        ActionResultPayload,
        view="Profiel.Gegevensdeling",
    )
    SAVE_BINDINGS: Final = ServerAction(
        f"{_PRIORITY}/ActionBindingenOpslaan",
        SaveBindingsInputs,
        ActionResultPayload,
        view="Profiel.VoorrangsregelingenSetWijzigen",
    )
    SAVE_GROUPS: Final = ServerAction(
        f"{_PRIORITY}/ActionGroepenOpslaan",
        SaveGroupsInputs,
        ActionResultPayload,
        view="Profiel.VoorrangsregelingenSetWijzigen",
    )
    SAVE_INDICATIONS: Final = ServerAction(
        f"{_PRIORITY}/ActionIndicatiesOpslaan",
        SaveIndicationsInputs,
        ActionResultPayload,
        view="Profiel.VoorrangsregelingenSetWijzigen",
    )
    UPLOAD_DOCUMENT: Final = ServerAction(
        f"{_DOCUMENTS}/DocumentToevoegen_CW/ActionDocumentToevoegen_Lokaal",
        UploadDocumentInputs,
        ActionResultPayload,
        view="Profiel.DocumentToevoegen",
    )
    DELETE_DOCUMENT: Final = ServerAction(
        f"{_DOCUMENTS}/DocumentlijstWeergaveSub/ActionDocumentVerwijder",
        DeleteDocumentInputs,
        ActionResultPayload,
        view="Profiel.Documenten",
    )


class Settings:
    REGISTRATIONS: Final = DataAction(
        f"{_SETTINGS}/InstellingenOverzicht/ScreenDataSetHaalInschrijvingInSWV",
        AggregatePayload[RegistrationItemPayload],
        page_size=50,
    )
    MFA: Final = DataAction(f"{_SETTINGS}/InstellingenOverzicht/DataActionHaalMFADetails", MFADetailsPayload)
    DISPLAY_PREFERENCES: Final = DataAction(
        f"{_SETTINGS}/WeergaveKaart/DataActionHaalVoorkeuren", DisplayPreferencesResponsePayload
    )

    # writes
    CHANGE_PASSWORD: Final = ServerAction(
        f"{_SETTINGS}/WijzigWachtwoord/ActionWijzigWachtwoord", ChangePasswordInputs, ChangePasswordPayload
    )
    SET_DISPLAY_PREFERENCES: Final = ServerAction(
        f"{_SETTINGS}/WeergaveKaart/ActionCreateUpdateWeergaveEnKaart",
        DisplayPreferencesInputs,
        ActionResultPayload,
    )
    SET_OFFER_END_DATE_DISPLAY: Final = ServerAction(
        f"{EP_REUSABLE}/Instellingen_CW/WeergaveAanbod_CW/ActionVerwerkAanbodWeergave",
        OfferDisplayInputs,
        ActionResultPayload,
        view="Instellingen.WeergaveAanbod",
    )
    SET_FILTER_BY_WISHES: Final = ServerAction(
        f"{EP}/Overzicht/WoningOverzicht/ActionUpdateVoorkeurWoonwensFilter", WishesFilterInputs, ActionResultPayload
    )
    SET_POINTS_COUNTER: Final = ServerAction(
        f"{EP_REUSABLE}/Instellingen_CW/WeergavePuntenteller_CW/ActionVerwerkOpstartenPuntenoverzicht",
        PointsCounterInputs,
        ActionResultPayload,
        view="Instellingen.WeergavePuntenteller",
    )
