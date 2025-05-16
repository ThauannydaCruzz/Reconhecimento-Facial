from pydantic import BaseModel, EmailStr

class RegisterSchema(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    country: str

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
        orm_mode = True 
