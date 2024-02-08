from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

from typing import Optional
from datetime import datetime, timedelta, date



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False) 
    hashed_password = Column(String, nullable=False)
    ref_code = Column(String, unique=True, nullable=True)
    referral_codes = relationship('ReferralCode', back_populates='user')


class ReferralCode(Base):
    __tablename__ = 'referral_codes'
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    expiration_date = datetime.utcnow() + timedelta(days=180)
    user_id = Column(ForeignKey("users.id")) 
    user = relationship("User", back_populates="referral_codes")











# class SReferralCode(BaseModel):
#     id: int
#     code: str
#     expiration_date: date
#     user_id: int




# class SUserAuth(BaseModel):
#     email: EmailStr
#     password: str

#     model_config = {
#         "json_schema_extra": {
#             "examples": [
#                 {
#                     "email": "test@gmail.com",
#                     "password": "Stro0ng!",
#                 }
#             ]
#         }
#     }