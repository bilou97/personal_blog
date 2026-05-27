import logging

from django.utils import timezone

from blog.models import Post

from .cache import cache_delete

logger = logging.getLogger(__name__)


def publish_scheduled_posts() -> int:
    now = timezone.now()
    ids = list(
        Post.objects.filter(
            published=False,
            published_at__isnull=False,
            published_at__lte=now,
        ).values_list("pk", flat=True)
    )
    if not ids:
        return 0

    updated = Post.objects.filter(pk__in=ids, published=False).update(published=True)
    if not updated:
        return 0

    cache_delete("posts:*")
    logger.info("Published %d scheduled post(s)", updated)

    from .newsletter import send_newsletter_for_post
    for post in Post.objects.filter(pk__in=ids):
        try:
            count = send_newsletter_for_post(post)
            if count:
                logger.info("Newsletter: '%s' → %d subscriber(s)", post.slug, count)
        except Exception:
            logger.exception("Newsletter failed for '%s'", post.slug)

    return updated
