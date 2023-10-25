from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schema, database, models
from .auth import get_current_buyer

from haversine import haversine


router = APIRouter()


@router.get("s", response_model=schema.SellerList)
async def list_sellers(category: str, address_id: int, buyer: models.Buyer = Depends(get_current_buyer), db: Session = Depends(database.get_db)):
    # Validate the address_id
    address = crud.get_address(db=db, id=address_id)
    if address is None or address.owner_id != buyer.id:
        raise HTTPException(status_code=400, detail="Invalid address_id")

    # Get all sellers
    sellers = crud.get_sellers_by_category(db=db, category=category)

    # Calculate the distance of each seller from the buyer's selected address
    buyer_coords = (address.lat, address.lng)
    for seller in sellers:
        seller_coords = (seller.lat, seller.lng)
        seller.distance = haversine(buyer_coords, seller_coords)

    # Sort sellers by distance
    sellers.sort(key=lambda seller: seller.distance)

    return {"sellers": sellers}

