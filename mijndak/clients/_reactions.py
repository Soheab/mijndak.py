from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import ReactionsResponse

if TYPE_CHECKING:
    from ..http import HTTPClient
    from ..models import ActionResult, ReactionItem
    from ._client import Client


class ReactionsClient:
    """Methods for viewing, placing and withdrawing reactions to listings.

    Use it through :attr:`Client.reactions` instead of creating it directly.

    Parameters
    ----------
    parent: :class:`Client`
        The client this belongs to.
    """

    def __init__(self, parent: Client, /) -> None:
        self._parent: Client = parent
        self.__http: HTTPClient = parent.http

    async def current(self) -> list[ReactionItem]:
        """The account's reactions to listings that are still open.

        Returns
        -------
        list[:class:`ReactionItem`]
            Each reaction together with its listing.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return ReactionsResponse(await self.__http.get_current_reactions(), self.__http).reactions

    async def ongoing(self) -> list[ReactionItem]:
        """The account's reactions to listings that have closed and are being allocated.

        Returns
        -------
        list[:class:`ReactionItem`]
            Each reaction together with its listing.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return ReactionsResponse(await self.__http.get_ongoing_reactions(), self.__http).reactions

    async def past(self) -> list[ReactionItem]:
        """The account's reactions to listings that have already been allocated.

        Returns
        -------
        list[:class:`ReactionItem`]
            Each reaction together with its listing.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return ReactionsResponse(await self.__http.get_past_reactions(), self.__http).reactions

    async def react(self, publication_id: int) -> ActionResult:
        """React to a listing.

        **This places a real reaction on the account.**

        Parameters
        ----------
        publication_id: :class:`int`
            The listing's ID.

        Returns
        -------
        :class:`ActionResult`
            Check :attr:`ActionResult.is_success` to see whether it worked.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return await self._parent.listings.partial(publication_id).react()

    async def withdraw(self, publication_id: int) -> ActionResult:
        """Withdraw the account's reaction to a listing.

        Parameters
        ----------
        publication_id: :class:`int`
            The listing's ID.

        Returns
        -------
        :class:`ActionResult`
            Check :attr:`ActionResult.is_success` to see whether it worked.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return await self._parent.listings.partial(publication_id).withdraw_reaction()
