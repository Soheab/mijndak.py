# mijndak.py

An unofficial Python library for **DAK** (mijndak.nl or woningnet), the website many Dutch regions use for social housing. Log in,
browse listings, react to homes, keep an eye on your points and manage your profile, all from Python.

It's async, fully typed and works with Python 3.12 and later.

> [!WARNING]
> This library talks to the website the same way your browser does. DAK doesn't offer an official API, so things can
> break when they change their site. Reacting to listings automatically may also go against their terms of use. Calling
> `react()` places a **real** reaction on your account.

## Installation

```bash
pip install "mijndak.py[speedups] @ git+https://github.com/Soheab/mijndak.py"
```

The `speedups` extra is optional and makes requests a little faster.

## Getting started

Everything starts with a `Client`. Use it with `async with` so the connection is closed when you're done:

```python
import asyncio

import mijndak


async def main() -> None:
    async with mijndak.Client() as client:
        await client.auth.login("me@example.com", "my-password")

        for listing in await client.listings.matching():
            print(listing.address, listing.rent, listing.position)


asyncio.run(main())
```

The client connects to Amsterdam by default. To use another region, pass it in:

```python
client = mijndak.Client(region=mijndak.UTRECHT)
```

The built-in regions are `AMSTERDAM`, `UTRECHT`, `ALMERE`, `GOOI_EN_VECHT`, `EEMVALLEI`, `MIDDEN_HOLLAND` and
`GRONINGEN`. `mijndak.REGIONS` holds all of them.

If your region isn't built in, create your own. You need the region's website and its ID and code, which you can find
in your browser's developer tools: every request the site makes sends them as `SamenwerkingsverbandId` and
`SamenwerkingsverbandCode`.

```python
my_region = mijndak.Region("My region", "https://myregion.mijndak.nl", swv_id="99", swv_code="ABC")
client = mijndak.Client(region=my_region)
```

## What you can do

The client groups its methods by topic, mirroring the menus on the website.

### Logging in: `client.auth`

```python
await client.auth.login("me@example.com", "my-password")
print(client.auth.is_authenticated)
await client.auth.logout()
```

If your account uses two-step verification, `login()` raises `MFARequiredError`. Approve the login in the DAK app,
then call `login()` again.

### Listings: `client.listings`

```python
everything = await client.listings.public()  # works without logging in
for_you = await client.listings.matching()  # homes you qualify for
not_for_you = await client.listings.non_matching()
favourites = await client.listings.saved_and_hidden()

listing = for_you[0]
print(listing.address, listing.rent, listing.deadline, listing.match_percentage)
```

Each listing can also fetch more about itself:

```python
details = await listing.fetch()  # the full listing
extras = await listing.extras()  # description, costs, rooms and facilities
photos = await listing.photos()
rules = await listing.eligibility_rules()  # why you do or don't qualify

await listing.set_saved()  # add it to your favourites
await listing.set_hidden()  # hide it from your overview
```

If you only have a listing's ID, you don't need to look it up first:

```python
listing = client.listings.partial(123456)
await listing.set_saved()
```

### Filtering and sorting

The website filters and sorts listings in your browser, so the library does the same in Python. `ListingFilters`
takes the same filters as the website's filter panel, using the names the website shows:

```python
from mijndak import ListingFilters, ListingKind, SortBy, filter_options, sort_listings

listings = await client.listings.matching()

print(filter_options(listings))  # every filter's options, with how many listings have each

filters = ListingFilters(
    cities={"Amsterdam", "Zaandam"},
    kinds={ListingKind.REGULAR},
    rooms={2, 3},
    maximum_rent=1000,
)
for listing in sort_listings(filters.apply(listings), SortBy.TIME_LEFT):
    print(listing.address, listing.rent, listing.deadline)
```

You can sort by match, position, time left, price, date added and area, and pass `reverse=True` to flip the order.

Filters also work with the website's share links, so you can open your filters in the browser or use a link
someone sent you:

```python
print(filters.to_url(client.region))  # https://amsterdam.mijndak.nl/WoningOverzicht?woonplaats=...
filters = ListingFilters.from_url("https://amsterdam.mijndak.nl/WoningOverzicht?woonplaats=Amsterdam&kamers=2,3")
```

The website only remembers one filter for your account: whether to show only homes that match your housing wishes.
Change it with `await client.settings.set_filter_by_wishes(True)`.

### Reactions: `client.reactions`

```python
for item in await client.reactions.current():
    print(item.listing.address, item.reaction.status, item.reaction.position)

await client.reactions.react(123456)  # places a real reaction!
await client.reactions.withdraw(123456)
```

`ongoing()` lists reactions to listings that have closed and are being allocated, and `past()` lists finished ones.

### Your profile: `client.account`

```python
for registration in await client.account.points():
    print(registration.name, registration.total.points)

wishes = await client.account.housing_wishes()
details = await client.account.personal_details()
household = await client.account.household()
schemes = await client.account.priority_schemes()  # urgencies, bindings and so on
```

You can also see your current housing situation, payments, uploaded documents and which parts of your profile are
complete. Changes work too: updating your personal details, managing household members, uploading documents and
choosing which messages you get by e-mail.

### Settings: `client.settings`

```python
user = await client.settings.user()
print(user.username, user.last_login)

await client.settings.set_display_preferences(hide_map=True)
await client.settings.change_password("old-password", "new-password")
```

## Staying logged in

Logging in on every run is slow, and it can trigger two-step verification each time. Save the session instead and
restore it later:

```python
cookies = client.auth.export_session()
# ...store `cookies` somewhere safe...

client.auth.restore_session(cookies)
if not await client.auth.ensure_session():
    # The session expired, so log in again.
    await client.auth.ensure_session(username="me@example.com", password="my-password")
```

The saved cookies give full access to your account, so keep them as safe as a password, for example encrypted.
`ensure_session()` only logs in again when the session has really expired, and it never stores your password.

## Handling errors

Every error the library raises is a `mijndak.MijnDakError`, so you can catch them all at once or pick specific ones:

| Error                   | When it happens                                                   |
| ----------------------- | ----------------------------------------------------------------- |
| `AuthenticationError` | The username or password is wrong.                                |
| `MFARequiredError`    | The login has to be approved in the DAK app first.                |
| `NotLoggedInError`    | You called something that needs a login, or your session expired. |
| `ServerError`         | DAK said no, for example because a listing has closed.            |
| `HTTPError`           | The request itself failed, for example because the site is down.  |
