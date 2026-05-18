from fastapi import APIRouter, HTTPException, status
from django.contrib.auth.models import User

from ..deps import create_access_token, hash_password, verify_password
from ..schemas.auth import LoginRequest, RegisterRequest, TokenOut

router = APIRouter()


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
    return TokenOut(access_token=create_access_token(user.pk))


@router.post("/login", response_model=TokenOut)
def login(data: LoginRequest):
    try:
        user = User.objects.get(username=data.username, is_active=True)
    except User.DoesNotExist:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return TokenOut(access_token=create_access_token(user.pk))
