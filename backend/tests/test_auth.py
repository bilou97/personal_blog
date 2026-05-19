import pytest

pytestmark = pytest.mark.django_db(transaction=True)


def test_register(client):
    r = client.post("/api/auth/register", json={
        "username": "nouveau",
        "email": "nouveau@example.com",
        "password": "motdepasse123",
    })
    assert r.status_code == 201
    assert "access_token" in r.json()


def test_register_duplicate_username(client, user):
    r = client.post("/api/auth/register", json={
        "username": user.username,
        "email": "autre@example.com",
        "password": "motdepasse123",
    })
    assert r.status_code == 400
    assert "username" in r.json()["detail"].lower()


def test_register_duplicate_email(client, user):
    r = client.post("/api/auth/register", json={
        "username": "autreuser",
        "email": user.email,
        "password": "motdepasse123",
    })
    assert r.status_code == 400
    assert "email" in r.json()["detail"].lower()


def test_login(client, user):
    r = client.post("/api/auth/login", json={
        "username": user.username,
        "password": "password123",
    })
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client, user):
    r = client.post("/api/auth/login", json={
        "username": user.username,
        "password": "mauvais",
    })
    assert r.status_code == 401


def test_login_unknown_user(client, db):
    r = client.post("/api/auth/login", json={
        "username": "inexistant",
        "password": "password",
    })
    assert r.status_code == 401
