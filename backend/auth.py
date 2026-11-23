from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from .database import register_user, login_user


router = APIRouter(prefix="/auth", tags=["Authentication"])


class UserCredentials(BaseModel):
    username: str
    password: str


@router.post("/register")
def register(credentials: UserCredentials):

    result = register_user(
        credentials.username,
        credentials.password
    )

    if result == "Registration successful!":
        return {"message": result}

    raise HTTPException(
        status_code=400,
        detail=result
    )


@router.post("/login")
def login(credentials: UserCredentials):

    user = login_user(
        credentials.username,
        credentials.password
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    return {
        "message": "Login successful!",
        "user": user
    }