from sqlalchemy import Column, Integer, String, Boolean,ForeignKey, Date
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


from datetime import datetime, timedelta



class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False) 
    hashed_password = Column(String, nullable=False)
    referral_codes = relationship('ReferralCode', back_populates='user')


class ReferralCode(Base):
    __tablename__ = 'referral_codes'
    id = Column(Integer, primary_key=True)
    code = Column(String, nullable=False)
    expiration_date = Column(Date, nullable=False)
    user_id = Column(ForeignKey("users.id")) 
    user = relationship("User", back_populates="referral_codes")
    is_active = Column(Boolean, default=False)











