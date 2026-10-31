from __future__ import annotations

__all__ = (
    "AuthenticationError",
    "EndpointNotFoundError",
    "HTTPError",
    "MFARequiredError",
    "MijnDakError",
    "NotLoggedInError",
    "ServerError",
    "VersionChangedError",
)


class MijnDakError(Exception):
    """The base class of every error this library raises.

    Catch it to handle any error from this library at once.
    """


class HTTPError(MijnDakError):
    """The website answered with an HTTP error status, such as 404 or 500.

    This usually means the website is down or under maintenance.

    Parameters
    ----------
    status: :class:`int`
        The HTTP status code.
    url: :class:`str`
        The URL of the request.
    body: :class:`str`
        The body of the response.

    Attributes
    ----------
    status: :class:`int`
        The HTTP status code.
    url: :class:`str`
        The URL of the request.
    body: :class:`str`
        The body of the response.
    """

    def __init__(self, status: int, url: str, body: str) -> None:
        self.status = status
        self.url = url
        self.body = body
        super().__init__(f"HTTP {status} for {url}: {body[:200]}")


class ServerError(MijnDakError):
    """DAK received the request but refused or failed to handle it.

    For example, reacting to a listing that has already closed raises this error. The website still answers with
    HTTP status 200, but sends an error instead of data.

    Parameters
    ----------
    name: :class:`str` | :data:`None`
        The name of the error, if DAK gave one.
    message: :class:`str` | :data:`None`
        The error message, if DAK gave one.
    specific_type: :class:`str` | :data:`None`
        A more specific type of the error, if DAK gave one.
    endpoint: :class:`str`
        The endpoint the request was sent to.

    Attributes
    ----------
    name: :class:`str` | :data:`None`
        The name of the error, if DAK gave one.
    message: :class:`str` | :data:`None`
        The error message, if DAK gave one. It is often in Dutch.
    specific_type: :class:`str` | :data:`None`
        A more specific type of the error, if DAK gave one.
    endpoint: :class:`str`
        The endpoint the request was sent to.
    """

    def __init__(self, name: str | None, message: str | None, specific_type: str | None, endpoint: str) -> None:
        self.name = name
        self.message = message
        self.specific_type = specific_type
        self.endpoint = endpoint
        super().__init__(f"{endpoint}: {name}: {message}")


class NotLoggedInError(ServerError):
    """The request needs a logged-in account, but the client is not logged in or the session has expired.

    Log in with :meth:`AuthClient.login`, or use :meth:`AuthClient.ensure_session` to log in again only when needed.
    It has the same attributes as :class:`ServerError`.
    """


class AuthenticationError(MijnDakError):
    """Logging in failed.

    This usually means the username or password is wrong, but it is also raised if the account is blocked or DAK did
    not start a session.
    """


class MFARequiredError(AuthenticationError):
    """The login must be approved in the DAK app before it can finish.

    This happens when the account has multi-factor authentication turned on. Approve the login in the app, then call
    :meth:`AuthClient.login` again.
    """


class EndpointNotFoundError(MijnDakError):
    """The library could not find an endpoint on the website.

    Every request needs a version code that the library reads from the website's scripts. This error means the code
    could not be found, which usually happens after DAK changed or removed the page the endpoint belongs to.
    """


class VersionChangedError(MijnDakError):
    """DAK updated its website during a request, and the request failed again after retrying.

    The library retries once automatically when the website is updated. Trying again a little later usually works.
    """
