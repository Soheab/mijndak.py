from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import Listing, ListingDetail, ListingsResponse, PartialListing, SavedAndHiddenResponse

if TYPE_CHECKING:
    from ..http import HTTPClient
    from ._client import Client


class ListingsClient:
    """Housing listings (*woningaanbod*).

    Use it through :attr:`Client.listings` instead of creating it directly.

    Parameters
    ----------
    parent: :class:`Client`
        The client this belongs to.
    """

    def __init__(self, parent: Client, /) -> None:
        self._parent: Client = parent
        self.__http: HTTPClient = parent.http

    async def public(self) -> list[Listing]:
        """All current listings, as shown to visitors who are not logged in.

        This does not require logging in.

        Returns
        -------
        list[:class:`Listing`]
            Every listing that is currently open for reactions.

        Raises
        ------
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return ListingsResponse(await self.__http.get_public_listings(), self.__http).listings

    async def matching(self) -> list[Listing]:
        """Listings the account qualifies for.

        Returns
        -------
        list[:class:`Listing`]
            Each listing with how well it matches the account and the account's provisional position.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return ListingsResponse(await self.__http.get_matching_listings(), self.__http).listings

    async def non_matching(self) -> list[Listing]:
        """Listings the account does not qualify for.

        Returns
        -------
        list[:class:`Listing`]
            Each listing, with the same details as :meth:`matching`.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return ListingsResponse(await self.__http.get_non_matching_listings(), self.__http).listings

    async def saved_and_hidden(self) -> SavedAndHiddenResponse:
        """The listings the account has saved or hidden.

        Returns
        -------
        :class:`SavedAndHiddenResponse`
            Saved listings in ``saved`` and hidden listings in ``hidden``.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return SavedAndHiddenResponse(await self.__http.get_saved_and_hidden(), self.__http)

    def partial(self, publication_id: int) -> PartialListing:
        """A listing with only its ID, for calling its methods without fetching it first.

        This makes no request. Call :meth:`PartialListing.fetch` to get the full listing.

        Parameters
        ----------
        publication_id: :class:`int`
            The listing's ID.

        Returns
        -------
        :class:`PartialListing`
            The listing, with only its ID filled in.
        """
        return PartialListing(publication_id, self.__http)

    async def fetch(self, publication_id: int) -> ListingDetail | None:
        """Fetch the full details of one listing.

        Parameters
        ----------
        publication_id: :class:`int`
            The listing's ID.

        Returns
        -------
        :class:`ListingDetail` | :data:`None`
            The listing, its home, address and building complex, or :data:`None` if the listing does not exist.

        Raises
        ------
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return await self.partial(publication_id).fetch()
