from fastapi import APIRouter, Depends
from .. import schema

from .auth import get_current_user

router = APIRouter()


@router.get('')
async def categories(_: schema.User = Depends(get_current_user)):
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