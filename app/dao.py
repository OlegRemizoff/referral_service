from app.database import async_session_maker
from app.models import User, ReferralCode
from sqlalchemy import select, insert, update, text
from sqlalchemy.orm import selectinload, load_only
from app.schemas import SReferralCode


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


class ReferralCodesDao(BaseDAO):
    model = ReferralCode

    @classmethod
    async def add_code(cls, data: SReferralCode):

        new_code = insert(cls.model).values(

            code=data.code,
            expiration_date=data.expiration_date,
            user_id=data.user_id
        )

        async with async_session_maker() as session:
            await session.execute(new_code)
            await session.commit()
            return {"message": "Object has been successefuly created"}

    @classmethod
    async def delete_by_id(cls, id: int):
        async with async_session_maker() as session:
            obj = await session.get(cls.model, id)
            if obj:
                await session.delete(obj)
                await session.commit()
                return {"message": "Object has been successefuly deleted"}
            return {"message": "Object not found"}

    @classmethod
    async def change_code(cls, user_id, desired_code):
        async with async_session_maker() as session:
            # stmt = (
            #     """UPDATE referral_codes
            #        SET is_active = False
            #        FROM users
            #        WHERE users.id = referral_codes.user_id
            #        AND referral_codes.is_active = True;
            #     """
            # )
            off_all_code = (
                update(cls.model)
                .where(cls.model.user_id == user_id)
                .values(is_active=False)
            )
            on_desired_code = (
                update(cls.model)
                .where((cls.model.user_id == user_id) & (ReferralCode.code == desired_code))
                .values(is_active=True)
            )
            # await session.execute(text(stmt))
            await session.execute(off_all_code)
            await session.execute(on_desired_code)
            await session.commit()


            # активный код
            # stmt = (
            #     """SELECT users.id, email, referral_codes.code, referral_codes.is_active
            #        FROM users
            #        LEFT JOIN referral_codes
            #        ON users.id = referral_codes.user_id
            #        WHERE referral_codes.is_active = 'True'
            #     """
            #     )

            # UPDATE referral_codes
            # SET is_active = 'True'
            # WHERE id = '4';

