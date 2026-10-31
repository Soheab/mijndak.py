from __future__ import annotations

import asyncio
import pathlib
import time
from typing import TYPE_CHECKING

import mijndak
from mijndak import ListingFilters, ListingKind, SortBy, filter_options, sort_listings

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable


def read_env(path: pathlib.Path) -> dict[str, str]:
    """Read ``KEY=value`` lines from a ``.env`` file.

    The file is read directly instead of through ``os.environ``: Windows already sets ``USERNAME`` to the Windows
    login name.
    """
    if not path.is_file():
        return {}
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.strip().partition("=")
        if sep and key and not key.startswith("#"):
            values[key.strip()] = value.strip().strip("\"'")
    return values


passed: list[str] = []
failed: list[tuple[str, BaseException]] = []


async def check[T](name: str, call: Callable[[], Awaitable[T]], describe: Callable[[T], object] = repr) -> T | None:
    start = time.perf_counter()
    try:
        result = await call()
    except Exception as exc:  # report every failure and keep going
        failed.append((name, exc))
        print(f"  FAIL  {name}: {type(exc).__name__}: {exc}")
        return None
    passed.append(name)
    print(f"  ok    {name} ({time.perf_counter() - start:.1f}s): {describe(result)}")
    return result


async def now[T](value: T) -> T:  # ruff: ignore[unused-async] - check() awaits whatever it is given
    """Wrap a plain value so :func:`check` can time and report synchronous code too."""
    return value


def test_filters(client: mijndak.Client, listings: list[mijndak.Listing]) -> Awaitable[None]:
    """Filter, sort and share-link checks; these make no requests."""

    async def run() -> None:
        print(f"\nFiltering and sorting ({len(listings)} listings)")
        options = await check(
            "filter_options", lambda: now(filter_options(listings)), lambda o: {k: len(v) for k, v in o.items()}
        )
        if not options or not options["cities"]:
            return
        city = next(iter(options["cities"]))
        rooms = sorted(options["rooms"])[:2]
        filters = ListingFilters(cities={city}, kinds={ListingKind.REGULAR}, rooms=rooms, maximum_rent=1200)

        def all_match(result: list[mijndak.Listing]) -> str:
            ok = all(
                x.address.city == city
                and ListingKind.of(x) is ListingKind.REGULAR
                and str(x.unit.rooms) in rooms
                and x.rent is not None
                and x.rent <= 1200
                for x in result
            )
            return f"{len(result)} of {len(listings)} match {filters!r}, all correct: {ok}"

        await check("ListingFilters.apply", lambda: now(filters.apply(listings)), all_match)
        url = await check("ListingFilters.to_url", lambda: now(filters.to_url(client.region)), str)
        if url:
            expected = ListingFilters(cities=filters.cities, kinds=filters.kinds, rooms=filters.rooms)
            await check(
                "ListingFilters.from_url",
                lambda: now(ListingFilters.from_url(url)),
                lambda back: f"same as the filters without rent: {back == expected}",
            )
        await check(
            "ListingKind.of",
            lambda: now({kind.value: sum(ListingKind.of(x) is kind for x in listings) for kind in ListingKind}),
        )
        for by in SortBy:
            await check(f"sort_listings({by.name})", lambda by=by: now(sort_listings(listings, by)), describe_sort(by))
        await check(
            "sort_listings(PRICE, reverse)",
            lambda: now(sort_listings(listings, SortBy.PRICE, reverse=True)),
            lambda r: f"most expensive first: {[str(x.rent) for x in r[:3]]}",
        )

    return run()


def describe_sort(by: SortBy) -> Callable[[list[mijndak.Listing]], str]:
    value: dict[SortBy, Callable[[mijndak.Listing], object]] = {
        SortBy.MATCH: lambda x: x.match_percentage,
        SortBy.POSITION: lambda x: x.position,
        SortBy.TIME_LEFT: lambda x: x.deadline and x.deadline.date().isoformat(),
        SortBy.PRICE: lambda x: x.rent and str(x.rent),
        SortBy.ADDED: lambda x: x.published_at and x.published_at.date().isoformat(),
        SortBy.AREA: lambda x: x.unit.living_area and str(x.unit.living_area),
    }

    def describe(result: list[mijndak.Listing]) -> str:
        return f"first {[value[by](x) for x in result[:3]]}, last {value[by](result[-1]) if result else None}"

    return describe


