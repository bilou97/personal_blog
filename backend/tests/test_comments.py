import pytest

pytestmark = pytest.mark.django_db(transaction=True)


def test_add_comment(client, published_post, auth_headers):
    r = client.post(
        f"/api/posts/{published_post.slug}/comments",
        json={"content": "Super article !"},
        headers=auth_headers,
    )
    assert r.status_code == 201
    body = r.json()
    assert body["content"] == "Super article !"
    assert body["author"]["username"] == "testuser"


def test_add_comment_unauthenticated(client, published_post):
    r = client.post(
        f"/api/posts/{published_post.slug}/comments",
        json={"content": "Commentaire sans token"},
    )
    assert r.status_code == 401


def test_add_comment_post_not_found(client, auth_headers, db):
    r = client.post(
        "/api/posts/slug-inexistant/comments",
        json={"content": "Commentaire"},
        headers=auth_headers,
    )
    assert r.status_code == 404


def test_add_comment_only_shows_approved(client, published_post, auth_headers):
    from blog.models import Comment
    client.post(
        f"/api/posts/{published_post.slug}/comments",
        json={"content": "Commentaire approuvé"},
        headers=auth_headers,
    )
    Comment.objects.filter(post=published_post).update(approved=False)

    r = client.get(f"/api/posts/{published_post.slug}")
    assert r.json()["comments"] == []
