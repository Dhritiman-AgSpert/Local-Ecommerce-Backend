from pydantic import BaseModel
from typing import List


# Address
class AddressBase(BaseModel):
    name: str
    phone: str
    house: str
    street: str
    area: str
    city: str
    pincode: str
    lat: float
    lng: float

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    id: int

class Address(AddressBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# Token
class Token(BaseModel):
    access_token: str
    token_type: str

# OTP
class OTPBase(BaseModel):
    otp: str
    phone_number: str
    count: int
    verified: bool

class OTPCreate(OTPBase):
    pass

class OTP(OTPBase):
    id: int

    class Config:
        from_attributes = True

# Buyer
class BuyerBase(BaseModel):
    phone_number: str
    addresses: List[Address] = []

class BuyerCreate(BuyerBase):
    pass

class Buyer(BuyerBase):
    id: int

    class Config:
        from_attributes = True


