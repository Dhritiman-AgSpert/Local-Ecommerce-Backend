from pydantic import BaseModel

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

class OTPCreate(OTPBase):
    pass

class OTP(OTPBase):
    id: int

    class Config:
        from_attributes = True
