from pydantic import BaseModel, EmailStr
from typing import Optional, List


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    # referral_codes: Optional[List[str]] = None
    # ref_code: Optional[str] = None


class SUserLogin(BaseModel):
    email: EmailStr
    password: str
