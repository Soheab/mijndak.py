from __future__ import annotations

from typing import TYPE_CHECKING

from ..errors import AuthenticationError, HTTPError, MFARequiredError, NotLoggedInError, ServerError

if TYPE_CHECKING:
    from ..http import HTTPClient, SessionCookie
    from ._client import Client


class AuthClient:
    """Methods for logging in and out, and for saving and restoring the session.

    Use it through :attr:`Client.auth` instead of creating it directly.

    Parameters
    ----------
    parent: :class:`Client`
        The client this belongs to.
    """

    def __init__(self, parent: Client, /) -> None:
        self._parent: Client = parent
        self.__http: HTTPClient = parent.http

    async def login(self, username: str, password: str, *, remember: bool = False) -> None:
        """Log in with an e-mail address or username and a password.

        Parameters
        ----------
        username: :class:`str`
            The account's e-mail address or username.
        password: :class:`str`
            The account's password. It is only sent to DAK and is never stored.
        remember: :class:`bool`, optional
            Whether to ask DAK for a longer-lasting session ("ingelogd blijven", stay logged in). Defaults to
            :data:`False`.

        Raises
        ------
        :class:`AuthenticationError`
            The username or password is wrong, or DAK did not return a session cookie.
        :class:`MFARequiredError`
            The login must be approved in the DAK app. Approve it, then call :meth:`login` again.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        try:
            await self.__http.login(username, password, remember=remember)
        except ServerError as exc:
            message = exc.message or exc.name or "Login failed"
            error_cls = MFARequiredError if "MFA" in message.upper() else AuthenticationError
            raise error_cls(message) from exc

        if not self.__http.is_authenticated():
            raise AuthenticationError("Login returned no session cookie")

    def export_session(self) -> list[SessionCookie]:
        """Export the session cookies so the session can be restored later.

        Anyone with these cookies has full access to the account, so store them securely, for example
        encrypted.

        Returns
        -------
        list[:class:`SessionCookie`]
            The cookies, which can be saved as JSON, each with the time it expires.
        """
        return self.__http.export_session()

    def restore_session(self, cookies: list[SessionCookie]) -> None:
        """Restore cookies from :meth:`export_session`.

        This does not check whether the session is still valid; call :meth:`refresh_session` to check.

        Parameters
        ----------
        cookies: list[:class:`SessionCookie`]
            Cookies previously returned by :meth:`export_session`.

        Raises
        ------
        :exc:`ValueError`
            A cookie belongs to another region.
        """
        self.__http.restore_session(cookies)

    async def refresh_session(self) -> bool:
        """Check that the session is still logged in.

        This makes a request that only works when logged in, and keeps any new cookies DAK sends back.
        It does not log in again and never repeats an earlier change to the account.

        Returns
        -------
        :class:`bool`
            :data:`True` if the session is logged in.

        Raises
        ------
        :class:`HTTPError`
            The request failed for a reason other than the session having expired.
        :class:`ServerError`
            DAK returned an error.
        """
        try:
            await self.__http.get_points()
        except NotLoggedInError:
            return False
        except HTTPError as exc:
            if exc.status == 401:
                return False
            raise
        return self.is_authenticated

    async def ensure_session(
        self, *, username: str | None = None, password: str | None = None, remember: bool = True
    ) -> bool:
        """Check that the session is still logged in, and log in again if it expired.

        A new login only happens if the session expired and both ``username`` and ``password`` are given.
        They are used for this call only and are never stored. A network error does not cause a new
        login, and no earlier changes to the account are repeated.

        Parameters
        ----------
        username: :class:`str`, optional
            The e-mail address or username to log in with if the session expired.
        password: :class:`str`, optional
            The password to log in with if the session expired.
        remember: :class:`bool`, optional
            Passed to :meth:`login`. Defaults to :data:`True`.

        Returns
        -------
        :class:`bool`
            :data:`True` if the session is logged in afterwards, or :data:`False` if the session expired and no
            username and password were given.

        Raises
        ------
        :class:`AuthenticationError`
            Logging in again failed because the username or password is wrong.
        :class:`MFARequiredError`
            The new login must be approved in the DAK app.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        if await self.refresh_session():
            return True
        if username is None or password is None:
            return False
        await self.login(username, password, remember=remember)
        return True

    async def logout(self) -> None:
        """Log out and end the session on DAK's servers.

        Raises
        ------
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        await self.__http.logout()

    @property
    def is_authenticated(self) -> bool:
        """Whether the client has a login cookie.

        This only checks that the cookie exists, not that it is still valid. Use :meth:`refresh_session`
        to check with DAK.

        Returns
        -------
        :class:`bool`
            :data:`True` if the client has a login cookie, even if it has expired.
        """
        return self.__http.is_authenticated()
