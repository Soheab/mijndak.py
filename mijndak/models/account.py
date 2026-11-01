from __future__ import annotations

from .actions import Result
from .base import Items, Model, Nested, field

__all__ = (
    "AccountStatus",
    "CodeName",
    "Configuration",
    "ConfigurationResponse",
    "Consent",
    "ConsentDetails",
    "ContactDetails",
    "CurrentHousing",
    "CurrentHousingResponse",
    "DataSharingResponse",
    "DisplayPreferences",
    "Document",
    "DocumentType",
    "DocumentsResponse",
    "ExternalLink",
    "Household",
    "HouseholdResponse",
    "HouseholdRole",
    "Income",
    "MFADetails",
    "MutationResult",
    "OpenPayment",
    "PasswordChangeResult",
    "Payment",
    "PaymentInformation",
    "PaymentsResponse",
    "Person",
    "PersonDocuments",
    "PersonUpdateResult",
    "PersonalDetails",
    "PointsLine",
    "PointsLinesResponse",
    "PointsTab",
    "PriorityRule",
    "PrioritySchemes",
    "PrioritySet",
    "ProfilePanel",
    "Registration",
    "ResidentialAddress",
    "Subscription",
    "SubscriptionsResponse",
    "User",
    "VSHIncome",
)


class ResidentialAddress(Model):
    """The address a person lives at (*woonadres*).

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The address's ID.
    street: :class:`str` | :data:`None`
        The street name. (*straatnaam*)
    house_number: :class:`int` | :data:`None`
        The house number. (*huisnummer*)
    house_number_addition: :class:`str` | :data:`None`
        The house number addition, such as ``2-hoog``. (*huisnummer toevoeging*)
    postcode: :class:`str` | :data:`None`
        The postcode.
    city_code: :class:`str` | :data:`None`
        The code of the town or city. (*woonplaats code*)
    city: :class:`str` | :data:`None`
        The town or city. (*woonplaats naam*)
    neighbourhood_code: :class:`str` | :data:`None`
        The code of the neighbourhood. (*buurt code*)
    neighbourhood: :class:`str` | :data:`None`
        The neighbourhood. (*buurt naam*)
    district_code: :class:`str` | :data:`None`
        The code of the district. (*wijk code*)
    district: :class:`str` | :data:`None`
        The district. (*wijk naam*)
    municipality_code: :class:`str` | :data:`None`
        The code of the municipality. (*gemeente code*)
    municipality: :class:`str` | :data:`None`
        The municipality. (*gemeente naam*)
    province_code: :class:`str` | :data:`None`
        The code of the province. (*provincie code*)
    province: :class:`str` | :data:`None`
        The province. (*provincie naam*)
    country_code: :class:`str` | :data:`None`
        The country code. (*land code*)
    country: :class:`str` | :data:`None`
        The country. (*land naam*)
    """

    id = field(str, "Id")
    street = field(str, "Straatnaam")
    house_number = field(int, "Huisnummer")
    house_number_addition = field(str, "HuisnummerToevoeging")
    postcode = field(str, "Postcode")
    city_code = field(str, "WoonplaatsCode")
    city = field(str, "WoonplaatsNaam")
    neighbourhood_code = field(str, "BuurtCode")
    neighbourhood = field(str, "BuurtNaam")
    district_code = field(str, "WijkCode")
    district = field(str, "WijkNaam")
    municipality_code = field(str, "GemeenteCode")
    municipality = field(str, "GemeenteNaam")
    province_code = field(str, "ProvincieCode")
    province = field(str, "ProvincieNaam")
    country_code = field(str, "LandCode")
    country = field(str, "LandNaam")


class ContactDetails(Model):
    """A person's e-mail addresses and phone numbers (*contactgegevens*).

    Attributes
    ----------
    email: :class:`str` | :data:`None`
        The main e-mail address. (*emailadres*)
    email_status: :class:`str` | :data:`None`
        Whether the main e-mail address has been verified. (*emailadres status code*)
    cc_email: :class:`str` | :data:`None`
        An e-mail address that receives copies of messages. (*emailadres cc*)
    cc_email_status: :class:`str` | :data:`None`
        Whether the copy e-mail address has been verified. (*emailadres cc status code*)
    backup_email: :class:`str` | :data:`None`
        The backup e-mail address, used for multi-factor authentication. (*emailadres backup*)
    backup_email_status: :class:`str` | :data:`None`
        Whether the backup e-mail address has been verified. (*emailadres backup status code*)
    phone: :class:`str` | :data:`None`
        The main phone number. (*telefoonnummer*)
    phone_status: :class:`str` | :data:`None`
        Whether the main phone number has been verified. (*telefoonnummer status code*)
    phone_2: :class:`str` | :data:`None`
        The second phone number. (*telefoonnummer 2*)
    phone_2_status: :class:`str` | :data:`None`
        Whether the second phone number has been verified. (*telefoonnummer 2 status code*)
    """

    email = field(str, "Emailadres")
    email_status = field(str, "EmailadresStatusCode")
    cc_email = field(str, "EmailadresCC")
    cc_email_status = field(str, "EmailadresCCStatusCode")
    backup_email = field(str, "EmailadresBackup")
    backup_email_status = field(str, "EmailadresBackupStatusCode")
    phone = field(str, "Telefoonnummer")
    phone_status = field(str, "TelefoonnummerStatusCode")
    phone_2 = field(str, "Telefoonnummer2")
    phone_2_status = field(str, "Telefoonnummer2StatusCode")


