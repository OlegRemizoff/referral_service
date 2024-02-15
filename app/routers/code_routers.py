from fastapi import APIRouter, HTTPException, Depends, status
from datetime import datetime, timedelta
from app.schemas import SReferralCode
from app.dao import UsersDAO, ReferralCodesDao
from app.models import User
from app.dependences import get_current_user


router = APIRouter(
    prefix="/codes",
    tags=["Referral Codes"],
)


# Добавление реферального кода
@router.post("/add")
async def add_code(data: SReferralCode, user: User = Depends(get_current_user)):
    if not user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized")

    data.user_id = user.id
    data.expiration_date = datetime.now().date() + timedelta(days=30)
    result = await ReferralCodesDao.add_code(data)
    return {"message": "Code has been successefuly created"}


# Удаление реферального кода
@router.delete("/delete")
async def del_code(code_id: int, user: User = Depends(get_current_user)):
    if not user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized")
    res = await UsersDAO.get_user_and_codes(id=user.id)
    ref_codes = res.referral_codes
    for i in ref_codes:
        if code_id == i.id:
            await ReferralCodesDao.delete_by_id(id=code_id)
            return {"message": "Code has been successefuly deleted"}
    return None


# Активация реферального кода
@router.get("/active")
async def activate_code(desired_code: str, user: User = Depends(get_current_user)):
    if not user:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is unauthorized")
    await ReferralCodesDao.change_code(user_id=user.id, desired_code=desired_code)
    current_code = await ReferralCodesDao.get_current_code(user.id)
    
    return {"Current active code": current_code}
