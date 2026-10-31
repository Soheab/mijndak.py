from __future__ import annotations

from typing import TypedDict

from .account import CurrentHousingPayload, PersonPayload, PrioritySetPayload, SubscriptionPayload
from .common import LongInteger, ResultPayload

__all__ = (
    "ChangePasswordInputs",
    "ChangePasswordPayload",
    "DataSharingConsentPayload",
    "DeleteDocumentInputs",
    "DisplayPreferencesInputs",
    "MutationResultPayload",
    "OfferDisplayInputs",
    "PersonResultPayload",
    "PointsCounterInputs",
    "RemovePersonInputs",
    "SaveBindingsInputs",
    "SaveGroupsInputs",
    "SaveIndicationsInputs",
    "SetDataSharingInputs",
    "SetSubscriptionInputs",
    "UpdateCurrentHousingInputs",
    "UpdatePersonInputs",
    "UploadDocumentInputs",
    "UserItemPayload",
    "UserPayload",
    "WishesFilterInputs",
)


class UpdatePersonInputs(TypedDict):
    Locale: str
    NatuurlijkPersoon: PersonPayload
    #: The person's role in the household (``RelatieRolSoortCode``), e.g. main or co-applicant.
    RelatieRolSoortCodeId: int
    SamenwerkingsverbandId: LongInteger


class RemovePersonInputs(TypedDict):
    Locale: str
    NatuurlijkPersoonId: LongInteger
    SamenwerkingsverbandId: LongInteger


class UpdateCurrentHousingInputs(TypedDict):
    HuidigeWoonsituatie: CurrentHousingPayload


class SetSubscriptionInputs(TypedDict):
    Locale: str
    Abonnement: SubscriptionPayload
    SamenwerkingsverbandId: LongInteger


class DataSharingConsentPayload(TypedDict):
    ToestemmingId: LongInteger
    IsToestemmingVerleend: bool


class SetDataSharingInputs(TypedDict):
    Locale: str
    SamenwerkingsverbandId: LongInteger
    Gegevensdeling: list[DataSharingConsentPayload]


class SaveBindingsInputs(TypedDict):
    SamenwerkingsverbandId: LongInteger
    Bindingen: PrioritySetPayload


class SaveGroupsInputs(TypedDict):
    SamenwerkingsverbandId: LongInteger
    Groepen: PrioritySetPayload


class SaveIndicationsInputs(TypedDict):
    SamenwerkingsverbandId: LongInteger
    Indicaties: PrioritySetPayload


class UploadDocumentInputs(TypedDict):
    #: File contents, base64-encoded (OutSystems ``BinaryData``).
    Document: str
    SamenwerkingsverbandId: LongInteger
    NatuurlijkPersoonId: LongInteger
    DocumentNaam: str
    Titel: str
    MimeType: str
    #: ``BenodigdheidCode`` of the document type, from :class:`DocumentTypePayload`.
    DocumentSoortCode: str


class DeleteDocumentInputs(TypedDict):
    Locale: str
    SamenwerkingsverbandId: LongInteger
    NatuurlijkpersoonId: LongInteger
    DocumentId: LongInteger


class ChangePasswordInputs(TypedDict):
    OudWachtwoord: str
    NieuwWachtwoord: str
    SamenwerkingsverbandId: LongInteger


class DisplayPreferencesInputs(TypedDict):
    IsDAK: bool
    IsKaartVerbergen: bool
    IsUitgebreidZoeken: bool


class WishesFilterInputs(TypedDict):
    IsWoonwensFilterByDefault: bool


class OfferDisplayInputs(TypedDict):
    IsWeergaveEinddatum: bool


class PointsCounterInputs(TypedDict):
    IsOpstartenPuntenoverzicht: bool


class MutationResultPayload(TypedDict, total=False):
    Result: ResultPayload
    #: Message shown after the change, e.g. that it must be re-validated.
    ProfielMutatieMelding: str


class PersonResultPayload(MutationResultPayload, total=False):
    Response: PersonPayload
    Melding: str


class ChangePasswordPayload(TypedDict, total=False):
    IsOudWachtwoordValid: bool
    IsSuccesWijzig: bool


class UserPayload(TypedDict, total=False):
    """The login account (OutSystems ``User``); ``Password`` is always sent empty."""

    Id: int
    Name: str
    Username: str
    Email: str
    MobilePhone: str
    External_Id: str
    Creation_Date: str
    Last_Login: str
    Is_Active: bool


class UserItemPayload(TypedDict, total=False):
    User: UserPayload
