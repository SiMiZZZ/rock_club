from pydantic import BaseModel, EmailStr, ConfigDict, UUID4


class UserAuthInfo(BaseModel):
    id: UUID4
    email: EmailStr
    name: str
    surname: str

    model_config = ConfigDict(from_attributes=True)
