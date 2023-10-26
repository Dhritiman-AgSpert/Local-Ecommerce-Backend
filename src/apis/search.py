from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Union

from .. import crud, schema, database, models
from .auth import get_current_buyer

from haversine import haversine


router = APIRouter()


@router.get("/{keyword}", response_model=schema.SearchResult)
def search(address_id: int, keyword: str, buyer: models.Buyer = Depends(get_current_buyer), db: Session = Depends(database.get_db)):
    products = db.query(models.Product).filter(or_(models.Product.name.ilike(f"%{keyword}%"), models.Product.description.ilike(f"%{keyword}%"))).all()
    sellers = db.query(models.Seller).filter(or_(models.Seller.name.ilike(f"%{keyword}%"), models.Seller.address.ilike(f"%{keyword}%"))).options(joinedload(models.Seller.products)).all()

    # Validate the address_id
    address = crud.get_address(db=db, id=address_id)
    if address is None or address.owner_id != buyer.id:
        raise HTTPException(status_code=400, detail="Invalid address_id")

    # Calculate the distance of each seller from the buyer's selected address
    buyer_coords = (address.lat, address.lng)
    for seller in sellers:
        seller_coords = (seller.lat, seller.lng)
        seller.distance = haversine(buyer_coords, seller_coords)

    # Sort sellers by distance
    sellers.sort(key=lambda seller: seller.distance)

    return {"products": products, "sellers": sellers}
