from __future__ import annotations

from typing import TypedDict

from .account_inputs import (
    ChangePasswordInputs,
    DeleteDocumentInputs,
    DisplayPreferencesInputs,
    OfferDisplayInputs,
    PointsCounterInputs,
    RemovePersonInputs,
    SaveBindingsInputs,
    SaveGroupsInputs,
    SaveIndicationsInputs,
    SetDataSharingInputs,
    SetSubscriptionInputs,
    UpdateCurrentHousingInputs,
    UpdatePersonInputs,
    UploadDocumentInputs,
    WishesFilterInputs,
)
from .auth.inputs import LoginInputs, LogoutInputs
from .common import ResultPayload
from .listings.inputs import HideInputs, PublicationInputs, ReactInputs, SaveInputs

__all__ = ("ActionInputs", "ActionResultPayload")

type ActionInputs = (
    LoginInputs
    | LogoutInputs
    | PublicationInputs
    | ReactInputs
    | SaveInputs
    | HideInputs
    | UpdatePersonInputs
    | RemovePersonInputs
    | UpdateCurrentHousingInputs
    | SetSubscriptionInputs
    | SetDataSharingInputs
    | SaveBindingsInputs
    | SaveGroupsInputs
    | SaveIndicationsInputs
    | UploadDocumentInputs
    | DeleteDocumentInputs
    | ChangePasswordInputs
    | DisplayPreferencesInputs
    | OfferDisplayInputs
    | PointsCounterInputs
    | WishesFilterInputs
)


class ActionResultPayload(TypedDict, total=False):
    """``{"Result": {IsSuccess, StatusCode, ErrorMessage}}``."""

    Result: ResultPayload