class Income(Model):
    """A person's income (*inkomen*).

    Attributes
    ----------
    gross_yearly_income: :class:`float` | :data:`None`
        The gross yearly income. (*bruto jaarinkomen*)
    source: :class:`str` | :data:`None`
        Where the income data came from, such as the tax authority. (*bron*)
    statement_type_code: :class:`str` | :data:`None`
        The code of the type of income statement. (*inkomensverklaring code*)
    statement_type: :class:`str` | :data:`None`
        The type of income statement. (*inkomensverklaring*)
    changed_at: :class:`str` | :data:`None`
        When the income was last changed, as an ISO 8601 string. (*mutatiedatum*)
    year: :class:`int` | :data:`None`
        The year the income is for. (*jaar*)
    description: :class:`str` | :data:`None`
        A description of the income. (*omschrijving*)
    documents: :class:`str` | :data:`None`
        The documents that prove the income. (*inkomensdocumenten*)
    needs_update: :class:`bool`
        Whether the income must be updated. (*moet gewijzigd*)
    chosen_source: :class:`str` | :data:`None`
        How the person chose to provide their income. (*keuze bron inkomen*)
    """

    gross_yearly_income = field(float, "BrutoJaarinkomen")
    source = field(str, "Bron")
    statement_type_code = field(str, "InkomensverklaringCode")
    statement_type = field(str, "Inkomensverklaring")
    changed_at = field(str, "Mutatiedatum")
    year = field(int, "Jaar")
    description = field(str, "Omschrijving")
    documents = field(str, "Inkomensdocumenten")
    needs_update = field(bool, "MoetGewijzigd", default=False)
    chosen_source = field(str, "KeuzeBronInkomen")


class VSHIncome(Model):
    """The income used to check whether a person qualifies for mid-rent housing.

    Mid-rent housing is also called ``vrije sector huur`` (VSH).

    Attributes
    ----------
    year: :class:`int` | :data:`None`
        The year the income is for. (*jaar*)
    amount: :class:`float` | :data:`None`
        The yearly income. (*bedrag*)
    is_known: :class:`bool`
        Whether the income is known. (*inkomen bekend*)
    """

    year = field(int, "Jaar")
    amount = field(float, "Bedrag")
    is_known = field(bool, "InkomenBekend", default=False)


class Person(Model):
    """A person in the household.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The person's ID. (*natuurlijk persoon id*)
    initials: :class:`str` | :data:`None`
        The initials. (*voorletters*)
    surname_prefix: :class:`str` | :data:`None`
        The surname prefix, such as ``van der``. (*tussenvoegsel*)
    surname: :class:`str` | :data:`None`
        The surname. (*achternaam*)
    first_name: :class:`str` | :data:`None`
        The first name the person goes by. (*roepnaam*)
    gender: :class:`str` | :data:`None`
        The gender. (*geslacht*)
    date_of_birth: :class:`str` | :data:`None`
        The date of birth, as an ISO 8601 string. (*geboortedatum*)
    allows_research_use: :class:`bool`
        Whether the person agreed to their data being used for research and analysis. (*gebruikgegevens oen a*)
    registered_at: :class:`str` | :data:`None`
        The date the person registered, as an ISO 8601 string. (*inschrijfdatum*)
    corrected_registered_at: :class:`str` | :data:`None`
        The corrected registration date, as an ISO 8601 string. (*gecorrigeerde inschrijfdatum*)
    has_verified_details: :class:`bool`
        Whether the personal details have been verified. (*heeft gevalideerde persoonsgegevens*)
    has_verified_address: :class:`bool`
        Whether the address has been verified. (*heeft gevalideerd woonadres*)
    has_verified_income: :class:`bool`
        Whether the income has been verified. (*heeft gevalideerd inkomen*)
    qualifies_for_social_rent: :class:`bool`
        Whether the income allows social rent housing. (*is inkomen sociaal ok*)
    qualifies_for_mid_rent: :class:`bool`
        Whether the income allows mid-rent housing. (*is inkomen vsh ok*)
    address: :class:`ResidentialAddress`
        The address the person lives at. (*woonadres*)
    contact: :class:`ContactDetails`
        The e-mail addresses and phone numbers. (*contactgegevens*)
    income: :class:`Income`
        The income. (*inkomen*)
    mid_rent_income: :class:`VSHIncome`
        The income used for mid-rent housing. (*inkomen vsh*)
    """

    id = field(str, "NatuurlijkPersoonId")
    initials = field(str, "Voorletters")
    surname_prefix = field(str, "Tussenvoegsel")
    surname = field(str, "Achternaam")
    first_name = field(str, "Roepnaam")
    gender = field(str, "Geslacht")
    date_of_birth = field(str, "Geboortedatum")
    allows_research_use = field(bool, "GebruikgegevensOenA", default=False)
    registered_at = field(str, "Inschrijfdatum")
    corrected_registered_at = field(str, "GecorrigeerdeInschrijfdatum")
    has_verified_details = field(bool, "HeeftGevalideerdePersoonsgegevens", default=False)
    has_verified_address = field(bool, "HeeftGevalideerdWoonadres", default=False)
    has_verified_income = field(bool, "HeeftGevalideerdInkomen", default=False)
    qualifies_for_social_rent = field(bool, "IsInkomenSociaalOK", default=False)
    qualifies_for_mid_rent = field(bool, "IsInkomenVshOK", default=False)
    address = Nested(ResidentialAddress, "Woonadres")
    contact = Nested(ContactDetails, "Contactgegevens")
    income = Nested(Income, "Inkomen")
    mid_rent_income = Nested(VSHIncome, "InkomenVSH")


class ExternalLink(Model):
    """A link between the account and another organisation, such as Woonmatch.

    Attributes
    ----------
    organisation: :class:`str` | :data:`None`
        The organisation. (*organisatie koppeling*)
    status: :class:`str` | :data:`None`
        The status of the link. (*status koppeling*)
    started_at: :class:`str` | :data:`None`
        When the link started, as an ISO 8601 string. (*begindatum koppeling*)
    """

    organisation = field(str, "OrganisatieKoppeling")
    status = field(str, "StatusKoppeling")
    started_at = field(str, "BegindatumKoppeling")


class PersonalDetails(Model):
    """The personal details of the account's main applicant.

    Attributes
    ----------
    person: :class:`Person`
        The main applicant's details. (*natuurlijk persoon gegevens*)
    result: :class:`Result`
        Whether fetching the details succeeded. (*result huis houden*)
    is_qii_processed: :class:`bool`
        Whether income data from Qii has been processed. (*is qii verwerkt*)
    qii_result: :class:`Result`
        Whether fetching the Qii data succeeded. (*result qii*)
    woonmatch_link: :class:`ExternalLink`
        The link with Woonmatch. (*woonmatch koppeling*)
    is_mid_rent_registration: :class:`bool`
        Whether the account is registered for mid-rent housing. (*is vrije sector inschrijving*)
    """

    person = Nested(Person, "NatuurlijkPersoonGegevens")
    result = Nested(Result, "ResultHuisHouden")
    is_qii_processed = field(bool, "IsQiiVerwerkt", default=False)
    qii_result = Nested(Result, "ResultQii")
    woonmatch_link = Nested(ExternalLink, "WoonmatchKoppeling")
    is_mid_rent_registration = field(bool, "IsVrijeSectorInschrijving", default=False)


