from datetime import datetime
from pydantic import BaseModel


class CommentCreate(BaseModel):
    content: str


class CommentAuthor(BaseModel):
    id: int
    username: str


class CommentOut(BaseModel):
    id: int
    author: CommentAuthor
    content: str
    created_at: datetime
