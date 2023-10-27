from fastapi import APIRouter, Depends
from .. import schema, models

from .auth import get_current_buyer

router = APIRouter()


@router.get('')
async def categories(_: schema.Buyer = Depends(get_current_buyer)):
    category_choices = models.CATEGORY_CHOICES
    out = []
    for category in category_choices:
        if category=="Grocery":
            out.append({
                "name": category,
                "url": "https://s3.ap-south-1.amazonaws.com/hypermaakbucket/04e486b79bec44aea3cf5cc2f7cf1ac9.png"
            })
        elif category=="Meat":
            out.append({
                "name": category,
                "url": "https://s3.ap-south-1.amazonaws.com/hypermaakbucket/2dd485c68393455c9ec35b7c6d86ba40.png"
            })
        else:
            pass
        
    return out