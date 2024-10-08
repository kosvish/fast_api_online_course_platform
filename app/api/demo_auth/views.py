import secrets
import uuid
from time import time
from typing import Annotated, Any

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
    Header,
    Form,
    Response,
    Cookie,
)
from fastapi.security import HTTPBasic, HTTPBasicCredentials

router = APIRouter(prefix="/demo-auth", tags=["Demo Auth"])

security = HTTPBasic()


@router.get("/basic-auth")
def demo_basic_auth_credentials(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)]
):
    return {
        "message": "Hi",
        "username": credentials.username,
        "password": credentials.password,
    }


usernames_to_passwords = {"admin": "admin", "john": "password"}

static_auth_token_to_username = {
    "959d0972b606929d119158221ec3": "admin",
    "a719f1403e4457aebe9ad958fc92fe78013b": "password",
}


def get_username_by_static_auth_token(
    static_token: str = Header(alias="x-auth-token"),
) -> str:
    if static_token not in static_auth_token_to_username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid"
        )

    return static_auth_token_to_username[static_token]


def get_auth_username(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = usernames_to_passwords[credentials.username]
    if correct_password is None:
        raise unauthed_exc
    if credentials.username not in usernames_to_passwords:
        raise unauthed_exc
    if not secrets.compare_digest(
        credentials.password.encode("utf-8"), correct_password.encode("utf-8")
    ):
        return unauthed_exc
    return credentials.username


@router.get("/basic-auth-username")
def demo_basic_auth_username(auth_username: str = Depends(get_auth_username)):
    return {
        "message": f"Hi {auth_username}",
        "username": auth_username,
    }


@router.get("/some-http-header-auth")
def demo_auth_some_http_header(
    username: str = Depends(get_username_by_static_auth_token),
):
    return {
        "message": f"Hi {username}",
        "username": username,
    }


def get_auth_username_through_form(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
):
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password",
        headers={"WWW-Authenticate": "Basic"},
    )
    correct_password = usernames_to_passwords[username]
    if correct_password is None:
        raise unauthed_exc
    if username not in usernames_to_passwords:
        raise unauthed_exc
    if not secrets.compare_digest(
        password.encode("utf-8"), correct_password.encode("utf-8")
    ):
        return unauthed_exc
    return username


COOKIES: dict[str, dict[str, Any]] = {}
COOKIE_SESSION_ID_KEY = "web-app-session-id"


def generate_session_id() -> str:
    return uuid.uuid4().hex


def get_session_data(session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY)):
    if session_id not in COOKIES:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="not authenticated"
        )

    return COOKIES[session_id]


@router.post("/login-cookie")
def demo_auth_login_cookie(
    response: Response,
    auth_username: str = Depends(get_auth_username_through_form),
):
    session_id = generate_session_id()
    COOKIES[session_id] = {
        "username": auth_username,
        "login_at": int(time()),
    }
    response.set_cookie(COOKIE_SESSION_ID_KEY, session_id)
    return {"result": "ok"}


@router.get("/check-cookie/")
def demo_auth_check_cookie(user_session_data: dict = Depends(get_session_data)):
    username = user_session_data["username"]
    return {"message": f"Hello, {username}", **user_session_data}


@router.get("/logout-cookie/")
def demo_auth_check_cookie(
    response: Response,
    session_id: str = Cookie(alias=COOKIE_SESSION_ID_KEY),
    user_session_data: dict = Depends(get_session_data),
):
    COOKIES.pop(session_id),
    response.delete_cookie(session_id)
    username = user_session_data['username']

    return {"message": f"Bye, {username}"}
