from __future__ import annotations

from .actions import Result
from .base import Items, Model, Nested, field
from .listings.models import Listing

__all__ = ("Reaction", "ReactionItem", "ReactionsResponse")


class Reaction(Model):
    """The state of one of the account's reactions.

    Attributes
    ----------
    listing_id: :class:`str` | :data:`None`
        The listing's ID. (*publicatie id*)
    allocation_id: :class:`str` | :data:`None`
        The ID of the allocation. (*aanbieding id*)
    allocation_status: :class:`str` | :data:`None`
        The status of the allocation. (*aanbieding status*)
    allocation_detail_status: :class:`str` | :data:`None`
        The detailed status of the allocation. (*aanbieding detailstatus*)
    status: :class:`str` | :data:`None`
        The status of the reaction. (*reactie status*)
    kind: :class:`str` | :data:`None`
        The kind of reaction. (*reactie soort*)
    position: :class:`int` | :data:`None`
        The account's position among the candidates. (*reactie positie*)
    allocation_stage: :class:`str` | :data:`None`
        The stage the allocation is in. (*positie aanbiedingsproces*)
    reaction_count: :class:`str` | :data:`None`
        The number of reactions to the listing, as a string. (*aantal reacties op publicatie*)
    description: :class:`str` | :data:`None`
        A description of the reaction's state. (*omschrijving*)
    pending_action: :class:`str` | :data:`None`
        An action the account still has to take, such as uploading documents. (*openstaande actie*)
    pending_action_id: :class:`str` | :data:`None`
        The ID of the action the account still has to take. (*openstaande actie guid*)
    """

    listing_id = field(str, "PublicatieId")
    allocation_id = field(str, "AanbiedingId")
    allocation_status = field(str, "AanbiedingStatus")
    allocation_detail_status = field(str, "AanbiedingDetailstatus")
    status = field(str, "ReactieStatus")
    kind = field(str, "ReactieSoort")
    position = field(int, "ReactiePositie")
    allocation_stage = field(str, "PositieAanbiedingsproces")
    reaction_count = field(str, "AantalReactiesOpPublicatie")
    description = field(str, "Omschrijving")
    pending_action = field(str, "OpenstaandeActie")
    pending_action_id = field(str, "OpenstaandeActieGuid")


class ReactionItem(Model):
    """One of the account's reactions, together with its listing.

    Attributes
    ----------
    listing: :class:`Listing`
        The listing reacted to. (*publicatie portaal*)
    reaction: :class:`Reaction`
        The state of the reaction. (*reactie v 11*)
    """

    listing = Nested(Listing, "Publicatie_Portaal")
    reaction = Nested(Reaction, "ReactieV11")


class ReactionsResponse(Model):
    """A list of the account's reactions.

    Attributes
    ----------
    reactions: list[:class:`ReactionItem`]
        The reactions, each with its listing.
    result: :class:`Result`
        Whether DAK handled the request successfully.
    """

    reactions = Items(ReactionItem, "Response")
    result = Nested(Result, "Result")
