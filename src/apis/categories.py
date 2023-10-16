from fastapi import APIRouter, Depends
from .. import schema

from .auth import get_current_buyer

router = APIRouter()


@router.get('')
async def categories(_: schema.Buyer = Depends(get_current_buyer)):
    return [
        {
            "category": "Hardware",
            "icon_name": "hammer-screwdriver"
        },
        {
            "category": "Paint",
            "icon_name": "paint-roller"
        },
        {
            "category": "Vegetable",
            "icon_name": "carrot"
        },
        {
            "category": "Furniture",
            "icon_name": "chair"
        },
        {
            "category": "Hardware",
            "icon_name": "hammer-screwdriver"
        },
        {
            "category": "Paint",
            "icon_name": "paint-roller"
        },
        {
            "category": "Vegetable",
            "icon_name": "carrot"
        },
        {
            "category": "Furniture",
            "icon_name": "chair"
        },
        {
            "category": "Hardware",
            "icon_name": "hammer-screwdriver"
        },
        {
            "category": "Paint",
            "icon_name": "paint-roller"
        },
        {
            "category": "Vegetable",
            "icon_name": "carrot"
        },
        {
            "category": "Furniture",
            "icon_name": "chair"
        },
    ]