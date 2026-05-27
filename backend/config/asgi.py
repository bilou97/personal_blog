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
    path = scope.get("path", "")
    if scope["type"] == "http" and (
        path.startswith("/api/") or path.startswith("/media/") or path in _FASTAPI_PATHS
    ):
        await fastapi_app(scope, receive, send)
    else:
        await _django_app(scope, receive, send)


application = ProxyHeadersMiddleware(_application, trusted_hosts="*")
