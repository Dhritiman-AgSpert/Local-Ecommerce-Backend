from pydantic import BaseModel
from typing import List, Optional

# Product
class ProductBase(BaseModel):
    category: Optional[str] = None
    sub_category: Optional[str] = None
    name: str
    description: Optional[str] = None
    image_url: str
    price: float

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True


# Seller
class SellerBase(BaseModel):
    phone_number: str
    
class SellerCreate(SellerBase):
    pass

class SellerUpdate(BaseModel):
    category: Optional[str] = None
    name: Optional[str] = None
    image_url: Optional[str] = None
    trade_license: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    
class Seller(BaseModel):
    id: int
    phone_number: str
    category: Optional[str] = None
    name: Optional[str] = None
    image_url: Optional[str] = None
    trade_license: Optional[str] = None
    address: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    
    class Config:
        from_attributes = True

class SellerWithProducts(Seller):
    products: List[Product] = []
    
    class Config:
        from_attributes = True

class SellerList(BaseModel):
    sellers: List[SellerWithProducts] = []

    class Config:
        from_attributes = True

# Address
class AddressBase(BaseModel):
    name: str
    phone_number: str
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


