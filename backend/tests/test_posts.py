import pytest

pytestmark = pytest.mark.django_db(transaction=True)


def test_list_posts_empty(client):
    r = client.get("/api/posts")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 0
    assert body["results"] == []
    assert body["page"] == 1


def test_list_posts(client, published_post):
    r = client.get("/api/posts")
    assert r.status_code == 200
    body = r.json()
    assert body["total"] == 1
    assert len(body["results"]) == 1
    post = body["results"][0]
    assert post["slug"] == published_post.slug
    assert post["title"] == published_post.title
    assert post["category"]["slug"] == "python"


def test_list_posts_unpublished_excluded(client, unpublished_post):
    r = client.get("/api/posts")
    assert r.json()["total"] == 0


def test_list_posts_pagination(client, db):
    from blog.models import Post
    for i in range(3):
        Post.objects.create(
            title=f"Article {i}",
            content="contenu",
            excerpt="extrait",
            published=True,
            published_at=f"2026-01-{i + 1:02d}T00:00:00+00:00",
        )
    r = client.get("/api/posts?page=1&page_size=2")
    body = r.json()
    assert body["total"] == 3
    assert len(body["results"]) == 2
    assert body["page"] == 1

    r2 = client.get("/api/posts?page=2&page_size=2")
    assert len(r2.json()["results"]) == 1


def test_list_posts_filter_by_category(client, published_post, db):
    from blog.models import Category, Post
    other_cat = Category.objects.create(name="JavaScript")
    Post.objects.create(
        title="Article JS",
        content="contenu",
        excerpt="extrait",
        category=other_cat,
        published=True,
        published_at="2026-01-20T00:00:00+00:00",
    )
    r = client.get("/api/posts?category=python")
    body = r.json()
    assert body["total"] == 1
    assert body["results"][0]["category"]["slug"] == "python"


def test_list_posts_filter_by_tag(client, published_post, db):
    from blog.models import Post, Tag
    other_tag = Tag.objects.create(name="Flask")
    p2 = Post.objects.create(
        title="Article Flask",
        content="contenu",
        excerpt="extrait",
        published=True,
        published_at="2026-01-20T00:00:00+00:00",
    )
    p2.tags.add(other_tag)

    r = client.get("/api/posts?tag=django")
    body = r.json()
    assert body["total"] == 1
    assert body["results"][0]["slug"] == published_post.slug


def test_get_post(client, published_post):
    r = client.get(f"/api/posts/{published_post.slug}")
    assert r.status_code == 200
    body = r.json()
    assert body["title"] == published_post.title
    assert "content" in body
    assert "comments" in body


def test_get_post_not_found(client, db):
    r = client.get("/api/posts/slug-inexistant")
    assert r.status_code == 404


def test_get_post_unpublished_returns_404(client, unpublished_post):
    r = client.get(f"/api/posts/{unpublished_post.slug}")
    assert r.status_code == 404


def test_list_categories(client, category):
    r = client.get("/api/posts/categories")
    assert r.status_code == 200
    slugs = [c["slug"] for c in r.json()]
    assert "python" in slugs


def test_list_tags(client, tag):
    r = client.get("/api/posts/tags")
    assert r.status_code == 200
    slugs = [t["slug"] for t in r.json()]
    assert "django" in slugs
