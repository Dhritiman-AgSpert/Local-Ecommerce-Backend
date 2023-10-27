from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schema, crud, database, models

from .auth import get_current_buyer

router = APIRouter()


@router.get('/allowed_areas')
def allowed_areas(
    _: schema.Buyer = Depends(get_current_buyer)
):
    return models.AREA_CHOICES

@router.post('', response_model=schema.Address)
def create_address_for_buyer(
    address: schema.AddressCreate, db: Session = Depends(database.get_db), current_buyer: schema.Buyer = Depends(get_current_buyer)
):
    return crud.create_buyer_address(db=db, address=address, buyer_id=current_buyer.id)

@router.put('/{id}', response_model=schema.Address)
def update_address(id: int, address: schema.AddressUpdate, db: Session = Depends(database.get_db), _: schema.Buyer = Depends(get_current_buyer)):
    # sourcery skip: reintroduce-else, swap-if-else-branches, use-named-expression
    db_address = crud.get_address(db=db, id=id)
    
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    return crud.update_buyer_address(db=db, address=address)

@router.delete('/{id}')
def delete_address(id: int, db: Session = Depends(database.get_db), _: schema.Buyer = Depends(get_current_buyer)):
    db_address = crud.get_address(db=db, id=id)
    
    if not db_address:
        raise HTTPException(status_code=404, detail="Address not found")
    
    crud.delete_buyer_address(db=db, id=id)
    
    return {"detail": "Address deleted"}