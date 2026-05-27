from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, comments, feeds, posts

app = FastAPI(
    title="Blog API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
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
