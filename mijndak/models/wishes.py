from __future__ import annotations

from .base import Items, Model, Nested, field

__all__ = (
    "Accessibility",
    "District",
    "HousingTypeGroup",
    "HousingWish",
    "NamedEntity",
    "NavigationLocation",
    "NavigationOption",
    "NavigationType",
    "PlaceWithDistricts",
    "WishesResponse",
)


class HousingWish(Model):
    """The account's housing wishes (*woonwens*).

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The record's ID.
    minimum_rent: :class:`float` | :data:`None`
        The lowest rent wanted. (*min huurprijs*)
    maximum_rent: :class:`float` | :data:`None`
        The highest rent wanted. (*max huurprijs*)
    minimum_rooms: :class:`int` | :data:`None`
        The smallest number of rooms wanted. (*min kamers*)
    maximum_rooms: :class:`int` | :data:`None`
        The largest number of rooms wanted. (*max kamers*)
    minimum_area: :class:`float` | :data:`None`
        The smallest floor area wanted, in square metres. (*min oppervlakte*)
    maximum_area: :class:`float` | :data:`None`
        The largest floor area wanted, in square metres. (*max oppervlakte*)
    updated_at: :class:`str` | :data:`None`
        When the record was last changed, as an ISO 8601 string. (*laatst gewijzigd op*)
    """

    id = field(str, "Id")
    minimum_rent = field(float, "MinHuurprijs")
    maximum_rent = field(float, "MaxHuurprijs")
    minimum_rooms = field(int, "MinKamers")
    maximum_rooms = field(int, "MaxKamers")
    minimum_area = field(float, "MinOppervlakte")
    maximum_area = field(float, "MaxOppervlakte")
    updated_at = field(str, "LaatstGewijzigdOp")


class NamedEntity(Model):
    """An option with an ID and a name, such as a town, district or housing type.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The record's ID.
    name: :class:`str` | :data:`None`
        The name. (*naam*)
    code: :class:`str` | :data:`None`
        The code.
    """

    id = field(str, "Id")
    name = field(str, "Naam")
    code = field(str, "Code")


class District(NamedEntity):
    """A district (*wijk*) of a town.

    Attributes
    ----------
    city_id: :class:`str` | :data:`None`
        The ID of the town the district is in. (*woonplaats id*)
    """

    city_id = field(str, "WoonplaatsId")


class PlaceWithDistricts(Model):
    """A town with its districts.

    Attributes
    ----------
    city: :class:`NamedEntity`
        The town. (*woonplaats*)
    districts: list[:class:`District`]
        The town's districts. (*wijken lijst*)
    """

    city = Nested(NamedEntity, "Woonplaats")
    districts = Items(District, "WijkenLijst")


class HousingTypeGroup(Model):
    """A group of housing types, such as apartments, with the types in it.

    Attributes
    ----------
    group: :class:`NamedEntity`
        The group. (*eenheid detailsoort groep*)
    types: list[:class:`NamedEntity`]
        The housing types in the group. (*eenheid detailsoort lijst*)
    """

    group = Nested(NamedEntity, "EenheidDetailsoortGroep")
    types = Items(NamedEntity, "EenheidDetailsoortLijst")


class Accessibility(Model):
    """An accessibility option, such as a ground-floor home.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The option's ID. (*toegankelijkheid id*)
    code: :class:`str` | :data:`None`
        The code.
    name: :class:`str` | :data:`None`
        The name. (*naam*)
    updated_at: :class:`str` | :data:`None`
        When the record was last changed, as an ISO 8601 string. (*laatst gewijzigd op*)
    """

    id = field(str, "ToegankelijkheidId")
    code = field(str, "Code")
    name = field(str, "Naam")
    updated_at = field(str, "LaatstGewijzigdOp")


class NavigationLocation(Model):
    """An address to measure travel time from, such as a workplace.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The record's ID.
    wishes_id: :class:`str` | :data:`None`
        The ID of the housing wishes the address belongs to. (*woon wens wizard id*)
    type_id: :class:`int` | :data:`None`
        The type of location, such as work or school. (*woon wens navigatie type id*)
    street: :class:`str` | :data:`None`
        The street name. (*straatnaam*)
    house_number: :class:`int` | :data:`None`
        The house number. (*huisnummer*)
    house_number_addition: :class:`str` | :data:`None`
        The house number addition, such as ``2-hoog``. (*huisnummer toevoeging*)
    postcode: :class:`str` | :data:`None`
        The postcode.
    city: :class:`str` | :data:`None`
        The town or city. (*woonplaats naam*)
    """

    id = field(str, "Id")
    wishes_id = field(str, "WoonWensWizardId")
    type_id = field(int, "WoonWensNavigatieTypeId")
    street = field(str, "Straatnaam")
    house_number = field(int, "Huisnummer")
    house_number_addition = field(str, "HuisnummerToevoeging")
    postcode = field(str, "Postcode")
    city = field(str, "WoonplaatsNaam")


class NavigationType(Model):
    """A type of location to measure travel time from, such as work or school.

    Attributes
    ----------
    id: :class:`int` | :data:`None`
        The type's ID.
    label: :class:`str` | :data:`None`
        The type's name.
    icon: :class:`str` | :data:`None`
        The name of the type's icon.
    order: :class:`int` | :data:`None`
        The position in the list of types.
    is_active: :class:`bool`
        Whether the type can be chosen.
    """

    id = field(int, "Id")
    label = field(str, "Label")
    icon = field(str, "Icon")
    order = field(int, "Order")
    is_active = field(bool, "Is_Active", default=False)


class NavigationOption(Model):
    """A location to measure travel time from, together with its type.

    Attributes
    ----------
    location: :class:`NavigationLocation`
        The location. (*woon wens navigatie opties*)
    type: :class:`NavigationType`
        The type of location. (*woon wens navigatie type*)
    """

    location = Nested(NavigationLocation, "WoonWensNavigatieOpties")
    type = Nested(NavigationType, "WoonWensNavigatieType")


class WishesResponse(Model):
    """The account's housing wishes and the options to choose from.

    Attributes
    ----------
    wishes: :class:`HousingWish`
        The account's housing wishes. (*woonwens*)
    cities: list[:class:`PlaceWithDistricts`]
        The towns that can be chosen, each with its districts. (*woonplaatsen met wijken lijst*)
    housing_types: list[:class:`HousingTypeGroup`]
        The housing types that can be chosen, in groups. (*woon type met sub woon types lijst*)
    accessibility_options: list[:class:`Accessibility`]
        The accessibility options that can be chosen. (*toegankelijkheid lijst*)
    locations: list[:class:`NavigationOption`]
        The locations to measure travel time from. (*woon wens navigatie opties*)
    """

    wishes = Nested(HousingWish, "Woonwens")
    cities = Items(PlaceWithDistricts, "WoonplaatsenMetWijkenLijst")
    housing_types = Items(HousingTypeGroup, "WoonTypeMetSubWoonTypesLijst")
    accessibility_options = Items(Accessibility, "ToegankelijkheidLijst")
    locations = Items(NavigationOption, "WoonWensNavigatieOpties")
