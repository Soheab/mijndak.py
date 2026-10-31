from __future__ import annotations

from typing import Final

from .._types import ActionResultPayload, PublicationInputs, ReactInputs, ReactionsPayload
from .base import EP, DataAction, ServerAction
from .details import VIEW

__all__ = ("Reactions",)

_OVERVIEW: Final = f"{EP}/Reacties/ReactieOverzicht"
_ACTIONS: Final = f"{EP}/HuisDetails/InHetKortEnPositie"


class Reactions:
    CURRENT: Final = DataAction(f"{_OVERVIEW}/DataActionActueleReactiesHaal", ReactionsPayload)
    ONGOING: Final = DataAction(f"{_OVERVIEW}/DataActionLopendeReactiesHaal", ReactionsPayload)
    PAST: Final = DataAction(f"{_OVERVIEW}/DataActionHistorischeReactiesHaal", ReactionsPayload)
    REACT: Final = ServerAction(f"{_ACTIONS}/ActionVerwerkReactie", ReactInputs, ActionResultPayload, view=VIEW)
    WITHDRAW: Final = ServerAction(f"{_ACTIONS}/ActionReactieIntrekken", PublicationInputs, ActionResultPayload, view=VIEW)
