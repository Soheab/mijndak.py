from __future__ import annotations

from typing import Final

from .._types import LoginInputs, LogoutInputs
from .base import EP, ServerAction

__all__ = ("Auth",)


class Auth:
    # Their output isn't used; ``object`` accepts whatever the server sends.
    LOGIN: Final = ServerAction(f"{EP}/Inloggen/Inloggen/ActionLoginServer", LoginInputs, object)
    # The menu is a web block, so the call needs a screen it sits on for DAK's role check.
    LOGOUT: Final = ServerAction(f"{EP}/Common/Menu/ActionDoLogout", LogoutInputs, object, view="Profiel.Persoonsgegevens")
