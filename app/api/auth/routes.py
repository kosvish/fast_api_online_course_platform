from fastapi import APIRouter, Form, HTTPException, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import validate_password, encode_jwt_token, decode_jwt_token
from fastapi.security import OAuth2PasswordBearer
from app.db.models import UserModel
from ..dependencies import get_async_session
from .schemas import TokenInfo
from jwt.exceptions import InvalidTokenError

from ..schemas import UserSchema

router = APIRouter(prefix="/jwt", tags=["AuthJWT"])


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(get_async_session),
):
    invalid_data_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password"
    )
    query = select(UserModel).where(UserModel.username == username)
    user = await session.scalar(query)
    if user is None:
        raise invalid_data_exc

    if not validate_password(password, user.hash_password):
        raise invalid_data_exc
    return user


@router.post("/login")
async def login_user(user: UserModel = Depends(validate_auth_user)):
    jwt_payload = {"sub": user.id, "username": user.username, "email": user.email}
    token = encode_jwt_token(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")
