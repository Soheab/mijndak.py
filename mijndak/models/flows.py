from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from .actions import Result
from .base import Items, Model, Nested, field

if TYPE_CHECKING:
    from .._types.flows import WishSelectionPayload

__all__ = (
    "Bank",
    "Banks",
    "MFADevice",
    "MFAResult",
    "MFASetup",
    "MFAStatus",
    "MandateRedirect",
    "MandateStatus",
    "PaymentAction",
    "PaymentChoices",
    "PaymentOptions",
    "PaymentRedirect",
    "WishChoice",
)


@dataclass(frozen=True, slots=True)
class WishChoice:
    """An option in the housing wishes wizard, such as a town or a type of home.

    Pass its :attr:`id` to the matching ``set_...`` method of :class:`HousingWishesClient`.

    Attributes
    ----------
    id: :class:`str`
        The option's ID.
    name: :class:`str`
        The option's name, such as ``"Amsterdam"``.
    selected: :class:`bool`
        Whether the option is currently part of the account's housing wishes.
    code: :class:`str`
        The option's code, such as ``"GEL"`` for a ground-floor home.
    selection: :class:`WishSelectionPayload`
        The record that links the option to the account's housing wishes, as the API sent it.
    """

    id: str
    name: str
    selected: bool
    code: str
    selection: WishSelectionPayload


class MFAResult(Model):
    """The outcome of a multi-factor authentication action.

    Attributes
    ----------
    is_success: :class:`bool`
        Whether the action succeeded.
    reason: :class:`str` | :data:`None`
        DAK's explanation of the outcome. (*is success reden*)
    """

    is_success = field(bool, "IsSuccess", default=False)
    reason = field(str, "IsSuccessReden")


class MFASetup(MFAResult):
    """The details needed to link the DAK app for multi-factor authentication.

    Show :attr:`qr_code` to the user privately and have them scan it in the DAK app. It is a secret, so it is left
    out of the model's ``repr()``.

    Attributes
    ----------
    is_active: :class:`bool`
        Whether multi-factor authentication is already turned on. (*is actief*)
    needs_app: :class:`bool`
        Whether DAK thinks the user does not have the app yet. (*heeft de app nog niet*)
    environment: :class:`str` | :data:`None`
        The DAK app environment the code is for. (*deeplink environment*)
    """

    is_active = field(bool, "IsActief", default=False)
    _qr_code = field(str, "QRcode")
    needs_app = field(bool, "HeeftDeAppNogNiet", default=False)
    environment = field(str, "DeeplinkEnvironment")

    @property
    def qr_code(self) -> str | None:
        """The code to show as a QR code for the DAK app to scan.

        Treat it as a secret: anyone who scans it can link their app to the account.

        Returns
        -------
        :class:`str` | :data:`None`
            The code, or :data:`None` if DAK did not send one.
        """
        return self._qr_code


class MFADevice(Model):
    """The device linked for multi-factor authentication.

    Attributes
    ----------
    created_at: :class:`str` | :data:`None`
        When linking started, as an ISO 8601 string. (*datum tijd aangemaakt*)
    linked_at: :class:`str` | :data:`None`
        When the device was linked, as an ISO 8601 string. (*datum tijd gekoppeld*)
    activated_at: :class:`str` | :data:`None`
        When multi-factor authentication was turned on, as an ISO 8601 string. (*datum tijd geactiveerd*)
    deactivation_started_at: :class:`str` | :data:`None`
        When turning it off was requested, as an ISO 8601 string. (*datum tijd deactivatie gestart*)
    deactivated_at: :class:`str` | :data:`None`
        When it was turned off, as an ISO 8601 string. (*datum tijd gedeactiveerd*)
    name: :class:`str` | :data:`None`
        The device's name. (*device name*)
    last_login: :class:`str` | :data:`None`
        When the device was last used to log in, as an ISO 8601 string. (*last login*)
    is_active: :class:`bool`
        Whether the device is active. (*is actief*)
    """

    created_at = field(str, "DatumTijdAangemaakt")
    linked_at = field(str, "DatumTijdGekoppeld")
    activated_at = field(str, "DatumTijdGeactiveerd")
    deactivation_started_at = field(str, "DatumTijdDeactivatieGestart")
    deactivated_at = field(str, "DatumTijdGedeactiveerd")
    name = field(str, "DeviceName")
    last_login = field(str, "LastLogin")
    is_active = field(bool, "IsActief", default=False)


