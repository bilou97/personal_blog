from fastapi import APIRouter, Depends, HTTPException, Request

from blog.models import Post
from ..deps import (
    _PREVIEW_TTL_HOURS,
    create_preview_token,
    get_current_user,
    verify_preview_token,
)
from ..routers.posts import _serialize_post_list
from ..schemas.posts import PostDetailOut

router = APIRouter()


@router.post("/{slug}/token")
def generate_preview_token(
    slug: str,
    request: Request,
    _=Depends(get_current_user),
):
    try:
        Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

    token = create_preview_token(slug)
    origin = request.headers.get("origin") or str(request.base_url).rstrip("/")
    return {
        "token": token,
        "url": f"{origin}/preview/{token}",
        "expires_in": _PREVIEW_TTL_HOURS * 3600,
    }


@router.get("/{token}", response_model=PostDetailOut)
def get_preview(token: str):
    slug = verify_preview_token(token)
    try:
        post = (
            Post.objects.select_related("category")
            .prefetch_related("tags", "comments__author")
            .get(slug=slug)
        )
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

    base_data = _serialize_post_list(post).model_dump()
    return PostDetailOut(
        **base_data,
        content=post.content,
        comments=[
            {
                "id": c.id,
                "author": {"id": c.author.id, "username": c.author.username},
                "content": c.content,
                "created_at": c.created_at,
            }
            for c in post.comments.filter(approved=True)
        ],
    )
