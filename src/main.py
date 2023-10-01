from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import crud, models, schema, database
from .config import settings

from datetime import datetime, timedelta
import random
import requests
from jose import JWTError, jwt

app = FastAPI()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"


def gene_otp():
    key = random.randint(999, 9999)
    print(key)
    return str(key)

def send_otp(phone, otp):
    if phone and otp:
        URL = (
            "https://2factor.in/API/V1/cebcca8d-5eaf-11ee-addf-0200cd936042/SMS/"
            + str(phone)
            + "/"
            + str(otp)
            + "/Template1"
        )
        resp = requests.get(url=URL)
        data = resp.json()
        print(data)
        if data["Status"] == "Success":
            return True
        else:
            return False
    else:
        return False

@app.post('/phone')
async def phone(user_phone: str, db: Session = Depends(get_db)):
    
    otp_in_db = crud.get_otp_by_phone(db=db, phone_number=user_phone)

    if otp_in_db and otp_in_db.count >= 10:
        return {"message": "OTP sending limit exceeded. Contact customer service."}
    
    # Generate OTP and send it to the user here
    generated_otp = gene_otp()
    sent = send_otp(user_phone, generated_otp)
    
    if sent:
        otp_create = schema.OTPCreate(otp=generated_otp, phone_number=user_phone, count=(otp_in_db.count if otp_in_db else 0) + 1)
        otp_in_db = crud.create_otp(db=db, otp=otp_create)
        return {"message": "OTP sent successfully."}
    else:
        return {"message": "OTP not sent."}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post('/otp')
async def otp(user_phone: str, otp:str ,db: Session = Depends(get_db)):
    
    otp_in_db = crud.get_otp_by_phone(db=db, phone_number=user_phone)

    
    if not otp_in_db or otp_in_db.otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    # Reset the count once the OTP is verified
    otp_in_db.count = 0

    # Create the token
    access_token = create_access_token(data={"sub": user_phone})
    
    return {"access_token": access_token}


