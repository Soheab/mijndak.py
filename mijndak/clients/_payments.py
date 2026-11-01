from __future__ import annotations

from typing import TYPE_CHECKING

from .._types.flows import MandateInputs, MandateStatusInputs, StartPaymentInputs
from ..endpoints.flows import Payments
from ..models.flows import Banks, MandateRedirect, MandateStatus, PaymentOptions, PaymentRedirect

if TYPE_CHECKING:
    from ..http import HTTPClient
    from ._client import Client


class PaymentsClient:
    """Methods for paying fees and setting up direct debit.

    Use it through :attr:`Client.payments` instead of creating it directly. Every method requires the client to be
    logged in and raises :class:`~mijndak.errors.NotLoggedInError` otherwise.

    The methods that start a payment or mandate only return the bank's address. They never open it, never choose a
    payment method by themselves and do not confirm that anything was paid.

    Parameters
    ----------
    parent: :class:`Client`
        The client this belongs to.
    """

    def __init__(self, parent: Client, /) -> None:
        self._parent: Client = parent
        self.__http: HTTPClient = parent.http

    async def _person_id(self) -> str:
        person_id = (await self._parent.account.personal_details()).person.id
        if not person_id:
            raise ValueError("DAK returned no applicant ID")
        return person_id

    async def options(self, *, guid: str = "") -> PaymentOptions:
        """The payment methods and banks offered to the account.

        Parameters
        ----------
        guid: :class:`str`, optional
            The ID of a payment that is already in progress, if any.

        Returns
        -------
        :class:`PaymentOptions`
            The payment methods and banks.

        Raises
        ------
        :exc:`ValueError`
            DAK did not return the main applicant's ID.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        person_id = await self._person_id()
        variables: dict[str, object] = {
            "NatuurlijkPersoonId": person_id,
            "HaalAanvrager": {"NatuurlijkPersoonId": person_id},
            "_natuurlijkPersoonIdInDataFetchStatus": 1,
            "_samenwerkingsverbandIdInDataFetchStatus": 1,
            "SamenwerkingsverbandId": self._parent.region.swv_id,
            "IsDak": True,
            "IsBetalen": True,
            "GUID": guid,
        }
        return PaymentOptions(await self.__http.data_action(Payments.OPTIONS, variables=variables), self.__http)

    async def start(self, action_id: int, *, bank_code: str = "", guid: str = "") -> PaymentRedirect:
        """Start a payment and get the address of the bank's payment page.

        Only call this when the user has chosen to pay. Open the returned address to pay; this method does not open
        it, and starting a payment does not mean it was paid.

        Parameters
        ----------
        action_id: :class:`int`
            The ID of the payment method, from :attr:`PaymentAction.id` in :meth:`options`.
        bank_code: :class:`str`, optional
            The bank's code, from :attr:`Bank.code` in :meth:`options`, if the payment method needs one.
        guid: :class:`str`, optional
            The ID of a payment that is already in progress, if any.

        Returns
        -------
        :class:`PaymentRedirect`
            The address of the bank's payment page.

        Raises
        ------
        :exc:`ValueError`
            The payment method or bank is not offered to the account, or DAK did not return the main applicant's ID.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        options = await self.options(guid=guid)
        if not any(item.id == action_id and item.is_active for item in options.choices.actions):
            raise ValueError("Payment method is not offered for this account")
        banks = [*options.banks, *options.choices.banks]
        if bank_code and not any(bank.code == bank_code for bank in banks):
            raise ValueError("Bank is not offered for this account")
        inputs = StartPaymentInputs(
            NatuurlijkPersoonId=await self._person_id(),
            SamenwerkingsverbandId=self._parent.region.swv_id,
            BetaalActieId=str(action_id),
            BankCode=bank_code,
            GUID=guid,
        )
        return PaymentRedirect(await self.__http.server_action(Payments.START, inputs), self.__http)

    async def mandate_banks(self) -> Banks:
        """The banks that can approve a direct-debit mandate.

        Returns
        -------
        :class:`Banks`
            The banks.

        Raises
        ------
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return Banks(await self.__http.data_action(Payments.BANKS), self.__http)

    async def start_mandate(self, bank_code: str) -> MandateRedirect:
        """Start setting up direct debit and get the address of the bank's approval page.

        Open the returned address to approve the mandate; this method does not open it, and starting a mandate does
        not mean it was approved. Check the outcome with :meth:`mandate_status`.

        Parameters
        ----------
        bank_code: :class:`str`
            The bank's code, from :attr:`Bank.code` in :meth:`mandate_banks`.

        Returns
        -------
        :class:`MandateRedirect`
            The address of the bank's approval page.

        Raises
        ------
        :exc:`ValueError`
            The bank does not offer mandates, or DAK did not return the main applicant's ID.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        options = await self.mandate_banks()
        if not bank_code or not any(bank.code == bank_code for bank in options.banks):
            raise ValueError("Bank is not offered for mandate authorization")
        inputs = MandateInputs(
            BankCodeLocal=bank_code,
            SamenwerkingsverbandId=self._parent.region.swv_id,
            Natuurlijkpersoonid=await self._person_id(),
        )
        return MandateRedirect(await self.__http.server_action(Payments.START_MANDATE, inputs), self.__http)

    async def mandate_status(self, guid: str) -> MandateStatus:
        """The state of a direct-debit mandate after returning from the bank.

        Parameters
        ----------
        guid: :class:`str`
            The ID the bank sends back when it returns to DAK.

        Returns
        -------
        :class:`MandateStatus`
            The mandate's status, exactly as DAK sent it.

        Raises
        ------
        :exc:`ValueError`
            ``guid`` is empty.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        if not guid.strip():
            raise ValueError("A bank return GUID is required")
        return MandateStatus(
            await self.__http.server_action(Payments.MANDATE_STATUS, MandateStatusInputs(GUID=guid)), self.__http
        )
