from pydantic import BaseModel
from typing import Optional, Dict, Any
from database.models.user import UserRead


class UserRegisterRequest(BaseModel):
    email: str
    username: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    user: UserRead
    token: str


class UserRegisterResponse(BaseModel):
    success: bool
    data: UserResponse


class UserLoginResponse(BaseModel):
    success: bool
    data: UserResponse


class UserProfileResponse(BaseModel):
    success: bool
    data: UserRead


class AuthErrorResponse(BaseModel):
    success: bool
    error: str
    message: str