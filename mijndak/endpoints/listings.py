from __future__ import annotations

from typing import Final

from .._types import ActionResultPayload, HideInputs, ListingsPayload, SavedAndHiddenPayload, SaveInputs
from .base import EP, EP_CW, DataAction, ServerAction

__all__ = ("Listings",)

_OVERVIEW: Final = f"{EP}/Overzicht"
_CARD: Final = f"{EP_CW}/Overzicht/HuisBlock"
#: The listing card is a web block, so its actions need a screen it sits on for DAK's role check.
_CARD_VIEW: Final = "Overzicht.Favorieten"


class Listings:
    MATCHING: Final = DataAction(f"{_OVERVIEW}/WoningOverzicht/DataActionHaalPassendAanbod", ListingsPayload)
    NON_MATCHING: Final = DataAction(
        f"{_OVERVIEW}/WoningOverzichtNietPassend/DataActionHaalNietPassendAanbod", ListingsPayload
    )
    PUBLIC: Final = DataAction(f"{_OVERVIEW}/Woningaanbod/DataActionHaalUitgelogdAanbod", ListingsPayload)
    SAVED_AND_HIDDEN: Final = DataAction(
        f"{_OVERVIEW}/Favorieten/DataActionHaalFavorietenEnVerborgen", SavedAndHiddenPayload
    )
    SET_SAVED: Final = ServerAction(
        f"{_CARD}/ActionPublicatieBewarenWijzigen", SaveInputs, ActionResultPayload, view=_CARD_VIEW
    )
    SET_HIDDEN: Final = ServerAction(
        f"{_CARD}/ActionPublicatieVerborgenWijzigen", HideInputs, ActionResultPayload, view=_CARD_VIEW
    )