class MFAStatus(Model):
    """The state of the account's multi-factor authentication.

    Attributes
    ----------
    device: :class:`MFADevice`
        The linked device. (*MFA details*)
    has_backup_email: :class:`bool`
        Whether the account has a backup e-mail address for turning it off without the device.
        (*heeft backup emailadres*)
    email_used: :class:`str` | :data:`None`
        The e-mail address used for backup codes. (*emailadres gebruikt*)
    """

    device = Nested(MFADevice, "MFADetails")
    has_backup_email = field(bool, "HeeftBackupEmailadres", default=False)
    email_used = field(str, "EmailadresGebruikt")


class Bank(Model):
    """A bank that can be chosen for a payment or direct-debit mandate.

    Attributes
    ----------
    code: :class:`str` | :data:`None`
        The bank's code. Pass it to :meth:`PaymentsClient.start` or :meth:`PaymentsClient.start_mandate`.
    name: :class:`str` | :data:`None`
        The bank's name. (*naam*)
    """

    code = field(str, "Code")
    name = field(str, "Naam")


class Banks(Model):
    """The banks that can be chosen.

    Attributes
    ----------
    banks: list[:class:`Bank`]
        The banks. (*banken*)
    error_message: :class:`str` | :data:`None`
        The error message, if fetching the banks failed.
    """

    banks = Items(Bank, "Banken")
    error_message = field(str, "ErrorMessage")


class PaymentAction(Model):
    """A way to pay, such as iDEAL.

    Attributes
    ----------
    id: :class:`int` | :data:`None`
        The payment method's ID. Pass it to :meth:`PaymentsClient.start`.
    name: :class:`str` | :data:`None`
        The payment method's name. (*naam*)
    description: :class:`str` | :data:`None`
        The payment method's description. (*omschrijving*)
    order: :class:`int` | :data:`None`
        The position in the list of payment methods. (*volgorde nummer*)
    is_active: :class:`bool`
        Whether the payment method can be used. (*is actief*)
    """

    id = field(int, "Id")
    name = field(str, "Naam")
    description = field(str, "Omschrijving")
    order = field(int, "VolgordeNummer")
    is_active = field(bool, "IsActief", default=False)


class PaymentChoices(Model):
    """The payment methods and banks offered for a payment.

    Attributes
    ----------
    actions: list[:class:`PaymentAction`]
        The payment methods. (*betaal acties*)
    banks: list[:class:`Bank`]
        The banks. (*banken*)
    """

    actions = Items(PaymentAction, "BetaalActies")
    banks = Items(Bank, "Banken")


class PaymentOptions(Banks):
    """The ways the account can pay what it owes.

    Attributes
    ----------
    choices: :class:`PaymentChoices`
        The payment methods and banks offered. (*betaal acties*)
    """

    choices = Nested(PaymentChoices, "BetaalActies")


class PaymentRedirect(Model):
    """A payment that has been started and must be finished at the bank.

    Open :attr:`url` to pay. Starting a payment does not mean it was paid.

    Attributes
    ----------
    result: :class:`Result`
        Whether starting the payment succeeded.
    url: :class:`str` | :data:`None`
        The address of the bank's payment page. (*betaal URL*)
    message: :class:`str` | :data:`None`
        A message from DAK about the payment. (*status message*)
    """

    result = Nested(Result, "Result")
    url = field(str, "BetaalURL")
    message = field(str, "StatusMessage")


class MandateRedirect(Model):
    """A direct-debit mandate that has been started and must be approved at the bank.

    Open :attr:`url` to approve it. Starting a mandate does not mean it was approved.

    Attributes
    ----------
    url: :class:`str` | :data:`None`
        The address of the bank's approval page. (*betaal url*)
    message: :class:`str` | :data:`None`
        A message from DAK about the mandate. (*statusmessage*)
    """

    url = field(str, "BetaalUrl")
    message = field(str, "Statusmessage")


class MandateStatus(Model):
    """The state of a direct-debit mandate after returning from the bank.

    Attributes
    ----------
    status: :class:`str` | :data:`None`
        The mandate's status, exactly as DAK sent it.
    user_id: :class:`int` | :data:`None`
        The ID of the login account.
    """

    status = field(str, "Status")
    user_id = field(int, "UserId")
