from fastapi import APIRouter, HTTPException, status
from django.contrib.auth.models import User

from ..deps import (
    create_access_token,
    create_refresh_token,
    hash_password,
    verify_password,
    verify_refresh_token,
)
from ..schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenOut

router = APIRouter()


def _token_pair(user_id: int) -> TokenOut:
    return TokenOut(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )


@router.post("/register", response_model=TokenOut, status_code=status.HTTP_201_CREATED)
def register(data: RegisterRequest):
    if User.objects.filter(username=data.username).exists():
        raise HTTPException(status_code=400, detail="Username already taken")
    if User.objects.filter(email=data.email).exists():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User.objects.create(
        username=data.username,
        email=data.email,
        password=hash_password(data.password),
    )
    return _token_pair(user.pk)


@router.post("/login", response_model=TokenOut)
def login(data: LoginRequest):
    try:
        user = User.objects.get(username=data.username, is_active=True)
    except User.DoesNotExist:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return _token_pair(user.pk)


@router.post("/refresh", response_model=TokenOut)
def refresh(data: RefreshRequest):
    user_id = verify_refresh_token(data.refresh_token)
    try:
        User.objects.get(pk=user_id, is_active=True)
    except User.DoesNotExist:
        raise HTTPException(status_code=401, detail="User not found")
    return _token_pair(user_id)
