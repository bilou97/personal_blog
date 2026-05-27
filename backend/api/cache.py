import json
import os
from datetime import datetime

import redis as _redis

_client: _redis.Redis | None = None


def _get_client() -> _redis.Redis:
    global _client
    if _client is None:
        _client = _redis.Redis(
            host=os.getenv("REDIS_HOST", "redis"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True,
        )
    return _client


class _DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


def cache_get(key: str):
    try:
        value = _get_client().get(key)
        return json.loads(value) if value is not None else None
    except Exception:
        return None


def cache_set(key: str, value, ttl: int = 300) -> None:
    try:
        _get_client().setex(key, ttl, json.dumps(value, cls=_DatetimeEncoder))
    except Exception:
        pass


def cache_delete(pattern: str) -> None:
    try:
        client = _get_client()
        keys = client.keys(pattern)
        if keys:
            client.delete(*keys)
    except Exception:
        pass
