from __future__ import annotations

from typing import TypedDict

from ..common import LongInteger

__all__ = ("HideInputs", "PublicationInputs", "ReactInputs", "SaveInputs")


class PublicationInputs(TypedDict):
    PublicatieId: LongInteger
    SamenwerkingsverbandId: LongInteger


class ReactInputs(PublicationInputs):
    ToonMijNietMeer: bool


class SaveInputs(PublicationInputs):
    IsBewaren: bool


class HideInputs(PublicationInputs):
    IsVerbergen: bool
