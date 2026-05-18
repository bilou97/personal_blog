from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from .comments import CommentOut


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str


class TagOut(BaseModel):
    id: int
    name: str
    slug: str


class PostListOut(BaseModel):
    id: int
    title: str
    slug: str
    excerpt: str
    cover_image: Optional[str]
    category: Optional[CategoryOut]
    tags: list[TagOut]
    published_at: Optional[datetime]


class PostDetailOut(PostListOut):
    content: str
    comments: list[CommentOut]