class Configuration(Model):
    """The registration settings of a region.

    Attributes
    ----------
    region_id: :class:`str` | :data:`None`
        The ID of the region. (*samenwerkingsverband id*)
    registration_fee: :class:`str` | :data:`None`
        The registration fee, as a decimal string. (*inschrijfkosten*)
    renewal_fee: :class:`str` | :data:`None`
        The yearly renewal fee, as a decimal string. (*verlengingsfkosten*)
    minimum_age_months: :class:`int` | :data:`None`
        The minimum age to register, in months. (*minimale leeftijd in maanden*)
    has_mid_rent: :class:`bool`
        Whether the region offers mid-rent housing. (*heeft vrije sector*)
    """

    region_id = field(str, "SamenwerkingsverbandId")
    registration_fee = field(str, "Inschrijfkosten")
    renewal_fee = field(str, "Verlengingsfkosten")
    minimum_age_months = field(int, "MinimaleLeeftijdInMaanden")
    has_mid_rent = field(bool, "HeeftVrijeSector", default=False)


class ConfigurationResponse(Model):
    """The registration settings of a region.

    Attributes
    ----------
    can_verify_online: :class:`bool`
        Whether personal details can be verified online. (*is valideren beschikbaar*)
    configuration: :class:`Configuration`
        The settings. (*configuratie*)
    """

    can_verify_online = field(bool, "IsValiderenBeschikbaar", default=False)
    configuration = Nested(Configuration, "Configuratie")


class Household(Model):
    """The account's household (*huishouden*).

    Attributes
    ----------
    main_applicant_id: :class:`str` | :data:`None`
        The main applicant's ID. (*natuurlijk persoon id*)
    username: :class:`str` | :data:`None`
        The account's username. (*gebruikersnaam*)
    id: :class:`str` | :data:`None`
        The household's ID. (*relatiegroep id*)
    adult_count: :class:`int` | :data:`None`
        The number of adults. (*aantal volwassenen*)
    child_count: :class:`int` | :data:`None`
        The number of children. (*aantal kinderen*)
    combined_income: :class:`float` | :data:`None`
        The combined yearly income of the household. (*verzamel inkomen*)
    combined_mid_rent_income: :class:`float` | :data:`None`
        The combined yearly income used for mid-rent housing. (*verzamel inkomen vsh*)
    has_combined_mid_rent_income: :class:`bool`
        Whether the combined income for mid-rent housing is known. (*heeft verzamel inkomen vsh*)
    can_remove_co_applicant: :class:`bool`
        Whether the co-applicant can be removed. (*is verwijderen medeaanvrager toegestaan*)
    is_partly_verified: :class:`bool`
        Whether some of the household's details have been verified. (*is huishouden deels gevalideerd*)
    is_fully_verified: :class:`bool`
        Whether all of the household's details have been verified. (*is huishouden volledig gevalideerd*)
    main_applicant: :class:`Person`
        The main applicant. (*hoofdaanvrager*)
    co_applicant: :class:`Person`
        The co-applicant, such as a partner. (*medeaanvrager*)
    other_adults: list[:class:`Person`]
        The other adults. (*overige volwassenen*)
    children: list[:class:`Person`]
        The children. (*kinderen*)
    """

    main_applicant_id = field(str, "NatuurlijkPersoonId")
    username = field(str, "Gebruikersnaam")
    id = field(str, "RelatiegroepId")
    adult_count = field(int, "AantalVolwassenen")
    child_count = field(int, "AantalKinderen")
    combined_income = field(float, "VerzamelInkomen")
    combined_mid_rent_income = field(float, "VerzamelInkomenVSH")
    has_combined_mid_rent_income = field(bool, "HeeftVerzamelInkomenVSH", default=False)
    can_remove_co_applicant = field(bool, "IsVerwijderenMedeaanvragerToegestaan", default=False)
    is_partly_verified = field(bool, "IsHuishoudenDeelsGevalideerd", default=False)
    is_fully_verified = field(bool, "IsHuishoudenVolledigGevalideerd", default=False)
    main_applicant = Nested(Person, "Hoofdaanvrager")
    co_applicant = Nested(Person, "Medeaanvrager")
    other_adults = Items(Person, "OverigeVolwassenen")
    children = Items(Person, "Kinderen")


class _HouseholdWrapper(Model):
    household = Nested(Household, "Huishouden")
    link = Nested(ExternalLink, "OvereenkomstKoppeling")


class HouseholdResponse(Model):
    """The account's household and income.

    Attributes
    ----------
    result: :class:`Result`
        Whether fetching the household succeeded. (*result huishouden*)
    is_qii_processed: :class:`bool`
        Whether income data from Qii has been processed. (*is qii verwerkt*)
    qii_result: :class:`Result`
        Whether fetching the Qii data succeeded. (*result qii*)
    can_edit_qii_income: :class:`bool`
        Whether the income from Qii can be changed by hand. (*qii handmatig aanpassen*)
    """

    _wrapper = Nested(_HouseholdWrapper, "Huishouden")
    result = Nested(Result, "ResultHuishouden")
    is_qii_processed = field(bool, "IsQiiVerwerkt", default=False)
    qii_result = Nested(Result, "ResultQii")
    can_edit_qii_income = field(bool, "QiiHandmatigAanpassen", default=False)

    @property
    def household(self) -> Household:
        """The household.

        Returns
        -------
        :class:`Household`
            The household members and their incomes.
        """
        return self._wrapper.household

    @property
    def link(self) -> ExternalLink:
        """The link between the household and another organisation.

        Returns
        -------
        :class:`ExternalLink`
            The organisation, the status of the link and when it started.
        """
        return self._wrapper.link


class CodeName(Model):
    """An option with a code and a name.

    Attributes
    ----------
    code: :class:`str` | :data:`None`
        The option's code.
    name: :class:`str` | :data:`None`
        The option's name. (*naam*)
    """

    code = field(str, "Code")
    name = field(str, "Naam")


