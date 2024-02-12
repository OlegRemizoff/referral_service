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
   




    # model_config = {
    #     "json_schema_extra": {
    #         "examples": [
    #             {   
    #                 "code": "",
    #                 "expiration_date": "date-time",
    #                 # "date_to": date.today().isoformat()
    #             }
    #         ],
    #     }
    # }



    # id = Column(Integer, primary_key=True)
    # code = Column(String, nullable=False)
    # expiration_date = datetime.utcnow() + timedelta(days=180)
    # user_id = Column(ForeignKey("users.id")) 
    # user = relationship("User", back_populates="referral_codes")