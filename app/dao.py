from app.database import async_session_maker
from app.models import User, ReferralCode
from sqlalchemy import select, insert
from sqlalchemy.orm import selectinload, load_only
from app.schemas import SReferralCode
from datetime import date

class BaseDAO:
    model = None

    @classmethod
    async def find_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalars().one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def delete_by_id(cls, model_id: int):
        async with async_session_maker() as session:
            obj = await session.get(cls.model, model_id)
            if obj:
                await session.delete(obj)
                await session.commit()
                return {"message": "Object has been successefuly deleted"}
            return {"message": "Object not found"}

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()


class UsersDAO(BaseDAO):
    model = User


    @classmethod
    async def get_user_and_codes(cls, **filter_by):
        async with async_session_maker() as session:

            query = (
                select(cls.model)
                .filter_by(**filter_by)
                .options(selectinload(cls.model.referral_codes), load_only(cls.model.id, cls.model.email))
                )
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def add_code(cls, data: SReferralCode):
    # id: Optional[int]
    # code: str = Field(..., min_length=1)
    # expiration_date: date
    # user_id: int
        
        new_code = insert(ReferralCode).values(

            code=data.code,
            expiration_date=data.expiration_date,
            user_id=data.user_id
        )

        async with async_session_maker() as session:
            await session.execute(new_code)
            await session.commit()
            return {"message": "Object has been successefuly created"}