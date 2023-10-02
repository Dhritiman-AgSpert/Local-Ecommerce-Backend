from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []
        
class UserBase(BaseModel):
    phone_number: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

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
