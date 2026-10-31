# TODO

## Unverified account writes

These are implemented but have never been run against a real account. Check each one before relying on it.

- **Role IDs.** `Client.update_personal_details` sends `RelatieRolSoortCodeId=4` for the main applicant (`MAIN_APPLICANT_ROLE_ID` in `client.py`). The value comes from a captured page load. The site resolves the real IDs at runtime from a static entity, so the IDs for the co-applicant, child and other adult are still unknown.
- **Priority-set saves.** `save_bindings`, `save_groups` and `save_indications` send the set record the edit screen holds (`huidigeSetVar`). They assume it has the same shape as `PrioritySetPayload`.
- **Data sharing.** `set_data_sharing` sends `Gegevensdeling` as a flat list of `{ToestemmingId, IsToestemmingVerleend}`. The script builds it from `Struc_VerwerkGegevensdelingList`, so it may need wrapping as `{"Struc_VerwerkGegevensdeling": {...}}`. The item shape of `DataActionHaalGegevensdeling` is also unknown, because the list was empty on the test account.
- **Display settings.** The view names `Instellingen.WeergaveAanbod` and `Instellingen.WeergavePuntenteller` come from the host screens' script names.

## Unknown list item shapes

These lists were empty on the test account. Their element types are guesses, and the real shapes are in the site's `*.model.js`.

- `Voorrangsregelingen.Indicatie`, `Binding` and `Groep` (assumed to match `Urgentie`)
- `Huishouden.Kinderen` and `OverigeVolwassenen` (assumed to be `PersonPayload`)
- `Sancties` and `Gedeelde gegevens`

## Not implemented

| Endpoint | Path | Notes |
|---|---|---|
| Sanctions list | `DAKReusable_CW/Sancties_CW/Sancties/DataActionHaalSanctiesEnRedenen` | Needs `NatuurlijkPersoonId` and `SamenwerkingsverbandId` screen variables. The hash was not in the expected script. |
| Deregistration | `DAKWP/Instellingen/Uitschrijven/ActionUitschrijvenWoningzoekende` (`Locale`, `SamenwerkingsverbandId`, `IsTevensAccountVerwijderen`, `VerificatieCode`) and `ActionVerwerkUitschrijven` (`SamenwerkingsverbandId`, `IsAccountVerwijderen`, `VerificatieCode`) | Deletes the registration and optionally the account. The order of the two steps and how the verification code is sent are unclear. |
| Bank mandate | `DAKWP/Profiel/MachtigingAfgeven/ActionBetaalgegevensAanpassen` (`BankCodeLocal`, `SamenwerkingsverbandId`, `Natuurlijkpersoonid`) | Starts a bank authorisation. `DataActionHaalBanken` lists the banks. |
| Split account | `DAKReusable_CW/Profiel_CW/Splitsen/ActionSplitsen_SplitsingUitvoeren` (`NatuurlijkPersoonId`, `SamenwerkingsverbandId`, `EmailAdresNieuwAccount`) | |
| Add household member with label | `.../NatuurlijkPersoonToevoegenOfWijzigen_CW/ActionNatuurlijkPersoonVerwerkenMetLabel` | Same as `UPDATE_HOUSEHOLD_MEMBER`, plus `BrutoJaarInkomenStart` and `IsQiiVerwerktEnWijzigPersoon`. |
| DigiD validation | `DAKWP/Profiel/PersoonsgegevensValideren/ActionVerwerkGeauthenticeerdPersoon` | Part of the DigiD and MijnOverheid flow (`ActionHaalDigiDEndpoint`, `ActionHaalBvBSNMijnOverheid`). |
| Rental passport | `DAKWP/Profiel/PersoonsgegevensWijzigen/ActionHuurpaspoortVerwerk` (`Locale`, `SamenwerkingsverbandId`, `RelatiegroepStatusCodeId`) | |
| Education | `DAKReusable_CW/Profiel_CW/OpleidingWijzigen_CW/ActionOpleidingVerwerk` / `ActionOpleidingVerwijder` | Not shown in the Amsterdam region. |
| Waiting lists | `DAKReusable_CW/Profiel_CW/RegelingenWijzigen_CW/ActionRegelingenVerwerk` | Not shown in the Amsterdam region. |
| Change e-mail | `DAKWP/Instellingen/WijzigEmailadres/*` | Reads only so far (`ActionAccountBestaat`, `ActionCheckWijzigGebruikersnaam`). |
| Edit-form lookups | `ScreenDataSetGetLanden`, `GetEtages`, `GetVestigingen`, `GetRelatieRolSoortCodes`, `GetDocumentSoorten`, `GetOpleidings*` | Option lists for the edit forms. |

## How to find inputs

Each write action builds its inputs in its `*.mvc.js` script as `var inputs = { Name: OS.DataConversion.ServerDataConverter.to(xIn, OS.DataTypes.DataTypes.Type) }`, followed by `controller.callServerAction("Name", "screenservices/...")`. The scripts are public, and their URLs are listed in `/DAKWP/moduleservices/moduleinfo`. Record fields come from `this.attr(...)` in the `*.model.js` files.
