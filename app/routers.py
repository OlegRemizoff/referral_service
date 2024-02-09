from fastapi import Response, APIRouter, HTTPException, status
from app.schemas import SUserRegister, SUserLogin
from app.dao import UsersDAO
from app.auth import get_password_hash, verify_password, create_access_token


user_router = APIRouter(
    prefix="/auth",
    tags=["Auth & Users"],
)


@user_router.post("/register")
async def register_user(user_data: SUserRegister):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=500, detail="User is already existing")
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password, ref_code=user_data.ref_code)
    return {"message": "Register has been successful!"}


@user_router.post("/login")
async def register_user(response: Response, user_data: SUserLogin):
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if not user and not verify_password(user_data.password, user.password):
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not register or wrong password! ")
    access_token = create_access_token(
        {"sub": int(user.id)})  # {sub: , expire: ""}
    response.set_cookie("ref_access_token", access_token)
    return {"message": "Login has been successful!"}


@user_router.post("/logout")
async def login_user(response: Response) -> dict:
    response.delete_cookie("events_access_token")
    return {"message": "Logout has been successful!"}
