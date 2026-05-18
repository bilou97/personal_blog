from fastapi import APIRouter, Depends, HTTPException, status
from django.contrib.auth.models import User

from blog.models import Comment, Post
from ..deps import get_current_user
from ..schemas.comments import CommentCreate, CommentOut

router = APIRouter()


@router.post("/{slug}/comments", response_model=CommentOut, status_code=status.HTTP_201_CREATED)
def add_comment(slug: str, data: CommentCreate, current_user: User = Depends(get_current_user)):
    try:
        post = Post.objects.get(slug=slug, published=True)
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")
    comment = Comment.objects.create(post=post, author=current_user, content=data.content)
    return CommentOut(
        id=comment.id,
        author={"id": current_user.id, "username": current_user.username},
        content=comment.content,
        created_at=comment.created_at,
    )
