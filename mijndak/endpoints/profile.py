from __future__ import annotations

from typing import Final

from .._types import PointsPayload, WishesPayload
from .base import EP, DataAction

__all__ = ("Profile",)


class Profile:
    POINTS: Final = DataAction(f"{EP}/Woonpunten/PuntenOverzicht/DataActionHaalPuntenInfo", PointsPayload)
    HOUSING_WISHES: Final = DataAction(f"{EP}/Profiel/WoonwensOverzicht/DataActionHaalWoonwensInformatie", WishesPayload)
