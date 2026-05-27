import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.dev")
django.setup()

from django.core.asgi import get_asgi_application
from api.main import app as fastapi_app
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

_django_app = get_asgi_application()

_FASTAPI_PATHS = {
    "/openapi.json", "/docs", "/redoc", "/feed.xml", "/sitemap.xml"
}


async def _application(scope, receive, send):
    if scope["type"] == "lifespan":
        await fastapi_app(scope, receive, send)
        return
    path = scope.get("path", "")
    is_fastapi = (
        path.startswith("/api/")
        or path.startswith("/media/")
        or path in _FASTAPI_PATHS
    )
    if scope["type"] == "http" and is_fastapi:
        await fastapi_app(scope, receive, send)
    else:
        await _django_app(scope, receive, send)


application = ProxyHeadersMiddleware(_application, trusted_hosts="*")
