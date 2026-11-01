from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import msgspec

from .._types.flows import (
    AccessibilityWishInputs,
    CityWishInputs,
    DistrictWishInputs,
    HousingSubtypeWishInputs,
    HousingTypeWishInputs,
    MaximumWishInputs,
    MinimumWishInputs,
    RecalculateWishesInputs,
    RemoveCityWishInputs,
    WishOptionPayload,
    WishReferencePayload,
    WishSelectionPayload,
    WizardPayload,
)
from ..endpoints.flows import HousingWishes
from ..models.base import records
from ..models.flows import WishChoice

if TYPE_CHECKING:
    from collections.abc import Iterable

    from ..http import HTTPClient
    from ._client import Client

_Category = Literal["cities", "districts", "types", "subtypes", "accessibility"]


class HousingWishesClient:
    """Methods for changing the account's housing wishes (*woonwensen*).

    Use it through :attr:`Client.wishes` instead of creating it directly. Every method requires the client to be
    logged in and raises :class:`~mijndak.errors.NotLoggedInError` otherwise. To read the current wishes, use
    :meth:`AccountClient.housing_wishes`.

    The options to choose from come from DAK, so pass IDs from :meth:`cities`, :meth:`districts`,
    :meth:`housing_types`, :meth:`housing_subtypes` and :meth:`accessibility`.

    Parameters
    ----------
    parent: :class:`Client`
        The client this belongs to.
    """

    def __init__(self, parent: Client, /) -> None:
        self._parent: Client = parent
        self.__http: HTTPClient = parent.http

    async def _wizard(self) -> WizardPayload:
        data = await self.__http.data_action(HousingWishes.WIZARD)
        if not data.get("Woonwens", {}).get("Id"):
            raise ValueError("DAK returned no housing-wish wizard ID")
        return data

    async def _refresh_matches(self, wizard: WizardPayload) -> None:
        registration = wizard["Inschrijving"]
        preferences = await self._parent.settings.display_preferences()
        await self.__http.server_action(
            HousingWishes.RECALCULATE,
            RecalculateWishesInputs(Inschrijving=registration, WoonwensFilterIsEis=preferences.filters_by_wishes),
        )

    async def set_minimum_rooms(self, rooms: int) -> None:
        """Set the smallest number of rooms wanted.

        Afterwards this recalculates which listings match the wishes. That is a separate request, so it can fail
        after the change is saved.

        Parameters
        ----------
        rooms: :class:`int`
            The smallest number of rooms.

        Raises
        ------
        :exc:`ValueError`
            ``rooms`` is negative or not an integer, or DAK returned no housing wishes to change.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        self._nonnegative(rooms)
        wizard = await self._wizard()
        await self.__http.server_action(
            HousingWishes.MINIMUM_ROOMS,
            MinimumWishInputs(MinimaalAantal=rooms, WoonwensWizardId=wizard["Woonwens"]["Id"]),
        )
        await self._refresh_matches(wizard)

    async def set_maximum_rent(self, rent: int) -> None:
        """Set the highest rent wanted.

        Afterwards this recalculates which listings match the wishes. That is a separate request, so it can fail
        after the change is saved.

        Parameters
        ----------
        rent: :class:`int`
            The highest rent per month, in whole euros.

        Raises
        ------
        :exc:`ValueError`
            ``rent`` is negative or not an integer, or DAK returned no housing wishes to change.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        self._nonnegative(rent)
        wizard = await self._wizard()
        await self.__http.server_action(
            HousingWishes.MAXIMUM_RENT,
            MaximumWishInputs(MaximaalAantal=rent, WoonwensWizardId=wizard["Woonwens"]["Id"]),
        )
        await self._refresh_matches(wizard)

    async def set_minimum_area(self, area: int) -> None:
        """Set the smallest floor area wanted.

        Afterwards this recalculates which listings match the wishes. That is a separate request, so it can fail
        after the change is saved.

        Parameters
        ----------
        area: :class:`int`
            The smallest floor area, in square metres.

        Raises
        ------
        :exc:`ValueError`
            ``area`` is negative or not an integer, or DAK returned no housing wishes to change.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        self._nonnegative(area)
        wizard = await self._wizard()
        await self.__http.server_action(
            HousingWishes.MINIMUM_AREA,
            MinimumWishInputs(MinimaalAantal=area, WoonwensWizardId=wizard["Woonwens"]["Id"]),
        )
        await self._refresh_matches(wizard)

    @staticmethod
    def _nonnegative(value: int) -> None:
        if type(value) is not int or value < 0:
            raise ValueError("An integer greater than or equal to zero is required")

    async def _choices(self, category: _Category, wizard: WizardPayload, parent_id: str = "") -> list[WishChoice]:
        action = {
            "cities": HousingWishes.CITIES,
            "districts": HousingWishes.DISTRICTS,
            "types": HousingWishes.TYPES,
            "subtypes": HousingWishes.SUBTYPES,
            "accessibility": HousingWishes.ACCESSIBILITY,
        }[category]
        variables: dict[str, object] = {
            "HaalInschrijvingEnWizardId": {
                "Inschrijving": wizard.get("Inschrijving", {}),
                "WoonwensId": wizard["Woonwens"]["Id"],
            },
            "_woonplaatsIdInDataFetchStatus": 1,
            "_eenheiddetailsoortGroepIdInDataFetchStatus": 1,
            "WoonplaatsId": parent_id,
            "EenheiddetailsoortGroepId": parent_id,
        }
        data = await self.__http.data_action(action, variables=variables)
        options: list[WishChoice] = []
        for item in records(data):
            reference, association, identifier = self._option_parts(category, item)
            if identifier:
                options.append(
                    WishChoice(
                        identifier,
                        reference.get("Naam", ""),
                        item.get("IsSelected", False),
                        reference.get("Code", ""),
                        association,
                    )
                )
        return options

    @staticmethod
    def _option_parts(
        category: _Category, item: WishOptionPayload
    ) -> tuple[WishReferencePayload, WishSelectionPayload, str]:
        if category == "cities":
            reference = item.get("Woonplaats", {})
            return reference, item.get("WoonWensWoonplaats", {}), reference.get("WoonplaatsId", "")
        if category == "districts":
            reference = item.get("Wijk", {})
            return reference, item.get("WoonWensWijk", {}), reference.get("WijkId", "")
        if category == "types":
            reference = item.get("EenheidDetailsoortGroep", {})
            return reference, item.get("EenheidDetailsoortGroepWoonwens", {}), reference.get("EenheidDetailsoortGroepId", "")
        if category == "subtypes":
            reference = item.get("EenheidDetailsoort", {})
            return reference, item.get("EenheidDetailsoortWoonwens", {}), reference.get("EenheidDetailsoortId", "")
        reference = item.get("Toegankelijkheid", {})
        return reference, item.get("ToegankelijkheidWoonwens", {}), reference.get("ToegankelijkheidId", "")

    async def cities(self) -> list[WishChoice]:
        """The towns that can be chosen.

        Returns
        -------
        list[:class:`WishChoice`]
            Each town, with whether it is part of the account's wishes.

        Raises
        ------
        :exc:`ValueError`
            DAK returned no housing wishes.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return await self._choices("cities", await self._wizard())

    async def districts(self, city_id: str) -> list[WishChoice]:
        """The districts of a town that can be chosen.

        Parameters
        ----------
        city_id: :class:`str`
            The town's ID, from :meth:`cities`.

        Returns
        -------
        list[:class:`WishChoice`]
            Each district, with whether it is part of the account's wishes.

        Raises
        ------
        :exc:`ValueError`
            DAK returned no housing wishes.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return await self._choices("districts", await self._wizard(), city_id)

    async def housing_types(self) -> list[WishChoice]:
        """The groups of housing types that can be chosen, such as apartments.

        Returns
        -------
        list[:class:`WishChoice`]
            Each group, with whether it is part of the account's wishes.

        Raises
        ------
        :exc:`ValueError`
            DAK returned no housing wishes.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return await self._choices("types", await self._wizard())

    async def housing_subtypes(self, group_id: str) -> list[WishChoice]:
        """The housing types in a group that can be chosen.

        Parameters
        ----------
        group_id: :class:`str`
            The group's ID, from :meth:`housing_types`.

        Returns
        -------
        list[:class:`WishChoice`]
            Each housing type, with whether it is part of the account's wishes.

        Raises
        ------
        :exc:`ValueError`
            DAK returned no housing wishes.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return await self._choices("subtypes", await self._wizard(), group_id)

    async def accessibility(self) -> list[WishChoice]:
        """The accessibility options that can be chosen, such as a ground-floor home.

        Returns
        -------
        list[:class:`WishChoice`]
            Each option, with whether it is part of the account's wishes.

        Raises
        ------
        :exc:`ValueError`
            DAK returned no housing wishes.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        return await self._choices("accessibility", await self._wizard())

    async def _selections(
        self, category: _Category, selected_ids: Iterable[str], wizard: WizardPayload, parent_id: str = ""
    ) -> tuple[list[WishSelectionPayload], list[WishSelectionPayload]]:
        choices = await self._choices(category, wizard, parent_id)
        selected = set(selected_ids)
        if selected - {choice.id for choice in choices}:
            raise ValueError("A selected option is not offered by DAK")
        if category == "accessibility":
            # DAK's wizard expands these accessible categories to their implied alternatives.
            implied = {"GEL": {"GNV", "NUL"}, "ROA": {"ROG"}}
            codes = {choice.code for choice in choices if choice.id in selected}
            extra_codes = {extra for code in codes for extra in implied.get(code, set[str]())}
            selected.update(choice.id for choice in choices if choice.code in extra_codes)
        active: list[WishSelectionPayload] = []
        inactive: list[WishSelectionPayload] = []
        key = {
            "cities": "WoonplaatsId",
            "districts": "WijkId",
            "types": "EenheidDetailsoortGroepId",
            "subtypes": "EenheidDetailsoortId",
            "accessibility": "ToegankelijkheidId",
        }[category]
        for choice in choices:
            if choice.id in selected:
                payload = {
                    **choice.selection,
                    "Id": choice.selection.get("Id", "0"),
                    "WoonWensWizardId": wizard["Woonwens"]["Id"],
                    key: choice.id,
                }
                active.append(msgspec.convert(payload, type=WishSelectionPayload))
            elif choice.selection.get("Id") not in {None, "", "0"}:
                inactive.append(choice.selection.copy())
        return active, inactive

    async def set_cities(self, city_ids: Iterable[str]) -> None:
        """Set which towns are wanted, replacing the current choice.

        Afterwards this recalculates which listings match the wishes. That is a separate request, so it can fail
        after the change is saved.

        Parameters
        ----------
        city_ids: Iterable[:class:`str`]
            The IDs of the towns, from :meth:`cities`. Pass nothing to clear the choice.

        Raises
        ------
        :exc:`ValueError`
            A town is not offered, or DAK returned no housing wishes to change.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        wizard = await self._wizard()
        active, inactive = await self._selections("cities", city_ids, wizard)
        await self.__http.server_action(
            HousingWishes.SET_CITIES,
            CityWishInputs(
                ActieveWoonplaatsen=active,
                InactieveWoonplaatsen=inactive,
                WoonwenswizardId=wizard["Woonwens"]["Id"],
            ),
        )
        await self._refresh_matches(wizard)

    async def set_districts(self, city_id: str, district_ids: Iterable[str]) -> None:
        """Set which districts of a town are wanted, replacing the current choice.

        Passing no districts removes the town from the wishes, as the website does. Afterwards this recalculates
        which listings match the wishes. That is a separate request, so it can fail after the change is saved.

        Parameters
        ----------
        city_id: :class:`str`
            The town's ID, from :meth:`cities`.
        district_ids: Iterable[:class:`str`]
            The IDs of the districts, from :meth:`districts`.

        Raises
        ------
        :exc:`ValueError`
            A district is not offered, or DAK returned no housing wishes to change.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        wizard = await self._wizard()
        active, inactive = await self._selections("districts", district_ids, wizard, city_id)
        if not active:
            await self.__http.server_action(
                HousingWishes.REMOVE_CITY,
                RemoveCityWishInputs(
                    WoonplaatsId=city_id,
                    WoonwensId=wizard["Woonwens"]["Id"],
                ),
            )
        else:
            await self.__http.server_action(
                HousingWishes.SET_DISTRICTS,
                DistrictWishInputs(
                    ActieveWoonwensWijk=active,
                    InactieveWoonwensWijk=inactive,
                ),
            )
        await self._refresh_matches(wizard)

    async def set_housing_types(self, group_ids: Iterable[str]) -> None:
        """Set which groups of housing types are wanted, replacing the current choice.

        Afterwards this recalculates which listings match the wishes. That is a separate request, so it can fail
        after the change is saved.

        Parameters
        ----------
        group_ids: Iterable[:class:`str`]
            The IDs of the groups, from :meth:`housing_types`.

        Raises
        ------
        :exc:`ValueError`
            A group is not offered, or DAK returned no housing wishes to change.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        wizard = await self._wizard()
        active, inactive = await self._selections("types", group_ids, wizard)
        await self.__http.server_action(
            HousingWishes.SET_TYPES,
            HousingTypeWishInputs(
                ActieveWoontype=active,
                InactieveWoontype=inactive,
                WoonwenswizardId=wizard["Woonwens"]["Id"],
            ),
        )
        await self._refresh_matches(wizard)

    async def set_housing_subtypes(self, group_id: str, subtype_ids: Iterable[str]) -> None:
        """Set which housing types in a group are wanted, replacing the current choice.

        Afterwards this recalculates which listings match the wishes. That is a separate request, so it can fail
        after the change is saved.

        Parameters
        ----------
        group_id: :class:`str`
            The group's ID, from :meth:`housing_types`.
        subtype_ids: Iterable[:class:`str`]
            The IDs of the housing types, from :meth:`housing_subtypes`.

        Raises
        ------
        :exc:`ValueError`
            A housing type is not offered, or DAK returned no housing wishes to change.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        wizard = await self._wizard()
        active, inactive = await self._selections("subtypes", subtype_ids, wizard, group_id)
        await self.__http.server_action(
            HousingWishes.SET_SUBTYPES,
            HousingSubtypeWishInputs(
                ActieveWoonsubtype=active,
                InactieveWoonsubtype=inactive,
            ),
        )
        await self._refresh_matches(wizard)

    async def set_accessibility(self, option_ids: Iterable[str]) -> None:
        """Set which accessibility options are wanted, replacing the current choice.

        Like the website, this also adds the options that some choices include. Afterwards this recalculates which
        listings match the wishes. That is a separate request, so it can fail after the change is saved.

        Parameters
        ----------
        option_ids: Iterable[:class:`str`]
            The IDs of the options, from :meth:`accessibility`.

        Raises
        ------
        :exc:`ValueError`
            An option is not offered, or DAK returned no housing wishes to change.
        :class:`NotLoggedInError`
            The client is not logged in.
        :class:`ServerError`
            DAK returned an error.
        :class:`HTTPError`
            The request failed.
        """
        wizard = await self._wizard()
        active, _ = await self._selections("accessibility", option_ids, wizard)
        await self.__http.server_action(
            HousingWishes.SET_ACCESSIBILITY,
            AccessibilityWishInputs(
                ActieveToegankelijkheid=active,
                WoonwensWizardId=wizard["Woonwens"]["Id"],
            ),
        )
        await self._refresh_matches(wizard)
