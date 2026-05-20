from pydantic import BaseModel


class LoginRequest(BaseModel):
    username: str
    password: str


class AdminUserCreateRequest(BaseModel):
    username: str
    password: str
    role: str


class AdminUserStatusRequest(BaseModel):
    enabled: bool


class AdminUserPasswordResetRequest(BaseModel):
    password: str
