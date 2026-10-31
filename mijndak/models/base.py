from __future__ import annotations

import datetime as dt
from collections.abc import Callable, Mapping
from decimal import Decimal, InvalidOperation
from typing import TYPE_CHECKING, ClassVar, Self, TypeGuard, overload, override

if TYPE_CHECKING:
    from .._types import AggregatePayload
    from ..http import HTTPClient

__all__ = (
    "Descriptor",
    "Field",
    "Items",
    "Model",
    "Nested",
    "Payload",
    "field",
    "is_payload",
    "parse_datetime",
    "parse_decimal",
    "records",
    "to_pascal",
)

_OS_NULL_DATE = "1900-01-01"

#: One JSON record, as decoded from the API.
type Payload = Mapping[str, object]


def is_payload(value: object) -> TypeGuard[Payload]:
    """Check whether a value is a JSON record.

    Parameters
    ----------
    value: :class:`object`
        The value to check.

    Returns
    -------
    :class:`bool`
        :data:`True` if ``value`` is a mapping.
    """
    return isinstance(value, Mapping)


def _is_list(value: object) -> TypeGuard[list[object]]:
    return isinstance(value, list)


def records[T](aggregate: AggregatePayload[T]) -> list[T]:
    """Get the records out of an aggregate's response.

    Aggregates (``ScreenDataSet*`` endpoints) wrap their records as ``{"List": {"List": [...]}}``.

    Parameters
    ----------
    aggregate: :class:`AggregatePayload`
        The aggregate's response.

    Returns
    -------
    list
        The records, or an empty list if there are none.
    """
    container = aggregate.get("List")
    return (container.get("List") if container is not None else None) or []


def to_pascal(name: str) -> str:
    """Convert a snake_case attribute name to the PascalCase key the API uses.

    For example, ``woon_vertrekken_tot_opp`` becomes ``WoonVertrekkenTotOpp``.

    Parameters
    ----------
    name: :class:`str`
        The snake_case name.

    Returns
    -------
    :class:`str`
        The name in PascalCase.
    """
    return "".join(part[:1].upper() + part[1:] for part in name.split("_"))


def parse_decimal(value: str | None) -> Decimal | None:
    """Parse a decimal number, which the API sends as a string.

    Parameters
    ----------
    value: :class:`str` | :data:`None`
        The number as a string, such as ``"812.50"``.

    Returns
    -------
    :class:`~decimal.Decimal` | :data:`None`
        :data:`None` if ``value`` is :data:`None` or not a valid number.
    """
    if value is None:
        return None
    try:
        return Decimal(value)
    except (InvalidOperation, ValueError):
        return None


def parse_datetime(value: str | None) -> dt.datetime | None:
    """Parse a date and time, which the API sends as an ISO 8601 string.

    The API sends ``1900-01-01`` when there is no date.

    Parameters
    ----------
    value: :class:`str` | :data:`None`
        The date and time as a string.

    Returns
    -------
    :class:`~datetime.datetime` | :data:`None`
        :data:`None` if there is no date or ``value`` is not a valid date.
    """
    if not value or value.startswith(_OS_NULL_DATE):
        return None
    try:
        return dt.datetime.fromisoformat(value)
    except ValueError:
        return None


class Model:
    """The base class of every model: a view over one record from the API.

    A model reads its attributes from the record when they are first accessed, checks their types and caches them.
    It also holds the HTTP client, so models such as :class:`Listing` can make requests about themselves.

    Two models are equal if they are of the same class and were made from the same record.

    Parameters
    ----------
    data: :class:`Payload`
        The record, as the API sent it.
    state: :class:`HTTPClient`
        The HTTP client to make requests with.
    """

    __fields__: ClassVar[tuple[str, ...]] = ()

    def __init__(self, data: Payload, state: HTTPClient) -> None:
        self._data = data
        self._state = state

    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        declared = tuple(
            name for name, value in vars(cls).items() if isinstance(value, Descriptor) and not name.startswith("_")
        )
        cls.__fields__ = (*cls.__fields__, *declared)

    @property
    def raw(self) -> Payload:
        """The record exactly as the API sent it.

        Use it to read fields the model does not declare.

        Returns
        -------
        :class:`Payload`
            The record as a mapping of the API's keys to their values.
        """
        return self._data

    @property
    def state(self) -> HTTPClient:
        """The HTTP client this model makes requests with.

        Returns
        -------
        :class:`HTTPClient`
            The client the model was created with.
        """
        return self._state

    @override
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Model) and type(other) is type(self) and other.raw == self._data

    @override
    def __hash__(self) -> int:
        return id(self)

    @override
    def __repr__(self) -> str:
        shown: list[str] = []
        for name in self.__fields__:
            value: object = getattr(self, name)
            if value is None or value is False or isinstance(value, Model | list):
                continue
            shown.append(f"{name}={value!r}")
        return f"{type(self).__name__}({', '.join(shown)})"


