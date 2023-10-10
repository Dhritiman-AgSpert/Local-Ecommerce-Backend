from pydantic import BaseModel
from typing import List



class AddressBase(BaseModel):
    name: str
    house: str
    street: str
    city: str
    pincode: str

class AddressCreate(AddressBase):
    pass

class AddressUpdate(AddressBase):
    id: int

class Address(AddressBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


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


class UserBase(BaseModel):
    phone_number: str
    addresses: List[Address] = []

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True


