from fastapi import  APIRouter, HTTPException, Depends, status
from app.schemas import  SReferralCode
from app.dao import UsersDAO
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
            detail="User is not register or wrong password! ")

    result = await UsersDAO.add_code(data)
    return None


# Удаление реферального кода
@router.post("/delete")
async def add_code(data: SReferralCode, user: User = Depends(get_current_user)):
    pass