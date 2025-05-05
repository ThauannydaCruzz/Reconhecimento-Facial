from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    country: str
    agree_to_terms: bool

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class UserResponseSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    country: str

    class Config:
        from_attributes = True  
