from __future__ import annotations

from typing import NotRequired, TypedDict

from ..actions import ActionInputs

__all__ = (
    "AggregateInputs",
    "ClientVariables",
    "DataActionPayload",
    "EmptyVariables",
    "ScreenData",
    "ServerActionPayload",
    "VersionInfoPayload",
)


class VersionInfoPayload(TypedDict):
    moduleVersion: str
    apiVersion: str


class ClientVariables(TypedDict, total=False):
    """Client variables the server reads from the request (stored in localStorage by the real site).

    ``SamenwerkingsverbandId`` and ``SamenwerkingsverbandCode`` are required for nearly every call.
    """

    SamenwerkingsverbandId: str
    SamenwerkingsverbandCode: str
    SamenwerkingsverbandNaam: str
    SWVConfiguratie: str
    Weergave_Sortering: str
    Weergave_SorteringIsAflopend: str
    Weergave_GebruikWoonwensFilter: str
    Weergave_Filters: str
    IsUitgebreidZoeken: str


class EmptyVariables(TypedDict):
    """Screen variables for data actions that don't read any screen state."""


class ScreenData(TypedDict):
    variables: EmptyVariables | dict[str, object]


class AggregateInputs(TypedDict):
    StartIndex: int
    MaxRecords: int


class DataActionPayload(TypedDict):
    versionInfo: VersionInfoPayload
    viewName: str
    screenData: ScreenData
    clientVariables: ClientVariables
    inputParameters: NotRequired[AggregateInputs]


class ServerActionPayload(TypedDict):
    versionInfo: VersionInfoPayload
    viewName: str
    inputParameters: ActionInputs
    clientVariables: ClientVariables