class _Owner(Model):
    id = field(str, "VestigingId")
    name = field(str, "VestigingNaam")


class CurrentHousing(Model):
    """The account's current housing situation.

    Attributes
    ----------
    housing_type: :class:`CodeName`
        The type of home. (*eenheid detailsoort*)
    rooms: :class:`int` | :data:`None`
        The number of rooms. (*kamers aantal*)
    total_area: :class:`str` | :data:`None`
        The total floor area in square metres, as a decimal string. (*totale oppervlakte*)
    floor: :class:`int` | :data:`None`
        The floor the home is on. (*etage*)
    frees_up_home: :class:`bool`
        Whether moving frees up a self-contained home. (*laat zelfstandig eenheid achter*)
    contract_type: :class:`CodeName`
        The type of contract, such as rent or ownership. (*overeenkomstsoort*)
    contract_subtype: :class:`CodeName`
        The detailed type of contract. (*overeenkomst detail soort*)
    social_rent: :class:`CodeName`
        Whether the home is a social rent home. (*socialehuur indicator*)
    monthly_cost: :class:`float` | :data:`None`
        The rent or mortgage per month. (*overeenkomst bedrag*)
    contract_start_date: :class:`str` | :data:`None`
        When the contract started, as an ISO 8601 string. (*overeenkomst begindatum*)
    municipal_registration_date: :class:`str` | :data:`None`
        When the person was registered at the address in the municipal records (BRP), as an ISO 8601 string. (*brp
        inschrijfdatum*)
    """

    _landlord = Nested(_Owner, "EigenaarVestiging")
    housing_type = Nested(CodeName, "EenheidDetailsoort")
    rooms = field(int, "KamersAantal")
    total_area = field(str, "TotaleOppervlakte")
    floor = field(int, "Etage")
    frees_up_home = field(bool, "LaatZelfstandigEenheidAchter", default=False)
    contract_type = Nested(CodeName, "Overeenkomstsoort")
    contract_subtype = Nested(CodeName, "OvereenkomstDetailSoort")
    social_rent = Nested(CodeName, "SocialehuurIndicator")
    monthly_cost = field(float, "OvereenkomstBedrag")
    contract_start_date = field(str, "OvereenkomstBegindatum")
    municipal_registration_date = field(str, "BRPInschrijfdatum")

    @property
    def landlord_id(self) -> str | None:
        """The ID of the landlord's office.

        Returns
        -------
        :class:`str` | :data:`None`
            The ID, or :data:`None` if the landlord is not known.
        """
        return self._landlord.id

    @property
    def landlord_name(self) -> str | None:
        """The landlord's name.

        Returns
        -------
        :class:`str` | :data:`None`
            The name, or :data:`None` if the landlord is not known.
        """
        return self._landlord.name


class _CurrentHousingWrapper(Model):
    housing = Nested(CurrentHousing, "HuidigeWoonsituatie")
    contract_subtypes = Items(CodeName, "lstOvereenkomstDetailSoort")


class CurrentHousingResponse(Model):
    """The account's current housing situation.

    Attributes
    ----------
    result: :class:`Result`
        Whether DAK handled the request successfully.
    """

    _response = Nested(_CurrentHousingWrapper, "Response")
    result = Nested(Result, "Result")

    @property
    def housing(self) -> CurrentHousing:
        """The current housing situation.

        Returns
        -------
        :class:`CurrentHousing`
            The landlord, type of home, number of rooms, type of contract and rent.
        """
        return self._response.housing

    @property
    def contract_subtypes(self) -> list[CodeName]:
        """The detailed types of contract that can be chosen when changing the housing situation.

        Returns
        -------
        list[:class:`CodeName`]
            Each type of contract with its code and name.
        """
        return self._response.contract_subtypes


class PriorityRule(Model):
    """One rule of a priority scheme, such as an urgency for a municipality.

    Attributes
    ----------
    kind: :class:`CodeName`
        The kind of priority. (*voorrang detail soort*)
    subkind: :class:`CodeName`
        The detailed kind of priority. (*voorrang sub detail soort*)
    name: :class:`str` | :data:`None`
        The rule's name. (*naam*)
    description: :class:`str` | :data:`None`
        What the rule means, such as where it applies. (*omschrijving*)
    start_date: :class:`str` | :data:`None`
        The date the rule starts, as an ISO 8601 string. (*begindatum*)
    end_date: :class:`str` | :data:`None`
        The date the rule ends, as an ISO 8601 string. (*einddatum*)
    is_active: :class:`bool`
        Whether the rule is active. (*is actief*)
    is_editable: :class:`bool`
        Whether the rule can be changed. (*is wijzigbaar*)
    is_assigned: :class:`bool`
        Whether the rule has been given to the account. (*is toegewezen*)
    """

    kind = Nested(CodeName, "VoorrangDetailSoort")
    subkind = Nested(CodeName, "VoorrangSubDetailSoort")
    name = field(str, "Naam")
    description = field(str, "Omschrijving")
    start_date = field(str, "Begindatum")
    end_date = field(str, "Einddatum")
    is_active = field(bool, "IsActief", default=False)
    is_editable = field(bool, "IsWijzigbaar", default=False)
    is_assigned = field(bool, "IsToegewezen", default=False)


class PrioritySet(Model):
    """A priority scheme, such as an urgency, with its rules.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The scheme's ID.
    name: :class:`str` | :data:`None`
        The scheme's name. (*naam*)
    description: :class:`str` | :data:`None`
        The scheme's description. (*omschrijving*)
    is_exclusive: :class:`bool`
        Whether the scheme cannot be combined with others. (*is exclusief*)
    is_visible: :class:`bool`
        Whether the scheme is shown to house seekers. (*is zichtbaar voor wozo*)
    is_editable: :class:`bool`
        Whether house seekers can change the scheme. (*is wijzigbaar door wozo*)
    is_start_date_editable: :class:`bool`
        Whether house seekers can change the start date. (*is ingangsdatum wijzigbaar door wozo*)
    rules: list[:class:`PriorityRule`]
        The scheme's rules. (*voorrangsregelingen*)
    """

    id = field(str, "Id")
    name = field(str, "Naam")
    description = field(str, "Omschrijving")
    is_exclusive = field(bool, "IsExclusief", default=False)
    is_visible = field(bool, "IsZichtbaarVoorWozo", default=False)
    is_editable = field(bool, "IsWijzigbaarDoorWozo", default=False)
    is_start_date_editable = field(bool, "IsIngangsdatumWijzigbaarDoorWozo", default=False)
    rules = Items(PriorityRule, "Voorrangsregelingen")


