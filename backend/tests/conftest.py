import pytest
from starlette.testclient import TestClient

from api.deps import create_access_token
from api.main import app
from blog.models import Category, Post, Tag
from django.contrib.auth.models import User


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def user(transactional_db):
    return User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="password123",
    )


@pytest.fixture
def auth_headers(user):
    token = create_access_token(user.pk)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def category(transactional_db):
    return Category.objects.create(name="Python")


@pytest.fixture
def tag(transactional_db):
    return Tag.objects.create(name="Django")


@pytest.fixture
def published_post(transactional_db, category, tag):
    post = Post.objects.create(
        title="Mon premier article",
        content="# Titre\n\nContenu en **markdown**.",
        excerpt="Un résumé court.",
        category=category,
        published=True,
        published_at="2026-01-15T10:00:00+00:00",
    )
    post.tags.add(tag)
    return post


@pytest.fixture
def unpublished_post(transactional_db):
    return Post.objects.create(
        title="Brouillon",
        content="Pas encore publié.",
        excerpt="Brouillon.",
        published=False,
    )
