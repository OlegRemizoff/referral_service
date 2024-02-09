from fastapi import  Request, HTTPException, Depends, status
from jose import jwt, JWTError
from datetime import datetime

from app.config import settings
from app.dao import UsersDAO





def get_token(request: Request):
    token = request.cookies.get('ref_access_token')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User does not found")
    print(token)
    return token


async def get_current_user(token: str =  Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM) # {exp: 23423, "sub": user.id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="One")
    expire: str = payload.get('exp')
    if not (expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="TWO")
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Three")
    user = await UsersDAO.find_by_id(int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Four")
    return user