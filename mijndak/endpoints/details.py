from __future__ import annotations

from typing import Final

import msgspec

from .._types import (
    AggregatePayload,
    ApplicantPayload,
    EligibilityPayload,
    EnrolmentInformationPayload,
    FileItemPayload,
    HousingCostsResponsePayload,
    ListingExtrasPayload,
)
from .base import EP, EP_REUSABLE, DataAction

__all__ = ("VIEW", "ListingDetails")

_SCREEN: Final = f"{EP}/HuisDetails/HuisDetails"
_BLOCK: Final = f"{EP}/HuisDetails/HuisDetails_WB"
#: Web-block and reusable actions must be called from this screen, or role validation fails.
VIEW: Final = "HuisDetails.HuisDetails"


class ListingDetails:
    LISTING: Final = DataAction(f"{_SCREEN}/ScreenDataSetGetPublicatie", AggregatePayload[msgspec.Raw], page_size=1)
    PHOTOS: Final = DataAction(f"{_SCREEN}/ScreenDataSetGetFotos", AggregatePayload[FileItemPayload], page_size=50)
    APPLICANT: Final = DataAction(f"{_SCREEN}/DataActionHaalAanvrager", ApplicantPayload)
    ENROLMENT_INFORMATION: Final = DataAction(
        f"{_SCREEN}/DataActionGetInformatieBijInschrijving", EnrolmentInformationPayload
    )
    ELIGIBILITY: Final = DataAction(
        f"{EP_REUSABLE}/HuisDetails_CW/RedenNietPassend/DataActionSynchroniseerWoningDetails",
        EligibilityPayload,
        view=VIEW,
    )
    # Web-block actions: they take the full listing record as the ``Publicatie`` variable.
    EXTRAS: Final = DataAction(f"{_BLOCK}/DataActionGetPublicatieDetails", ListingExtrasPayload, view=VIEW)
    DOWNLOADS: Final = DataAction(
        f"{_BLOCK}/ScreenDataSetGetDownloads", AggregatePayload[FileItemPayload], view=VIEW, page_size=50
    )
    VR_FLOORPLANS: Final = DataAction(
        f"{_BLOCK}/ScreenDataSetGetVRPlattegrond", AggregatePayload[FileItemPayload], view=VIEW, page_size=50
    )
    HOUSING_COSTS: Final = DataAction(f"{_BLOCK}/DataActionGetWoonlasten", HousingCostsResponsePayload, view=VIEW)
