from typing import TypedDict

__all__ = ("Envelope", "ModuleInfo", "ModuleManifest", "OSException", "VersionInfo")


class VersionInfo(TypedDict, total=False):
    hasModuleVersionChanged: bool
    hasApiVersionChanged: bool


class OSException(TypedDict, total=False):
    name: str
    message: str
    specificType: str


class Envelope[T](TypedDict, total=False):
    """Outer ``screenservices`` response: ``{versionInfo, data, exception}``."""

    versionInfo: VersionInfo
    data: T
    exception: OSException


class ModuleManifest(TypedDict, total=False):
    versionToken: str
    urlVersions: dict[str, str]
    urlMappings: dict[str, str]


class ModuleInfo(TypedDict):
    manifest: ModuleManifest
