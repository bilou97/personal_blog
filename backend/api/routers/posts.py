from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from blog.models import Category, Post, Tag
from ..schemas.posts import CategoryOut, PostDetailOut, PostListOut, TagOut

router = APIRouter()


def _serialize_post_list(post) -> PostListOut:
    return PostListOut(
        id=post.id,
        title=post.title,
        slug=post.slug,
        excerpt=post.excerpt,
        cover_image=post.cover_image.url if post.cover_image and post.cover_image.name else None,
        category=CategoryOut(id=post.category.id, name=post.category.name, slug=post.category.slug)
        if post.category
        else None,
        tags=[TagOut(id=t.id, name=t.name, slug=t.slug) for t in post.tags.all()],
        published_at=post.published_at,
    )


@router.get("", response_model=list[PostListOut])
def list_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    category: Optional[str] = None,
    tag: Optional[str] = None,
):
    qs = Post.objects.filter(published=True).select_related("category").prefetch_related("tags")
    if category:
        qs = qs.filter(category__slug=category)
    if tag:
        qs = qs.filter(tags__slug=tag)
    offset = (page - 1) * page_size
    return [_serialize_post_list(p) for p in qs[offset : offset + page_size]]


@router.get("/categories", response_model=list[CategoryOut])
def list_categories():
    return [CategoryOut(id=c.id, name=c.name, slug=c.slug) for c in Category.objects.all()]


@router.get("/tags", response_model=list[TagOut])
def list_tags():
    return [TagOut(id=t.id, name=t.name, slug=t.slug) for t in Tag.objects.all()]


@router.get("/{slug}", response_model=PostDetailOut)
def get_post(slug: str):
    try:
        post = (
            Post.objects.filter(published=True)
            .select_related("category")
            .prefetch_related("tags", "comments__author")
            .get(slug=slug)
        )
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

    base = _serialize_post_list(post)
    return PostDetailOut(
        **base.model_dump(),
        content=post.content,
        comments=[
            {"id": c.id, "author": {"id": c.author.id, "username": c.author.username},
             "content": c.content, "created_at": c.created_at}
            for c in post.comments.filter(approved=True)
        ],
    )
