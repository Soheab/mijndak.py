from __future__ import annotations

import asyncio
import os

import mijndak


async def main() -> None:
    async with mijndak.Client() as client:
        await client.auth.login(os.environ["MIJNDAK_USER"], os.environ["MIJNDAK_PASSWORD"])

        listings = await client.listings.matching()
        print(f"{len(listings)} matching listings")
        for listing in sorted(listings, key=lambda item: item.position or 1_000_000)[:10]:
            print(
                f"  #{listing.position or '?':>5}  {listing.address!s:<55} "
                f"€{listing.rent}  {listing.match_percentage:.0%}  deadline {listing.deadline}"
            )

        for item in await client.reactions.current():
            print("reaction:", item.listing.address, item.reaction.status, item.reaction.position)

        for dashboard in await client.account.points():
            print("points:", dashboard.name, dashboard.total.points)


if __name__ == "__main__":
    asyncio.run(main())