class _PrioritySetItem(Model):
    priority_set = Nested(PrioritySet, "VoorrangsregelingenSets")


class _PrioritySets(Model):
    urgencies = Items(_PrioritySetItem, "Urgentie")
    indications = Items(_PrioritySetItem, "Indicatie")
    bindings = Items(_PrioritySetItem, "Binding")
    groups = Items(_PrioritySetItem, "Groep")


class PrioritySchemes(Model):
    """The account's priority schemes (*voorrangsregelingen*).

    These give the account priority for some listings.

    Attributes
    ----------
    result: :class:`Result`
        Whether DAK handled the request successfully.
    """

    _sets = Nested(_PrioritySets, "Voorrangsregelingen")
    result = Nested(Result, "Result")

    @property
    def urgencies(self) -> list[PrioritySet]:
        """The account's urgencies (*urgentie*), such as for medical or social reasons.

        Returns
        -------
        list[:class:`PrioritySet`]
            Each urgency with its rules. An empty list if the account has none.
        """
        return [item.priority_set for item in self._sets.urgencies]

    @property
    def indications(self) -> list[PrioritySet]:
        """The account's indications (*indicatie*).

        Returns
        -------
        list[:class:`PrioritySet`]
            Each indication with its rules. An empty list if the account has none.
        """
        return [item.priority_set for item in self._sets.indications]

    @property
    def bindings(self) -> list[PrioritySet]:
        """The account's bindings (*binding*), such as to a municipality.

        Returns
        -------
        list[:class:`PrioritySet`]
            Each binding with its rules. An empty list if the account has none.
        """
        return [item.priority_set for item in self._sets.bindings]

    @property
    def groups(self) -> list[PrioritySet]:
        """The groups (*groep*) the account belongs to, such as students.

        Returns
        -------
        list[:class:`PrioritySet`]
            Each group with its rules. An empty list if the account has none.
        """
        return [item.priority_set for item in self._sets.groups]


class ProfilePanel(Model):
    """One section of the account's profile.

    Attributes
    ----------
    id: :class:`int` | :data:`None`
        The section's ID. (*profiel panelen id*)
    name: :class:`str` | :data:`None`
        The section's name. (*weer te geven naam*)
    internal_name: :class:`str` | :data:`None`
        The section's internal name. (*wrb naam*)
    description: :class:`str` | :data:`None`
        The section's description. (*wrb omschrijving*)
    is_complete: :class:`bool`
        Whether the section is complete. (*is compleet*)
    is_coming_soon: :class:`bool`
        Whether the section will be available soon. (*binnenkort beschikbaar*)
    """

    id = field(int, "ProfielPanelenId")
    name = field(str, "WeerTeGevenNaam")
    internal_name = field(str, "WRBNaam")
    description = field(str, "WRBOmschrijving")
    is_complete = field(bool, "IsCompleet", default=False)
    is_coming_soon = field(bool, "BinnenkortBeschikbaar", default=False)


class AccountStatus(Model):
    """Which sections of the account's profile are complete.

    Attributes
    ----------
    sections: list[:class:`ProfilePanel`]
        The sections of the profile. (*profiel panelen visualisatie list*)
    offers_qii: :class:`bool`
        Whether the profile offers sharing income data through Qii. (*qii in profiel*)
    result: :class:`Result`
        Whether DAK handled the request successfully.
    """

    sections = Items(ProfilePanel, "ProfielPanelenVisualisatieList")
    offers_qii = field(bool, "QiiInProfiel", default=False)
    result = Nested(Result, "Result")


class OpenPayment(Model):
    """A payment the account has to make, such as a registration or renewal fee.

    Attributes
    ----------
    is_due: :class:`bool`
        Whether a payment is due. (*openstaande betaling*)
    is_processing: :class:`bool`
        Whether a payment is being processed. (*heeft betaling in behandeling*)
    amount: :class:`str` | :data:`None`
        The amount due, as a decimal string. (*bedrag*)
    is_renewal_fee: :class:`bool`
        Whether the payment is for renewing the registration. (*is verlengings kosten*)
    is_renewal_paid: :class:`bool`
        Whether the renewal has been paid. (*is betaalde verlenging*)
    """

    is_due = field(bool, "OpenstaandeBetaling", default=False)
    is_processing = field(bool, "HeeftBetalingInBehandeling", default=False)
    amount = field(str, "Bedrag")
    is_renewal_fee = field(bool, "IsVerlengingsKosten", default=False)
    is_renewal_paid = field(bool, "IsBetaaldeVerlenging", default=False)


class Payment(Model):
    """One payment the account made.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The payment's ID.
    period_start: :class:`str` | :data:`None`
        The start of the period paid for, as an ISO 8601 string. (*betaalperiode begin datum*)
    period_end: :class:`str` | :data:`None`
        The end of the period paid for, as an ISO 8601 string. (*betaalperiode eind datum*)
    amount: :class:`str` | :data:`None`
        The amount, as a decimal string. (*bedrag*)
    method: :class:`str` | :data:`None`
        How it was paid, such as by direct debit. (*betaalwijze*)
    requested_at: :class:`str` | :data:`None`
        When the payment request was sent, as an ISO 8601 string. (*verzoek verzonden datum tijd*)
    processed_at: :class:`str` | :data:`None`
        When the payment was processed, as an ISO 8601 string. (*betaling verwerkt datum tijd*)
    invoice_number: :class:`str` | :data:`None`
        The invoice number of the payment provider (Buckaroo). (*buckaroo factuur nummer*)
    status_code: :class:`str` | :data:`None`
        The code of the payment's status. (*betaal status code*)
    status: :class:`str` | :data:`None`
        The payment's status. (*betaal status*)
    description: :class:`str` | :data:`None`
        What the payment was for. (*omschrijving*)
    """

    id = field(str, "Id")
    period_start = field(str, "BetaalperiodeBeginDatum")
    period_end = field(str, "BetaalperiodeEindDatum")
    amount = field(str, "Bedrag")
    method = field(str, "Betaalwijze")
    requested_at = field(str, "VerzoekVerzondenDatumTijd")
    processed_at = field(str, "BetalingVerwerktDatumTijd")
    invoice_number = field(str, "BuckarooFactuurNummer")
    status_code = field(str, "BetaalStatusCode")
    status = field(str, "BetaalStatus")
    description = field(str, "Omschrijving")


