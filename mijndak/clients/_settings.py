from __future__ import annotations

from typing import TYPE_CHECKING

from ..models import ActionResult, DisplayPreferences, MFADetails, PasswordChangeResult, Registration, User
from ..models.base import records

if TYPE_CHECKING:
    from ..http import HTTPClient
    from ._client import Client


class SettingsClient:
    """Methods for account settings (*instellingen*).

    Use it through :attr:`Client.settings` instead of creating it directly. Every method requires the
    client to be logged in and raises :class:`~mijndak.errors.NotLoggedInError` otherwise.

    Parameters
    ----------
    parent: :class:`Client`
        The client this belongs to.
    """

    def __init__(self, parent: Client, /) -> None:
        self._parent: Client = parent
        self.__http: HTTPClient = parent.http

    async def user(self) -> User | None:
        """The account's login details.

        Returns
        -------
        :class:`User` | :data:`None`
            The username, e-mail address, creation date and last login, or :data:`None` if DAK returned no
            account.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        items = records(await self.__http.get_user())
        return User(items[0].get("User") or {}, self.__http) if items else None

    async def registrations(self) -> list[Registration]:
        """The account's registrations (*inschrijvingen*) in this region.

        Returns
        -------
        list[:class:`Registration`]
            Each registration with its product code and expiry date.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        data = await self.__http.get_registrations()
        return [Registration(item.get("Inschrijving") or {}, self.__http) for item in records(data)]

    async def mfa_details(self) -> MFADetails:
        """Whether multi-factor authentication is available and turned on.

        Returns
        -------
        :class:`MFADetails`
            Whether multi-factor authentication is available and whether it is turned on.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return MFADetails(await self.__http.get_mfa_details(), self.__http)

    async def display_preferences(self) -> DisplayPreferences:
        """The account's display preferences, such as whether the map is hidden.

        Returns
        -------
        :class:`DisplayPreferences`
            The preferences, such as whether the map is hidden and extended search is used.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        data = await self.__http.get_display_preferences()
        return DisplayPreferences(data.get("Voorkeuren") or {}, self.__http)

    async def change_password(self, old_password: str, new_password: str) -> PasswordChangeResult:
        """Change the account's password.

        Parameters
        ----------
        old_password: :class:`str`
            The current password.
        new_password: :class:`str`
            The new password. It must meet DAK's password requirements.

        Returns
        -------
        :class:`PasswordChangeResult`
            Whether the current password was correct and whether the change succeeded.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return PasswordChangeResult(await self.__http.change_password(old_password, new_password), self.__http)

    async def set_display_preferences(
        self, *, hide_map: bool | None = None, extended_search: bool | None = None
    ) -> ActionResult:
        """Change the account's map and search preferences.

        This fetches the current preferences first, so any option left as :data:`None` keeps its current value.

        Parameters
        ----------
        hide_map: :class:`bool`, optional
            Whether to hide the map in the listings overview.
        extended_search: :class:`bool`, optional
            Whether to use extended search.

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
        current = await self.display_preferences()
        data = await self.__http.set_display_preferences(
            is_dak=current.is_dak,
            hide_map=current.is_map_hidden if hide_map is None else hide_map,
            extended_search=current.uses_extended_search if extended_search is None else extended_search,
        )
        return ActionResult(data, self.__http)

    async def set_offer_end_date_display(self, show: bool) -> ActionResult:
        """Choose whether listings show their closing date instead of the time left.

        Parameters
        ----------
        show: :class:`bool`
            :data:`True` to show the closing date.

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
        return ActionResult(await self.__http.set_offer_end_date_display(show), self.__http)

    async def set_filter_by_wishes(self, enabled: bool) -> ActionResult:
        """Choose whether the listings overview shows only homes that match the account's housing wishes.

        This is the *woonwensen* switch at the top of the website's filter panel. The website remembers it for the
        account; its other filters are only kept in the browser, so use :class:`~mijndak.ListingFilters` for those.

        Parameters
        ----------
        enabled: :class:`bool`
            :data:`True` to show only matching homes.

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
        return ActionResult(await self.__http.set_filter_by_wishes(enabled), self.__http)

    async def set_points_counter(self, start_on_points_overview: bool) -> ActionResult:
        """Choose whether the website opens the points overview after logging in.

        Parameters
        ----------
        start_on_points_overview: :class:`bool`
            :data:`True` to open the points overview after logging in.

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
        return ActionResult(await self.__http.set_points_counter(start_on_points_overview), self.__http)
