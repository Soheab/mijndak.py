from __future__ import annotations

from .actions import Result
from .base import Items, Model, Nested, field

__all__ = (
    "PointsCategory",
    "PointsDashboard",
    "PointsResponse",
    "SearchPoints",
    "SearchPointsMonth",
    "TimedPointsCategory",
)


class PointsCategory(Model):
    """The points of one type, such as waiting points.

    Attributes
    ----------
    points: :class:`float` | :data:`None`
        The number of points. (*aantal*)
    text_line_1: :class:`str` | :data:`None`
        The first line of text the website shows. (*tekstregel 1*)
    text_line_2: :class:`str` | :data:`None`
        The second line of text the website shows. (*tekstregel 2*)
    """

    points = field(float, "Aantal")
    text_line_1 = field(str, "Tekstregel1")
    text_line_2 = field(str, "Tekstregel2")


class TimedPointsCategory(PointsCategory):
    """Points that are valid for a limited time, such as situation or starter points.

    Attributes
    ----------
    start_date: :class:`str` | :data:`None`
        The date the points started counting, as an ISO 8601 string. (*begindatum*)
    end_date: :class:`str` | :data:`None`
        The date the points expire, as an ISO 8601 string. (*einddatum*)
    renewal_date: :class:`str` | :data:`None`
        The date by which the points must be renewed, as an ISO 8601 string. (*verlengdatum*)
    is_shown: :class:`bool`
        Whether the website shows this type of points. (*tonen*)
    """

    start_date = field(str, "Begindatum")
    end_date = field(str, "Einddatum")
    renewal_date = field(str, "Verlengdatum")
    is_shown = field(bool, "Tonen", default=False)


class SearchPointsMonth(Model):
    """The reactions in one month that count towards search points.

    Attributes
    ----------
    month: :class:`int` | :data:`None`
        The month number. (*maand*)
    reactions: :class:`int` | :data:`None`
        The number of reactions placed in the month. (*aantal*)
    minimum_reactions: :class:`int` | :data:`None`
        The minimum number of reactions needed to earn search points for the month. (*min aantal*)
    text_line_1: :class:`str` | :data:`None`
        The first line of text the website shows. (*tekstregel 1*)
    """

    month = field(int, "Maand")
    reactions = field(int, "Aantal")
    minimum_reactions = field(int, "MinAantal")
    text_line_1 = field(str, "Tekstregel1")


class SearchPoints(PointsCategory):
    """Search points (*zoekpunten*), earned by reacting to listings regularly.

    Attributes
    ----------
    months: list[:class:`SearchPointsMonth`]
        The reactions per month that count towards the points. (*lst reacties*)
    """

    months = Items(SearchPointsMonth, "LstReacties")


class PointsDashboard(Model):
    """The points of one registration.

    Attributes
    ----------
    name: :class:`str` | :data:`None`
        The name of the registration. (*naam*)
    registration_date: :class:`str` | :data:`None`
        The start date of the registration, as an ISO 8601 string. (*overeenkomst begindatum*)
    registration_id: :class:`int` | :data:`None`
        The ID of the registration. (*relatie context id*)
    total: :class:`PointsCategory`
        The total points. (*totaalpunten*)
    waiting: :class:`PointsCategory`
        Waiting points (*wachtpunten*), earned by the time registered. (*wachtpunten*)
    search: :class:`SearchPoints`
        Search points (*zoekpunten*), earned by reacting to listings. (*zoekpunten*)
    situation: :class:`TimedPointsCategory`
        Situation points (*situatiepunten*), given for a specific situation. (*situatiepunten*)
    starter: :class:`TimedPointsCategory`
        Starter points (*startpunten*), given to new registrations. (*startpunten*)
    """

    name = field(str, "Naam")
    registration_date = field(str, "OvereenkomstBegindatum")
    registration_id = field(int, "RelatieContextId")
    total = Nested(PointsCategory, "Totaalpunten")
    waiting = Nested(PointsCategory, "Wachtpunten")
    search = Nested(SearchPoints, "Zoekpunten")
    situation = Nested(TimedPointsCategory, "Situatiepunten")
    starter = Nested(TimedPointsCategory, "Startpunten")


class PointsResponse(Model):
    """The points of each of the account's registrations.

    Attributes
    ----------
    registrations: list[:class:`PointsDashboard`]
        The points of each registration. (*puntendashboardoverzicht*)
    result: :class:`Result`
        Whether DAK handled the request successfully.
    """

    registrations = Items(PointsDashboard, "Puntendashboardoverzicht")
    result = Nested(Result, "Result")