class PaymentInformation(Model):
    """The account's payment method and history.

    Attributes
    ----------
    next_invoice_date: :class:`str` | :data:`None`
        The date of the next invoice, as an ISO 8601 string. (*volgende factuurdatum*)
    method: :class:`str` | :data:`None`
        The payment method, such as direct debit. (*betaalwijze*)
    payments: list[:class:`Payment`]
        The payments made. (*betalingen*)
    """

    next_invoice_date = field(str, "VolgendeFactuurdatum")
    method = field(str, "Betaalwijze")
    payments = Items(Payment, "Betalingen")


class PaymentsResponse(Model):
    """The account's payment information.

    Attributes
    ----------
    information: :class:`PaymentInformation`
        The payment method and history. (*betaal informatie*)
    result: :class:`Result`
        Whether DAK handled the request successfully.
    """

    information = Nested(PaymentInformation, "BetaalInformatie")
    result = Nested(Result, "Result")


class Document(Model):
    """A document uploaded to the account.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The document's ID. (*document id*)
    title: :class:`str` | :data:`None`
        The title. (*titel*)
    filename: :class:`str` | :data:`None`
        The file name. (*documentnaam*)
    mime_type: :class:`str` | :data:`None`
        The file's MIME type. (*mimetype*)
    received_at: :class:`str` | :data:`None`
        When DAK received the document, as an ISO 8601 string. (*ontvangst datum tijd*)
    status: :class:`str` | :data:`None`
        The document's status, such as whether it has been checked.
    """

    id = field(str, "DocumentId")
    title = field(str, "Titel")
    filename = field(str, "Documentnaam")
    mime_type = field(str, "Mimetype")
    received_at = field(str, "OntvangstDatumTijd")
    status = field(str, "Status")


class DocumentType(Model):
    """A type of document, such as proof of income, with the documents uploaded for it.

    Attributes
    ----------
    code: :class:`str` | :data:`None`
        The type's code. Pass it to :meth:`AccountClient.upload_document`. (*benodigdheid code*)
    name: :class:`str` | :data:`None`
        The type's name. (*benodigdheid naam*)
    documents: list[:class:`Document`]
        The documents uploaded for this type. (*documenten*)
    """

    code = field(str, "BenodigdheidCode")
    name = field(str, "BenodigdheidNaam")
    documents = Items(Document, "Documenten")


class PersonDocuments(Model):
    """The documents of one household member.

    Attributes
    ----------
    person_id: :class:`str` | :data:`None`
        The person's ID. (*natuurlijk persoon id*)
    has_income_document: :class:`bool`
        Whether the person uploaded proof of income. (*heeft inkomen document*)
    document_types: list[:class:`DocumentType`]
        The types of document, each with its documents. (*documenttypes*)
    """

    person_id = field(str, "NatuurlijkPersoonId")
    has_income_document = field(bool, "HeeftInkomenDocument", default=False)
    document_types = Items(DocumentType, "Documenttypes")


class DocumentsResponse(Model):
    """The documents uploaded to the account, for each household member.

    Attributes
    ----------
    main_applicant: list[:class:`PersonDocuments`]
        The main applicant's documents. (*hoofd aanvrager documenten*)
    co_applicant: list[:class:`PersonDocuments`]
        The co-applicant's documents. (*medeaanvrager documenten*)
    other_adults: list[:class:`PersonDocuments`]
        The other adults' documents. (*overige volwassenen documenten*)
    result: :class:`Result`
        Whether fetching the documents succeeded. (*result document*)
    household_result: :class:`Result`
        Whether fetching the household succeeded. (*result huishouden*)
    """

    main_applicant = Items(PersonDocuments, "HoofdAanvragerDocumenten")
    co_applicant = Items(PersonDocuments, "MedeaanvragerDocumenten")
    other_adults = Items(PersonDocuments, "OverigeVolwassenenDocumenten")
    result = Nested(Result, "ResultDocument")
    household_result = Nested(Result, "ResultHuishouden")
    _household = Nested(_HouseholdWrapper, "Huishouden")

    @property
    def household(self) -> Household:
        """The household.

        Returns
        -------
        :class:`Household`
            The household members and their incomes.
        """
        return self._household.household


class Subscription(Model):
    """A category of personal messages and whether its messages are also sent by e-mail.

    Attributes
    ----------
    code: :class:`str` | :data:`None`
        The category's code. Pass it to :meth:`AccountClient.set_subscription`. (*soort code*)
    name: :class:`str` | :data:`None`
        The category's name. (*naam*)
    email: :class:`str` | :data:`None`
        The e-mail address the messages are sent to.
    is_subscribed: :class:`bool`
        Whether the messages are also sent by e-mail. (*is geabonneerd*)
    """

    code = field(str, "SoortCode")
    name = field(str, "Naam")
    email = field(str, "Email")
    is_subscribed = field(bool, "IsGeabonneerd", default=False)


class SubscriptionsResponse(Model):
    """The account's categories of personal messages.

    Attributes
    ----------
    subscriptions: list[:class:`Subscription`]
        The categories. (*abonnementen*)
    result: :class:`Result`
        Whether DAK handled the request successfully.
    """

    subscriptions = Items(Subscription, "Abonnementen")
    result = Nested(Result, "Result")


