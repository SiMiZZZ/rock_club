from pydantic import BaseModel, EmailStr


class RegisterUser(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
