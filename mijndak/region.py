from __future__ import annotations

from typing import Final, override

from ._types import ClientVariables

__all__ = (
    "ALMERE",
    "AMSTERDAM",
    "EEMVALLEI",
    "GOOI_EN_VECHT",
    "GRONINGEN",
    "MIDDEN_HOLLAND",
    "REGIONS",
    "UTRECHT",
    "Region",
)


class Region:
    """A DAK region and its website (*samenwerkingsverband*).

    The library has the known regions built in, such as :data:`AMSTERDAM`. Create your own if your region is not one
    of them, and pass it to :class:`Client`.

    Parameters
    ----------
    name: :class:`str`
        The region's name, such as ``"Regio Amsterdam"``.
    base_url: :class:`str`
        The address of the region's website, such as ``"https://amsterdam.mijndak.nl"``.
    swv_id: :class:`str`
        The region's ID. The website sends it as ``SamenwerkingsverbandId`` with every request.
    swv_code: :class:`str`
        The region's code, such as ``"SRA"``. The website sends it as ``SamenwerkingsverbandCode`` with every request.

    Attributes
    ----------
    name: :class:`str`
        The region's name.
    base_url: :class:`str`
        The address of the region's website.
    swv_id: :class:`str`
        The region's ID.
    swv_code: :class:`str`
        The region's code.

    Examples
    --------
    ::

        my_region = mijndak.Region("My region", "https://myregion.mijndak.nl", swv_id="99", swv_code="ABC")
        client = mijndak.Client(region=my_region)
    """

    __slots__ = ("base_url", "name", "swv_code", "swv_id")

    def __init__(self, name: str, base_url: str, *, swv_id: str, swv_code: str) -> None:
        self.name: Final = name
        self.base_url: Final = base_url
        self.swv_id: Final = swv_id
        self.swv_code: Final = swv_code

    def client_variables(self) -> ClientVariables:
        """The region's details as the website sends them with every request.

        Returns
        -------
        :class:`ClientVariables`
            The region's ID and code.
        """
        return ClientVariables(SamenwerkingsverbandId=self.swv_id, SamenwerkingsverbandCode=self.swv_code)

    @override
    def __repr__(self) -> str:
        return f"Region({self.name!r}, {self.base_url!r}, swv_id={self.swv_id!r}, swv_code={self.swv_code!r})"


#: Regio Amsterdam (amsterdam.mijndak.nl). This is the default region.
AMSTERDAM: Final = Region("Regio Amsterdam", "https://amsterdam.mijndak.nl", swv_id="2", swv_code="SRA")
#: Regio Utrecht (utrecht.mijndak.nl).
UTRECHT: Final = Region("Regio Utrecht", "https://utrecht.mijndak.nl", swv_id="1", swv_code="UTR")
#: Almere (almere.mijndak.nl).
ALMERE: Final = Region("Almere", "https://almere.mijndak.nl", swv_id="7", swv_code="ALM")
#: Gooi en Vechtstreek (gooienvecht.mijndak.nl).
GOOI_EN_VECHT: Final = Region("Gooi en Vechtstreek", "https://gooienvecht.mijndak.nl", swv_id="11", swv_code="GEV")
#: Eemvallei (eemvallei.mijndak.nl).
EEMVALLEI: Final = Region("Eemvallei", "https://eemvallei.mijndak.nl", swv_id="10", swv_code="EEM")
#: Midden-Holland (middenholland.mijndak.nl).
MIDDEN_HOLLAND: Final = Region("Midden-Holland", "https://middenholland.mijndak.nl", swv_id="16", swv_code="MHO")
#: Groningen Huurt (groningenhuurt.mijndak.nl).
GRONINGEN: Final = Region("Groningen Huurt", "https://groningenhuurt.mijndak.nl", swv_id="12", swv_code="GRN")

#: Every built-in region.
REGIONS: Final = (AMSTERDAM, UTRECHT, ALMERE, GOOI_EN_VECHT, EEMVALLEI, MIDDEN_HOLLAND, GRONINGEN)
