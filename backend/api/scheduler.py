import logging

from django.utils import timezone

from blog.models import Post

from .cache import cache_delete

logger = logging.getLogger(__name__)


def publish_scheduled_posts() -> int:
    count = Post.objects.filter(
        published=False,
        published_at__isnull=False,
        published_at__lte=timezone.now(),
    ).update(published=True)
    if count:
        cache_delete("posts:*")
        logger.info("Published %d scheduled post(s)", count)
    return count
