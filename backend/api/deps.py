from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from django.conf import settings as django_settings
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import User

bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return make_password(password)


def verify_password(plain: str, hashed: str) -> bool:
    return check_password(plain, hashed)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=django_settings.JWT_EXPIRE_MINUTES
    )
    return jwt.encode(
        {"sub": str(user_id), "exp": expire, "type": "access"},
        django_settings.JWT_SECRET_KEY,
        algorithm=django_settings.JWT_ALGORITHM,
    )


def create_refresh_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=django_settings.JWT_REFRESH_EXPIRE_DAYS
    )
    return jwt.encode(
        {"sub": str(user_id), "exp": expire, "type": "refresh"},
        django_settings.JWT_SECRET_KEY,
        algorithm=django_settings.JWT_ALGORITHM,
    )


_PREVIEW_TTL_HOURS = 24


def create_preview_token(slug: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(hours=_PREVIEW_TTL_HOURS)
    return jwt.encode(
        {"sub": slug, "exp": expire, "type": "preview"},
        django_settings.JWT_SECRET_KEY,
        algorithm=django_settings.JWT_ALGORITHM,
    )


def verify_preview_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            django_settings.JWT_SECRET_KEY,
            algorithms=[django_settings.JWT_ALGORITHM],
        )
        if payload.get("type") != "preview":
            raise ValueError
        return str(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired preview token",
        )


def create_unsubscribe_token(email: str) -> str:
    return jwt.encode(
        {"sub": email, "type": "unsubscribe"},
        django_settings.JWT_SECRET_KEY,
        algorithm=django_settings.JWT_ALGORITHM,
    )


def verify_unsubscribe_token(token: str) -> str:
    try:
        payload = jwt.decode(
            token,
            django_settings.JWT_SECRET_KEY,
            algorithms=[django_settings.JWT_ALGORITHM],
            options={"verify_exp": False},
        )
        if payload.get("type") != "unsubscribe":
            raise ValueError
        return str(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid unsubscribe token",
        )


def verify_refresh_token(token: str) -> int:
    try:
        payload = jwt.decode(
            token,
            django_settings.JWT_SECRET_KEY,
            algorithms=[django_settings.JWT_ALGORITHM],
        )
        if payload.get("type") != "refresh":
            raise ValueError
        return int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
) -> User:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    try:
        payload = jwt.decode(
            credentials.credentials,
            django_settings.JWT_SECRET_KEY,
            algorithms=[django_settings.JWT_ALGORITHM],
        )
        if payload.get("type") != "access":
            raise ValueError
        user_id = int(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    try:
        return User.objects.get(pk=user_id, is_active=True)
    except User.DoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
