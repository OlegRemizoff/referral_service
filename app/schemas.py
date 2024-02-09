from pydantic import BaseModel, EmailStr
from typing import Optional


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    ref_code: Optional[str] = None


class SUserLogin(BaseModel):
    email: EmailStr
    password: str
