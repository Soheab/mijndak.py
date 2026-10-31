from typing import TypedDict

__all__ = ("AggregatePayload", "LongInteger", "OSListPayload", "ResultPayload")

#: OutSystems serialises ``LongInteger`` as a JSON string.
type LongInteger = str


class OSListPayload[T](TypedDict, total=False):
    """OutSystems ``RecordList``: ``{"List": [...], "EmptyListItem": {...}}``."""

    List: list[T]


class AggregatePayload[T](TypedDict, total=False):
    """Output of a ``ScreenDataSet*`` aggregate: ``{"List": {"List": [...]}, "Count": n}``."""

    List: OSListPayload[T]
    Count: int


class ResultPayload(TypedDict, total=False):
    IsSuccess: bool
    StatusCode: int
    ErrorMessage: str
