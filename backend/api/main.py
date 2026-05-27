import logging
import threading
import time
from contextlib import asynccontextmanager
from pathlib import Path

from django.conf import settings as django_settings
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from .routers import (
    auth, comments, config, feeds, newsletter, posts, preview, reactions, search
)

logger = logging.getLogger(__name__)


def _scheduler_loop() -> None:
    from .scheduler import publish_scheduled_posts
    while True:
        time.sleep(60)
        try:
            publish_scheduled_posts()
        except Exception:
            logger.exception("Scheduler error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    thread = threading.Thread(
        target=_scheduler_loop, daemon=True, name="post-scheduler"
    )
    thread.start()
    yield


_debug = django_settings.DEBUG

app = FastAPI(
    title="Blog API",
    version="1.0.0",
    docs_url="/docs" if _debug else None,
    redoc_url="/redoc" if _debug else None,
    openapi_url="/openapi.json" if _debug else None,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(comments.router, prefix="/api/posts", tags=["comments"])
app.include_router(feeds.router, tags=["feeds"])
app.include_router(search.router, prefix="/api/search", tags=["search"])
app.include_router(reactions.router, prefix="/api/posts", tags=["reactions"])
app.include_router(preview.router, prefix="/api/preview", tags=["preview"])
app.include_router(newsletter.router, prefix="/api/newsletter", tags=["newsletter"])
app.include_router(config.router, prefix="/api/config", tags=["config"])

media_root = Path(django_settings.MEDIA_ROOT)
media_root.mkdir(parents=True, exist_ok=True)
app.mount("/media", StaticFiles(directory=str(media_root)), name="media")
