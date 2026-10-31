from __future__ import annotations

from .base import Model, Nested, field

__all__ = ("ActionResult", "Result")


class Result(Model):
    """Whether DAK handled a request successfully.

    Attributes
    ----------
    is_success: :class:`bool`
        Whether the request succeeded.
    status_code: :class:`int` | :data:`None`
        The status code DAK returned.
    error_message: :class:`str` | :data:`None`
        The error message, if the request failed.
    """

    is_success = field(bool, "IsSuccess", default=False)
    status_code = field(int, "StatusCode")
    error_message = field(str, "ErrorMessage")


class ActionResult(Model):
    """The outcome of a change to the account, such as reacting to a listing.

    Attributes
    ----------
    result: :class:`Result`
        Whether the change succeeded. See also ``is_success``.
    """

    result = Nested(Result, "Result")

    @property
    def is_success(self) -> bool:
        """Whether the change succeeded.

        Returns
        -------
        :class:`bool`
            :data:`True` if the change succeeded.
        """
        return self.result.is_success
