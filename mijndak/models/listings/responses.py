from __future__ import annotations

from ..actions import Result
from ..base import Items, Model, Nested, field
from .models import Listing

__all__ = ("ListingsResponse", "SavedAndHiddenResponse")


class ListingsResponse(Model):
    """A list of listings.

    Attributes
    ----------
    listings: list[:class:`Listing`]
        The listings. (*publicatie lijst*)
    result: :class:`Result`
        Whether DAK handled the request successfully.
    registration_id: :class:`str` | :data:`None`
        The ID of the registration the list was made for. (*inschrijving id*)
    """

    listings = Items(Listing, "PublicatieLijst")
    result = Nested(Result, "Result")
    registration_id = field(str, "InschrijvingId")


class SavedAndHiddenResponse(Model):
    """The listings the account saved or hid.

    Attributes
    ----------
    saved: list[:class:`Listing`]
        The saved listings. (*favorieten lijst*)
    saved_result: :class:`Result`
        Whether fetching the saved listings succeeded. (*favorieten result*)
    hidden: list[:class:`Listing`]
        The hidden listings. (*verborgen lijst*)
    hidden_result: :class:`Result`
        Whether fetching the hidden listings succeeded. (*verborgen result*)
    """

    saved = Items(Listing, "FavorietenLijst")
    saved_result = Nested(Result, "FavorietenResult")
    hidden = Items(Listing, "VerborgenLijst")
    hidden_result = Nested(Result, "VerborgenResult")