async def test_listings(client: mijndak.Client) -> None:
    print("\nListings (no login needed)")
    listings = await check("listings.public", client.listings.public, lambda r: f"{len(r)} listings")
    if not listings:
        return
    listing = listings[0]
    print(f"        first: {listing.address} | rent {listing.rent} | deadline {listing.deadline} | labels {listing.labels}")
    detail = await check(
        "listing.fetch",
        listing.fetch,
        lambda d: d and f"{d.unit.rooms} rooms, {d.unit.living_area} m², floor {d.unit.floor}",
    )
    await check("listing.photos", listing.photos, lambda r: f"{len(r)} photos")
    await check("listing.extras", listing.extras, lambda e: e and f"{len(e.rooms)} rooms, {len(e.price_components)} costs")
    await check("listing.downloads", listing.downloads, lambda r: f"{len(r)} files")
    await check("listing.vr_floorplans", listing.vr_floorplans, lambda r: f"{len(r)} floor plans")
    await check("listing.housing_costs", listing.housing_costs, lambda h: h and h.costs.total_costs)
    if detail:
        await check("listings.fetch", lambda: client.listings.fetch(detail.publication_id), lambda d: d and d.address)
    await test_filters(client, listings)


async def test_account(client: mijndak.Client) -> None:
    print("\nListings and reactions (logged in)")
    matching = await check("listings.matching", client.listings.matching, lambda r: f"{len(r)} listings")
    await check("listings.non_matching", client.listings.non_matching, lambda r: f"{len(r)} listings")
    await check(
        "listings.saved_and_hidden",
        client.listings.saved_and_hidden,
        lambda r: f"{len(r.saved)} saved, {len(r.hidden)} hidden",
    )
    if matching:
        await test_filters(client, matching)
        listing = matching[0]
        await check("listing.enrolment_information", listing.enrolment_information, lambda e: f"eligible: {e.is_eligible}")
        await check("listing.eligibility_rules", listing.eligibility_rules, lambda r: f"{len(r)} rules")
    for name in ("current", "ongoing", "past"):
        await check(f"reactions.{name}", getattr(client.reactions, name), lambda r: f"{len(r)} reactions")

    print("\nAccount")
    account = client.account
    await check("account.points", account.points, lambda r: [(p.name, p.total.points) for p in r])
    await check("account.points_lines", account.points_lines, lambda r: [len(t.lines) for t in r])
    await check("account.housing_wishes", account.housing_wishes, lambda w: f"{len(w.cities)} cities to choose from")
    await check(
        "account.personal_details", account.personal_details, lambda d: f"first name set: {bool(d.person.first_name)}"
    )
    await check(
        "account.configuration", account.configuration, lambda c: f"registration fee {c.configuration.registration_fee}"
    )
    await check("account.has_priority_schemes", account.has_priority_schemes)
    await check("account.household", account.household, lambda h: f"{h.household.adult_count} adults")
    await check("account.current_housing", account.current_housing, lambda h: f"{h.housing.rooms} rooms")
    await check("account.priority_schemes", account.priority_schemes, lambda p: [s.name for s in p.urgencies])
    await check("account.status", account.status, lambda s: [(p.name, p.is_complete) for p in s.sections])
    await check("account.open_payment", account.open_payment, lambda p: f"payment due: {p.is_due}")
    await check("account.payments", account.payments, lambda p: f"{len(p.information.payments)} payments")
    await check("account.documents", account.documents, lambda d: f"{len(d.main_applicant)} people with documents")
    await check("account.subscriptions", account.subscriptions, lambda r: [s.name for s in r])

    print("\nSettings")
    settings = client.settings
    await check("settings.user", settings.user, lambda u: u and f"last login {u.last_login}")
    await check("settings.registrations", settings.registrations, lambda r: [x.product_code for x in r])
    await check("settings.mfa_details", settings.mfa_details)
    await check(
        "settings.display_preferences",
        settings.display_preferences,
        lambda p: f"map hidden: {p.is_map_hidden}, only homes matching wishes: {p.filters_by_wishes}",
    )

    print("\nSession")
    await check("auth.refresh_session", client.auth.refresh_session)
    await check("auth.ensure_session", client.auth.ensure_session)


async def main() -> None:
    async with mijndak.Client() as client:
        await test_listings(client)

        env = read_env(pathlib.Path(__file__).with_name(".env"))
        username, password = env.get("USERNAME"), env.get("PASSWORD")
        if username and password:
            print("\nLogging in")
            await client.auth.login(username, password)
            await test_account(client)
            await check(
                "auth.logout", client.auth.logout, lambda _: f"logged out, cookie gone: {not client.auth.is_authenticated}"
            )
        else:
            print("\nPut USERNAME and PASSWORD in .env to also test the logged-in methods.")

    print(f"\n{len(passed)} passed, {len(failed)} failed")
    for name, exc in failed:
        print(f"  {name}: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
