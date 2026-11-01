from __future__ import annotations

from typing import TYPE_CHECKING, Final, Self

from ..http import HTTPClient
from ..region import AMSTERDAM, Region
from ._account import AccountClient
from ._auth import AuthClient
from ._listing import ListingsClient
from ._mfa import MFAClient
from ._payments import PaymentsClient
from ._reactions import ReactionsClient
from ._settings import SettingsClient
from ._wishes import HousingWishesClient

if TYPE_CHECKING:
    from types import TracebackType

    import aiohttp


__all__ = ("Client",)


class Client:
    """Async client for DAK (mijndak.nl), the social housing platform used by several Dutch regions.

    Methods are grouped by topic into sub-clients: :attr:`auth`, :attr:`listings`, :attr:`reactions`,
    :attr:`account`, :attr:`settings`, :attr:`wishes`, :attr:`mfa` and :attr:`payments`.

    Parameters
    ----------
    region: :class:`Region`, optional
        The DAK region to connect to. Defaults to :data:`~mijndak.region.AMSTERDAM`.
    session: :class:`aiohttp.ClientSession`, optional
        Session to make requests with. If omitted, the client creates its own and closes it in :meth:`close`.
    timeout: :class:`float`, optional
        Request timeout in seconds. Defaults to ``20.0``.

    Attributes
    ----------
    region: :class:`Region`
        The region this client is connected to.
    http: :class:`HTTPClient`
        The low-level client that makes the requests and returns the raw API data.

    Examples
    --------
    ::

        async with mijndak.Client() as client:
            await client.auth.login("me@example.com", "hunter2")
            for listing in await client.listings.matching():
                print(listing.address, listing.rent, listing.position)
    """

    def __init__(
        self,
        *,
        region: Region = AMSTERDAM,
        session: aiohttp.ClientSession | None = None,
        timeout: float = 20.0,
    ) -> None:
        self.region: Final = region
        self.http: HTTPClient = HTTPClient(
            region.base_url, region.client_variables(), region.swv_id, session=session, timeout=timeout
        )

    async def close(self) -> None:
        """Close the underlying HTTP session.

        This is called automatically when the client is used with ``async with``.
        """
        await self.http.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.close()

    @property
    def auth(self) -> AuthClient:
        """Methods for logging in and out, and for saving and restoring the session.

        Returns
        -------
        :class:`AuthClient`
            A new sub-client that uses this client's session.
        """
        return AuthClient(self)

    @property
    def listings(self) -> ListingsClient:
        """Methods for housing listings: all, matching, saved, hidden and individual listings.

        Returns
        -------
        :class:`ListingsClient`
            A new sub-client that uses this client's session.
        """
        return ListingsClient(self)

    @property
    def reactions(self) -> ReactionsClient:
        """Methods for viewing, placing and withdrawing reactions to listings.

        Returns
        -------
        :class:`ReactionsClient`
            A new sub-client that uses this client's session.
        """
        return ReactionsClient(self)

    @property
    def account(self) -> AccountClient:
        """Methods for the account's profile: points, wishes, personal details, household and documents.

        Returns
        -------
        :class:`AccountClient`
            A new sub-client that uses this client's session.
        """
        return AccountClient(self)

    @property
    def settings(self) -> SettingsClient:
        """Methods for account settings: login details, registrations, MFA, display and password.

        Returns
        -------
        :class:`SettingsClient`
            A new sub-client that uses this client's session.
        """
        return SettingsClient(self)

    @property
    def wishes(self) -> HousingWishesClient:
        """Methods for changing the account's housing wishes.

        Returns
        -------
        :class:`HousingWishesClient`
            A new sub-client that uses this client's session.
        """
        return HousingWishesClient(self)

    @property
    def mfa(self) -> MFAClient:
        """Methods for turning the DAK app's multi-factor authentication on and off.

        Returns
        -------
        :class:`MFAClient`
            A new sub-client that uses this client's session.
        """
        return MFAClient(self)

    @property
    def payments(self) -> PaymentsClient:
        """Methods for paying fees and setting up direct debit.

        Returns
        -------
        :class:`PaymentsClient`
            A new sub-client that uses this client's session.
        """
        return PaymentsClient(self)