class Descriptor[T]:
    """The base class of model attributes.

    A descriptor reads one attribute from the model's record when it is first accessed, and caches the value on the
    model.

    Parameters
    ----------
    key: :class:`str` | :data:`None`, optional
        The key in the record. Defaults to the attribute's name in PascalCase; see :func:`to_pascal`.

    Attributes
    ----------
    key: :class:`str`
        The key in the record.
    name: :class:`str`
        The attribute's name on the model.
    """

    def __init__(self, key: str | None = None) -> None:
        self.key = key or ""
        self.name = ""

    def __set_name__(self, owner: type[Model], name: str) -> None:
        self.name = name
        self.key = self.key or to_pascal(name)

    def read(self, obj: Model) -> T:
        """Read the attribute's value from a model's record.

        Parameters
        ----------
        obj: :class:`Model`
            The model to read from.

        Returns
        -------
        T
            The value.
        """
        raise NotImplementedError

    @overload
    def __get__(self, obj: None, owner: type[Model]) -> Self: ...
    @overload
    def __get__(self, obj: Model, owner: type[Model]) -> T: ...
    def __get__(self, obj: Model | None, owner: type[Model]) -> Self | T:
        if obj is None:
            return self
        result = self.read(obj)
        obj.__dict__[self.name] = result  # cache: instance attributes shadow non-data descriptors
        return result


class Field[T](Descriptor[T]):
    """An attribute holding a single value, such as a string or number.

    Create one with :func:`field` instead of directly. A missing value, or an empty string, reads as ``default``.

    Parameters
    ----------
    convert: Callable[[:class:`object`], T]
        Checks and converts the value from the record.
    default: T
        The value to use when the record has none.
    key: :class:`str` | :data:`None`, optional
        The key in the record. Defaults to the attribute's name in PascalCase.

    Attributes
    ----------
    convert: Callable[[:class:`object`], T]
        Checks and converts the value from the record.
    default: T
        The value to use when the record has none.
    """

    def __init__(self, convert: Callable[[object], T], default: T, key: str | None = None) -> None:
        super().__init__(key)
        self.convert = convert
        self.default = default

    @override
    def read(self, obj: Model) -> T:
        value = obj.raw.get(self.key)
        if value is None or value == "":  # ruff: ignore[compare-to-empty-string] - "" but not 0/False
            return self.default
        return self.convert(value)


@overload
def field[T](tp: type[T], key: str | None = None) -> Field[T | None]: ...
@overload
def field[T](tp: type[T], key: str | None = None, *, default: T) -> Field[T]: ...
def field[T](tp: type[T], key: str | None = None, *, default: T | None = None) -> Field[T] | Field[T | None]:
    """Declare a model attribute holding a single value.

    A missing value, or an empty string, reads as ``default``.

    Parameters
    ----------
    tp: :class:`type`
        The value's type, such as :class:`str` or :class:`int`.
    key: :class:`str` | :data:`None`, optional
        The key in the record. Defaults to the attribute's name in PascalCase.
    default: T | :data:`None`, optional
        The value to use when the record has none. Defaults to :data:`None`.

    Returns
    -------
    :class:`Field`
        The descriptor to assign to the model attribute.

    Raises
    ------
    :exc:`TypeError`
        When the attribute is read, if the record's value is not of type ``tp``.
    """

    def convert(value: object) -> T | None:
        if isinstance(value, tp):
            return value
        msg = f"expected {tp.__name__}, got {type(value).__name__}: {value!r}"
        raise TypeError(msg)

    return Field[T | None](convert, default, key)


class Nested[M: Model](Descriptor[M]):
    """An attribute holding another model, such as a listing's address.

    If the record has no value, the attribute holds an empty model, so its own attributes read as their defaults.

    Parameters
    ----------
    model: type[:class:`Model`]
        The model class of the nested record.
    key: :class:`str` | :data:`None`, optional
        The key in the record. Defaults to the attribute's name in PascalCase.

    Attributes
    ----------
    model: type[:class:`Model`]
        The model class of the nested record.
    """

    def __init__(self, model: type[M], key: str | None = None) -> None:
        super().__init__(key)
        self.model = model

    @override
    def read(self, obj: Model) -> M:
        value = obj.raw.get(self.key)
        return self.model(value if is_payload(value) else {}, obj.state)


class Items[M: Model](Descriptor[list[M]]):
    """An attribute holding a list of models, such as a listing's rooms.

    The API sends lists as ``{"List": [...]}``. If the record has no list, the attribute holds an empty list.

    Parameters
    ----------
    model: type[:class:`Model`]
        The model class of the list's records.
    key: :class:`str` | :data:`None`, optional
        The key in the record. Defaults to the attribute's name in PascalCase.

    Attributes
    ----------
    model: type[:class:`Model`]
        The model class of the list's records.
    """

    def __init__(self, model: type[M], key: str | None = None) -> None:
        super().__init__(key)
        self.model = model

    @override
    def read(self, obj: Model) -> list[M]:
        container = obj.raw.get(self.key)
        if not is_payload(container):
            return []
        records = container.get("List")
        if not _is_list(records):
            return []
        return [self.model(record, obj.state) for record in records if is_payload(record)]
