from __future__ import annotations

from typing import TYPE_CHECKING, Final

if TYPE_CHECKING:
    from .._types import ActionInputs

__all__ = ("DataAction", "ServerAction", "view_name_for")

EP: Final = "screenservices/DAKWP"
EP_CW: Final = "screenservices/DAKWP_CW"
EP_REUSABLE: Final = "screenservices/DAKReusable_CW"


def view_name_for(path: str) -> str:
    """``screenservices/DAKWP/Overzicht/WoningOverzicht/DataActionX`` → ``Overzicht.WoningOverzicht``."""
    return ".".join(path.split("/")[2:-1])


class DataAction[T]:
    """A read: ``DataAction*`` or, with ``page_size``, a ``ScreenDataSet*`` aggregate.

    ``payload`` is the type the response's ``data`` is decoded and validated as.
    """

    __slots__ = ("page_size", "path", "payload", "view")

    def __init__(self, path: str, payload: type[T], *, view: str | None = None, page_size: int | None = None) -> None:
        self.path: Final = path
        self.payload: Final = payload
        #: The screen the call is made from; web-block actions need their parent screen for role validation.
        self.view: Final = view
        #: ``MaxRecords`` for aggregates; ``None`` for plain data actions.
        self.page_size: Final = page_size

    @property
    def view_name(self) -> str:
        return self.view or view_name_for(self.path)


class ServerAction[I: ActionInputs, T]:
    """A mutating ``Action*`` with typed input parameters."""

    __slots__ = ("inputs", "path", "payload", "view")

    def __init__(self, path: str, inputs: type[I], payload: type[T], *, view: str | None = None) -> None:
        self.path: Final = path
        self.inputs: Final = inputs
        self.payload: Final = payload
        self.view: Final = view

    @property
    def view_name(self) -> str:
        return self.view or view_name_for(self.path)
