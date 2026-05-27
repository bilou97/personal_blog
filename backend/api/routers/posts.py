from typing import Optional

from django.db.models import Count, F
from fastapi import APIRouter, HTTPException, Query

from blog.models import Category, Post, Tag
from ..cache import cache_get, cache_set
from ..schemas.posts import (
    CategoryOut,
    PaginatedPostListOut,
    PostDetailOut,
    PostListOut,
    TagOut,
)

router = APIRouter()

_TTL_LIST = 300       # 5 min
_TTL_META = 1800      # 30 min
_TTL_RELATED = 600    # 10 min


def _serialize_post_list(post) -> PostListOut:
    cover = (
        post.cover_image.url
        if post.cover_image and post.cover_image.name
        else None
    )
    cat = (
        CategoryOut(
            id=post.category.id,
            name=post.category.name,
            slug=post.category.slug,
        )
        if post.category
        else None
    )
    return PostListOut(
        id=post.id,
        title=post.title,
        slug=post.slug,
        excerpt=post.excerpt,
        cover_image=cover,
        category=cat,
        tags=[TagOut(id=t.id, name=t.name, slug=t.slug) for t in post.tags.all()],
        published_at=post.published_at,
        views=post.views,
    )


@router.get("", response_model=PaginatedPostListOut)
def list_posts(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    category: Optional[str] = None,
    tag: Optional[str] = None,
):
    key = f"posts:list:p{page}:ps{page_size}:c{category}:t{tag}"
    cached = cache_get(key)
    if cached:
        return cached

    qs = (
        Post.objects.filter(published=True)
        .select_related("category")
        .prefetch_related("tags")
        .order_by("-published_at")
    )
    if category:
        qs = qs.filter(category__slug=category)
    if tag:
        qs = qs.filter(tags__slug=tag)
    total = qs.count()
    offset = (page - 1) * page_size
    results = [_serialize_post_list(p) for p in qs[offset:offset + page_size]]
    response = PaginatedPostListOut(
        total=total, page=page, page_size=page_size, results=results
    )
    cache_set(key, response.model_dump(), _TTL_LIST)
    return response


@router.get("/categories", response_model=list[CategoryOut])
def list_categories():
    cached = cache_get("posts:categories")
    if cached:
        return cached

    result = [
        CategoryOut(id=c.id, name=c.name, slug=c.slug)
        for c in Category.objects.all()
    ]
    cache_set("posts:categories", [r.model_dump() for r in result], _TTL_META)
    return result


@router.get("/tags", response_model=list[TagOut])
def list_tags():
    cached = cache_get("posts:tags")
    if cached:
        return cached

    result = [
        TagOut(id=t.id, name=t.name, slug=t.slug)
        for t in Tag.objects.all()
    ]
    cache_set("posts:tags", [r.model_dump() for r in result], _TTL_META)
    return result


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

    Post.objects.filter(pk=post.pk).update(views=F("views") + 1)

    base_data = _serialize_post_list(post).model_dump()
    base_data["views"] = post.views + 1
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


@router.get("/{slug}/related", response_model=list[PostListOut])
def get_related_posts(slug: str):
    key = f"posts:related:{slug}"
    cached = cache_get(key)
    if cached:
        return cached

    try:
        post = Post.objects.prefetch_related("tags").get(
            slug=slug, published=True
        )
    except Post.DoesNotExist:
        raise HTTPException(status_code=404, detail="Post not found")

    tag_ids = list(post.tags.values_list("id", flat=True))

    related = list(
        Post.objects.filter(published=True, tags__in=tag_ids)
        .exclude(pk=post.pk)
        .annotate(common_tags=Count("id"))
        .order_by("-common_tags", "-published_at")
        .select_related("category")
        .prefetch_related("tags")
        .distinct()[:3]
    )

    if len(related) < 3 and post.category:
        existing_ids = {p.pk for p in related} | {post.pk}
        fill = list(
            Post.objects.filter(published=True, category=post.category)
            .exclude(pk__in=existing_ids)
            .select_related("category")
            .prefetch_related("tags")
            .order_by("-published_at")[: 3 - len(related)]
        )
        related += fill

    result = [_serialize_post_list(p) for p in related]
    cache_set(key, [r.model_dump() for r in result], _TTL_RELATED)
    return result
