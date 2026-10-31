from __future__ import annotations

from typing import TypedDict

from ..common import LongInteger

__all__ = ("LoginInputs", "LogoutInputs")


class LoginInputs(TypedDict):
    Gebruikersnaam: str
    Wachtwoord: str
    IsIngelogdBlijven: bool
    SwvClient: LongInteger
    ReturnUrl: str
    ClientInputLastUrl: str
    WoningAanbodPublicatie: str
    IsVanContactformulier: bool
    IsKlantContactCode: bool
    RequestId_In: LongInteger
    Request_In: str


class LogoutInputs(TypedDict):
    pass
