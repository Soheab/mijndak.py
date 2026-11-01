from __future__ import annotations

from typing import TYPE_CHECKING

from .._types.flows import EmptyInputs, MFABackupInputs, MFACodeInputs
from ..endpoints.flows import MFA
from ..models.flows import MFAResult, MFASetup, MFAStatus

if TYPE_CHECKING:
    from ..http import HTTPClient
    from ._client import Client


class MFAClient:
    """Methods for turning the DAK app's multi-factor authentication on and off.

    Use it through :attr:`Client.mfa` instead of creating it directly. Every method requires the client to be logged
    in and raises :class:`~mijndak.errors.NotLoggedInError` otherwise. Nothing here changes security settings unless
    you call it.

    Parameters
    ----------
    parent: :class:`Client`
        The client this belongs to.
    """

    def __init__(self, parent: Client, /) -> None:
        self._parent: Client = parent
        self.__http: HTTPClient = parent.http

    async def start_setup(self) -> MFASetup:
        """Start linking the DAK app, or continue a link that was already started.

        Show :attr:`MFASetup.qr_code` to the user privately and have them scan it in the DAK app, then pass the code
        the app shows to :meth:`activate`.

        Returns
        -------
        :class:`MFASetup`
            The code to scan and whether multi-factor authentication is already on.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return MFASetup(await self.__http.data_action(MFA.SETUP), self.__http)

    async def activate(self, code: str) -> MFAResult:
        """Turn on multi-factor authentication with the code the DAK app shows.

        Parameters
        ----------
        code: :class:`str`
            The code from the DAK app, after scanning the code from :meth:`start_setup`.

        Returns
        -------
        :class:`MFAResult`
            Whether it was turned on, and DAK's explanation.

        Raises
        ------
        :exc:`ValueError`
            ``code`` is empty or has spaces around it.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        self._validate_code(code)
        return MFAResult(await self.__http.server_action(MFA.ACTIVATE, MFACodeInputs(InvoerCode=code)), self.__http)

    async def status(self) -> MFAStatus:
        """The linked device and whether there is a backup e-mail address.

        Returns
        -------
        :class:`MFAStatus`
            The device's details and the backup e-mail address.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return MFAStatus(await self.__http.data_action(MFA.STATUS), self.__http)

    async def request_deactivation(self) -> MFAResult:
        """Ask the linked device to approve turning multi-factor authentication off.

        The DAK app then shows a code. Pass it to :meth:`deactivate`.

        Returns
        -------
        :class:`MFAResult`
            Whether the request was sent, and DAK's explanation.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return MFAResult(await self.__http.server_action(MFA.REQUEST_DEACTIVATION, EmptyInputs()), self.__http)

    async def deactivate(self, code: str) -> MFAResult:
        """Turn off multi-factor authentication with the code the linked device shows.

        Parameters
        ----------
        code: :class:`str`
            The code from the DAK app, after :meth:`request_deactivation`.

        Returns
        -------
        :class:`MFAResult`
            Whether it was turned off, and DAK's explanation.

        Raises
        ------
        :exc:`ValueError`
            ``code`` is empty or has spaces around it.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        self._validate_code(code)
        return MFAResult(await self.__http.server_action(MFA.DEACTIVATE, MFACodeInputs(InvoerCode=code)), self.__http)

    async def deactivate_with_backup_code(self, code: str) -> MFAResult:
        """Turn off multi-factor authentication with a code sent to the backup e-mail address.

        Use this when the linked device is lost. It does not send a new code; use one DAK already sent.

        Parameters
        ----------
        code: :class:`str`
            The code from the backup e-mail.

        Returns
        -------
        :class:`MFAResult`
            Whether it was turned off, and DAK's explanation.

        Raises
        ------
        :exc:`ValueError`
            ``code`` is empty or has spaces around it, or DAK did not return the main applicant's ID.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        self._validate_code(code)
        person = (await self._parent.account.personal_details()).person
        if not person.id:
            raise ValueError("DAK returned no applicant ID")
        inputs = MFABackupInputs(
            InvoerCode=code,
            NatuurlijkPersoonId=person.id,
            SamenwerkingsVerbandId=self._parent.region.swv_id,
        )
        return MFAResult(await self.__http.server_action(MFA.BACKUP_DEACTIVATE, inputs), self.__http)

    @staticmethod
    def _validate_code(code: str) -> None:
        if not code or code != code.strip():
            raise ValueError("A non-empty verification code without surrounding whitespace is required")
