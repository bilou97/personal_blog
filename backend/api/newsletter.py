import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from blog.models import Post, Subscriber

from .deps import create_unsubscribe_token

logger = logging.getLogger(__name__)


def send_newsletter_for_post(post: Post) -> int:
    subscribers = list(Subscriber.objects.all())
    if not subscribers:
        return 0

    site_url = getattr(settings, "SITE_URL", "http://localhost:5173")
    post_url = f"{site_url}/post/{post.slug}"
    sent = 0

    for sub in subscribers:
        token = create_unsubscribe_token(sub.email)
        unsub_url = f"{site_url}/unsubscribe?token={token}"

        text_body = (
            f"{post.title}\n\n"
            f"{post.excerpt}\n\n"
            f"Lire l'article : {post_url}\n\n"
            f"---\nSe désabonner : {unsub_url}"
        )
        html_body = (
            f"<h2>{post.title}</h2>"
            f"<p>{post.excerpt}</p>"
            f'<p><a href="{post_url}">Lire l\'article →</a></p>'
            f'<hr><p style="font-size:12px;color:#888">'
            f'<a href="{unsub_url}">Se désabonner</a></p>'
        )

        msg = EmailMultiAlternatives(
            subject=f"Nouvel article : {post.title}",
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[sub.email],
        )
        msg.attach_alternative(html_body, "text/html")
        try:
            msg.send(fail_silently=False)
            sent += 1
        except Exception:
            logger.exception("Failed to send newsletter to %s", sub.email)

    return sent
