from datetime import timedelta, datetime
import jwt
import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

from app.core import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/jwt/login", scheme_name="UserSchema")


async def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    print(token)
    try:
        payload = decode_jwt_token(token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid token: {e}"
        )
    return payload


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    hashed_pwd: bytes = password.encode()
    return bcrypt.hashpw(hashed_pwd, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password)


def encode_jwt_token(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta = timedelta(minutes=15),
) -> str:
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(exp=expire, iat=now)
    encoded = jwt.encode(payload, private_key, algorithm=algorithm)
    return encoded


def decode_jwt_token(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
) -> dict:
    data = jwt.decode(token, public_key, algorithms=[algorithm])
    return data