class PointsLine(Model):
    """One line of the points breakdown: an event that added or removed points.

    Attributes
    ----------
    code: :class:`str` | :data:`None`
        The code of the event.
    name: :class:`str` | :data:`None`
        The event, such as ``Intrekken reactie`` (withdrawing a reaction). (*naam*)
    date: :class:`str` | :data:`None`
        The date of the event, as an ISO 8601 string. (*datum*)
    start_date: :class:`str` | :data:`None`
        The date the points started counting, as an ISO 8601 string. (*begindatum*)
    text_line_1: :class:`str` | :data:`None`
        The first line of text the website shows. (*tekstregel 1*)
    text_line_2: :class:`str` | :data:`None`
        The second line of text the website shows. (*tekstregel 2*)
    search_points: :class:`float` | :data:`None`
        The change in search points. (*zoekpunten*)
    situation_points: :class:`float` | :data:`None`
        The change in situation points. (*situatiepunten*)
    starter_points: :class:`float` | :data:`None`
        The change in starter points. (*startpunten*)
    icon: :class:`int` | :data:`None`
        The number of the icon the website shows. (*icoon*)
    """

    code = field(str, "Code")
    name = field(str, "Naam")
    date = field(str, "Datum")
    start_date = field(str, "Begindatum")
    text_line_1 = field(str, "Tekstregel1")
    text_line_2 = field(str, "Tekstregel2")
    search_points = field(float, "Zoekpunten")
    situation_points = field(float, "Situatiepunten")
    starter_points = field(float, "Startpunten")
    icon = field(int, "Icoon")


class _PointsLineItem(Model):
    line = Nested(PointsLine, "Soort")


class PointsTab(Model):
    """The points breakdown of one registration.

    Attributes
    ----------
    registration_id: :class:`int` | :data:`None`
        The ID of the registration. (*relatie context id*)
    points_type_id: :class:`int` | :data:`None`
        The ID of the type of points. (*punten context id*)
    tab_id: :class:`int` | :data:`None`
        The ID of the tab the website shows it on. (*tabblad context id*)
    """

    registration_id = field(int, "RelatieContextId")
    points_type_id = field(int, "PuntenContextId")
    tab_id = field(int, "TabbladContextId")
    _items = Items(_PointsLineItem, "LstItems")

    @property
    def lines(self) -> list[PointsLine]:
        """The events that added or removed points.

        Returns
        -------
        list[:class:`PointsLine`]
            Each event, such as reacting to a listing, with the points it added or removed.
        """
        return [item.line for item in self._items]


class PointsLinesResponse(Model):
    """The points breakdown of each of the account's registrations.

    Attributes
    ----------
    registrations: list[:class:`PointsTab`]
        The breakdown of each registration. (*puntendashboardregels*)
    result: :class:`Result`
        Whether DAK handled the request successfully.
    """

    registrations = Items(PointsTab, "Puntendashboardregels")
    result = Nested(Result, "Result")


class Registration(Model):
    """One of the account's registrations in a region (*inschrijving*).

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The registration's ID.
    user_id: :class:`int` | :data:`None`
        The ID of the login account. (*user id*)
    person_id: :class:`str` | :data:`None`
        The person's ID. (*natuurlijk persoon id*)
    region_id: :class:`str` | :data:`None`
        The ID of the region. (*samenwerkingsverband id*)
    is_region_active: :class:`bool`
        Whether the region is active. (*is actief samenwerkingsverband*)
    expires_at: :class:`str` | :data:`None`
        The date the registration expires unless renewed, as an ISO 8601 string. (*verloop datum*)
    product_code: :class:`str` | :data:`None`
        The kind of registration, such as ``REG``. (*product code*)
    main_applicant_id: :class:`str` | :data:`None`
        The main applicant's ID. (*hoofdaanvrager*)
    """

    id = field(str, "Id")
    user_id = field(int, "UserId")
    person_id = field(str, "NatuurlijkPersoonId")
    region_id = field(str, "SamenwerkingsverbandId")
    is_region_active = field(bool, "IsActiefSamenwerkingsverband", default=False)
    expires_at = field(str, "VerloopDatum")
    product_code = field(str, "ProductCode")
    main_applicant_id = field(str, "Hoofdaanvrager")


class MFADetails(Model):
    """Whether multi-factor authentication is available and turned on.

    Attributes
    ----------
    is_enabled: :class:`bool`
        Whether multi-factor authentication is turned on for the account. (*is actief voor gebruiker*)
    is_available: :class:`bool`
        Whether multi-factor authentication is available. (*is actief mfa*)
    """

    is_enabled = field(bool, "IsActief_VoorGebruiker", default=False)
    is_available = field(bool, "IsActief_MFA", default=False)


class DisplayPreferences(Model):
    """The account's display preferences.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The preferences' ID.
    user_id: :class:`int` | :data:`None`
        The ID of the login account. (*user id*)
    skip_hide_confirmation: :class:`bool`
        Whether the account chose not to be asked again before hiding a listing. (*is verbergen vraag niet weer*)
    is_dak_plus: :class:`bool`
        Whether the preferences are for the DAK Plus website. (*is dakp*)
    is_dak: :class:`bool`
        Whether the preferences are for the DAK website. (*is dak*)
    is_map_hidden: :class:`bool`
        Whether the map is hidden in the listings overview. (*is kaart verborgen*)
    uses_extended_search: :class:`bool`
        Whether extended search is used. (*is uitgebreid zoeken*)
    filters_by_wishes: :class:`bool`
        Whether listings are filtered by the account's housing wishes. (*is woonwens filter*)
    last_login: :class:`str` | :data:`None`
        When the account last logged in, as an ISO 8601 string. (*laatste inlog*)
    last_review: :class:`str` | :data:`None`
        When the account last left a review, as an ISO 8601 string. (*laatste review*)
    skip_mijn_overheid_prompt: :class:`bool`
        Whether the account chose not to be asked about MijnOverheid again. (*is mijn overheid vraag niet weer*)
    skip_phone_verification_prompt: :class:`bool`
        Whether the account chose not to be asked to verify its phone number again. (*is tel validatie niet meer
        tonen*)
    skip_app_prompt: :class:`bool`
        Whether the account chose not to be asked to download the app again. (*is app download vraag niet weer*)
    """

    id = field(str, "Id")
    user_id = field(int, "UserId")
    skip_hide_confirmation = field(bool, "IsVerbergenVraagNietWeer", default=False)
    is_dak_plus = field(bool, "IsDAKP", default=False)
    is_dak = field(bool, "IsDAK", default=False)
    is_map_hidden = field(bool, "IsKaartVerborgen", default=False)
    uses_extended_search = field(bool, "IsUitgebreidZoeken", default=False)
    filters_by_wishes = field(bool, "IsWoonwensFilter", default=False)
    last_login = field(str, "LaatsteInlog")
    last_review = field(str, "LaatsteReview")
    skip_mijn_overheid_prompt = field(bool, "IsMijnOverheidVraagNietWeer", default=False)
    skip_phone_verification_prompt = field(bool, "IsTelValidatieNietMeerTonen", default=False)
    skip_app_prompt = field(bool, "IsAppDownloadVraagNietWeer", default=False)


