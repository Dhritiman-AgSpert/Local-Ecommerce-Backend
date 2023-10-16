from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Header, Request
from sqlalchemy.orm import Session

from .. import crud, schema, database
from ..config import settings

from datetime import datetime, timedelta, timezone
import random
import requests
from jose import jwt, JWTError

router = APIRouter()


SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


def gene_otp():
    key = random.randint(999, 9999)
    print(key)
    return str(key)

def send_otp(phone, otp):
    if not phone or not otp:
        return False
    URL = f"https://2factor.in/API/V1/cebcca8d-5eaf-11ee-addf-0200cd936042/SMS/{str(phone)}/{str(otp)}/Template1"
    resp = requests.get(url=URL)
    data = resp.json()
    print(data)
    return data["Status"] == "Success"

@router.post('/phone')
async def phone(buyer_phone: str, db: Session = Depends(database.get_db)):
    
    otp_in_db = crud.get_otp_by_phone(db=db, phone_number=buyer_phone)

    if otp_in_db and otp_in_db.count >= 10:
        return {"message": "OTP sending limit exceeded. Contact customer service."}
    
    # Generate OTP and send it to the buyer 
    generated_otp = gene_otp()
    # sent = send_otp(buyer_phone, generated_otp)
    sent = True
    
    if sent:
        otp_create = schema.OTPCreate(
            otp=generated_otp, 
            phone_number=buyer_phone, 
            count=(otp_in_db.count if otp_in_db else 0) + 1,
            verified=False
        )
        if otp_in_db:
            crud.update_otp(db=db, otp=otp_create)
        else:
            crud.create_otp(db=db, otp=otp_create)
        return {"message": "OTP sent successfully."}
    else:
        return {"message": "OTP not sent."}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=999999)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post('/otp')
async def otp(buyer_phone: str, otp:str, db: Session = Depends(database.get_db)):
    
    otp_in_db = crud.get_otp_by_phone(db=db, phone_number=buyer_phone)
    
    if not otp_in_db or otp_in_db.otp != otp or otp_in_db.verified == True:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Reset the count once the OTP is verified
    otp_in_db.count = 0
    otp_in_db.verified = True
    db.add(otp_in_db)
    db.commit()
    db.refresh(otp_in_db)

    # create buyer if doesn't exist.
    buyer_in_db = crud.get_buyer_by_phone(db=db, phone_number=buyer_phone)
    if not buyer_in_db:
        buyer_create = schema.BuyerCreate(phone_number=buyer_phone)
        crud.create_buyer(db=db, buyer=buyer_create)

    # Create the token
    access_token = create_access_token(data={"sub": buyer_phone})
    
    return {"access_token": access_token}


async def get_current_buyer(request: Request, token: Optional[str] = Header(None), db: Session = Depends(database.get_db)):
    authorization = request.headers.get('Authorization')
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        if token:
            # print("token", token)
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            phone_number: str = payload.get("sub")
            if phone_number is None:
                raise credentials_exception
        elif authorization:
            # print("authorization", authorization)
            payload = jwt.decode(authorization, SECRET_KEY, algorithms=[ALGORITHM])
            phone_number: str = payload.get("sub")
            if phone_number is None:
                raise credentials_exception
        else:
            raise credentials_exception
    except JWTError as e:
        raise credentials_exception from e
    buyer = crud.get_buyer_by_phone(db=db, phone_number=phone_number)
    if buyer is None:
        raise credentials_exception
    return buyer


@router.get("/me", response_model=schema.Buyer)
async def buyer_info(current_buyer: schema.Buyer = Depends(get_current_buyer), db: Session = Depends(database.get_db)):
    db_buyer = crud.get_buyer(db, buyer_id=current_buyer.id)
    if db_buyer is None:
        raise HTTPException(status_code=404, detail="Buyer not found")
    return db_buyer