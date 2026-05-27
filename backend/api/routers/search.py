from fastapi import APIRouter, Query
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector

from blog.models import Post
from ..routers.posts import _serialize_post_list
from ..schemas.posts import PaginatedPostListOut

router = APIRouter()


@router.get("", response_model=PaginatedPostListOut)
def search_posts(
    q: str = Query(..., min_length=1, max_length=200),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
):
    q = q.strip()
    if not q:
        return PaginatedPostListOut(total=0, page=page, page_size=page_size, results=[])

    try:
        query = SearchQuery(q, config="simple", search_type="websearch")
    except Exception:
        query = SearchQuery(q, config="simple")

    vector = SearchVector("title", weight="A", config="simple") + SearchVector(
        "content", weight="B", config="simple"
    )

    qs = (
        Post.objects.filter(published=True)
        .annotate(rank=SearchRank(vector, query))
        .filter(rank__gt=0)
        .select_related("category")
        .prefetch_related("tags")
        .order_by("-rank", "-published_at")
    )

    total = qs.count()
    offset = (page - 1) * page_size
    results = [_serialize_post_list(p) for p in qs[offset : offset + page_size]]
    return PaginatedPostListOut(
        total=total, page=page, page_size=page_size, results=results
    )
