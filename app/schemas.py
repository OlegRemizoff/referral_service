from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date


class SUserRegister(BaseModel):
    email: EmailStr
    password: str
    # referral_codes: Optional[List[str]] = None
    # ref_code: Optional[str] = None


class SUserLogin(BaseModel):
    email: EmailStr
    password: str




class SReferralCode(BaseModel):
    id: Optional[int] 
    code: str = Field(..., min_length=1)
    expiration_date: Optional[date]
    user_id: int
   

    model_config = {
        "json_schema_extra": {
            "examples": [
                {   "id": 0,
                    "code": "write something",
                    "user_id": 0,
                    "expiration_date": "2024-02-13"
                }
            ],
        }
    }