class User(Model):
    """The account's login details (OutSystems ``User``).

    Attributes
    ----------
    id: :class:`int` | :data:`None`
        The account's ID.
    name: :class:`str` | :data:`None`
        The account's name.
    username: :class:`str` | :data:`None`
        The username.
    email: :class:`str` | :data:`None`
        The e-mail address.
    mobile_phone: :class:`str` | :data:`None`
        The mobile phone number.
    external_id: :class:`str` | :data:`None`
        An ID in an external system, if any.
    creation_date: :class:`str` | :data:`None`
        When the account was created, as an ISO 8601 string.
    last_login: :class:`str` | :data:`None`
        When the account last logged in, as an ISO 8601 string.
    is_active: :class:`bool`
        Whether the account is active.
    """

    id = field(int, "Id")
    name = field(str, "Name")
    username = field(str, "Username")
    email = field(str, "Email")
    mobile_phone = field(str, "MobilePhone")
    external_id = field(str, "External_Id")
    creation_date = field(str, "Creation_Date")
    last_login = field(str, "Last_Login")
    is_active = field(bool, "Is_Active", default=False)


class MutationResult(Model):
    """The outcome of a change to the account's profile.

    Attributes
    ----------
    result: :class:`Result`
        Whether the change succeeded. See also ``is_success``.
    message: :class:`str` | :data:`None`
        A message about the change, for example that it must be verified again. (*profiel mutatie melding*)
    """

    result = Nested(Result, "Result")
    message = field(str, "ProfielMutatieMelding")

    @property
    def is_success(self) -> bool:
        """Whether the change succeeded.

        Returns
        -------
        :class:`bool`
            :data:`True` if the change succeeded.
        """
        return self.result.is_success


class PersonUpdateResult(MutationResult):
    """The outcome of changing a person's details.

    Attributes
    ----------
    person: :class:`Person`
        The saved details.
    notice: :class:`str` | :data:`None`
        A message from DAK about the change. (*melding*)
    """

    person = Nested(Person, "Response")
    notice = field(str, "Melding")


class PasswordChangeResult(Model):
    """The outcome of changing the account's password.

    Attributes
    ----------
    is_current_password_valid: :class:`bool`
        Whether the current password was correct. (*is oud wachtwoord valid*)
    is_changed: :class:`bool`
        Whether the password was changed. See also ``is_success``. (*is succes wijzig*)
    """

    is_current_password_valid = field(bool, "IsOudWachtwoordValid", default=False)
    is_changed = field(bool, "IsSuccesWijzig", default=False)

    @property
    def is_success(self) -> bool:
        """Whether the password was changed.

        Returns
        -------
        :class:`bool`
            :data:`True` if the change succeeded.
        """
        return self.is_changed


class ConsentDetails(Model):
    """What a consent to share data is about, and whether it can be changed.

    Attributes
    ----------
    id: :class:`str` | :data:`None`
        The consent's ID. Pass it to :meth:`AccountClient.set_data_sharing`. (*toestemming id*)
    code: :class:`str` | :data:`None`
        The kind of consent. (*soort code*)
    status_code: :class:`str` | :data:`None`
        The code of the consent's status. (*status code*)
    status: :class:`str` | :data:`None`
        The consent's status. (*status naam*)
    is_editable: :class:`bool`
        Whether the consent can be changed. (*is wijzigen toegestaan*)
    description: :class:`str` | :data:`None`
        What the consent is about. (*omschrijving*)
    question: :class:`str` | :data:`None`
        The question the website asks. (*vraag*)
    note: :class:`str` | :data:`None`
        An extra note. (*opmerking*)
    withdrawal_warning: :class:`str` | :data:`None`
        What withdrawing the consent means. (*waarschuwing bij intrekken*)
    """

    id = field(str, "ToestemmingId")
    code = field(str, "SoortCode")
    status_code = field(str, "StatusCode")
    status = field(str, "StatusNaam")
    is_editable = field(bool, "IsWijzigenToegestaan", default=False)
    description = field(str, "Omschrijving")
    question = field(str, "Vraag")
    note = field(str, "Opmerking")
    withdrawal_warning = field(str, "WaarschuwingBijIntrekken")


class Consent(Model):
    """A consent to share the account's data, and whether it is given.

    Attributes
    ----------
    details: :class:`ConsentDetails`
        What the consent is about. (*haal instemming*)
    is_granted: :class:`bool`
        Whether the consent is given. (*is toestemming verleend*)
    """

    details = Nested(ConsentDetails, "HaalInstemming")
    is_granted = field(bool, "IsToestemmingVerleend", default=False)


class DataSharingResponse(Model):
    """The account's consents to share its data.

    Attributes
    ----------
    consents: list[:class:`Consent`]
        The consents. (*gegevensdeling*)
    result: :class:`Result`
        Whether fetching the consents succeeded.
    """

    consents = Items(Consent, "Gegevensdeling")
    result = Nested(Result, "Result")


class HouseholdRole(Model):
    """A role a household member can have, such as co-applicant or child.

    Get the roles from :meth:`AccountClient.household_roles` instead of guessing their IDs.

    Attributes
    ----------
    id: :class:`int` | :data:`None`
        The role's ID. Pass it to :meth:`AccountClient.update_household_member`.
    label: :class:`str` | :data:`None`
        The role's name.
    order: :class:`int` | :data:`None`
        The position in the list of roles.
    is_active: :class:`bool`
        Whether the role can be chosen.
    name: :class:`str` | :data:`None`
        The role's internal name. (*rol*)
    """

    id = field(int, "Id")
    label = field(str, "Label")
    order = field(int, "Order")
    is_active = field(bool, "Is_Active", default=False)
    name = field(str, "Rol")
