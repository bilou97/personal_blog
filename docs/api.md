# Référence API

Base URL : `/api`

La documentation interactive est disponible en local sur http://localhost:8000/docs (Swagger UI) et http://localhost:8000/redoc.

## Authentification

Les endpoints protégés nécessitent un header :

```
Authorization: Bearer <access_token>
```

Le token est obtenu via `POST /api/auth/login`.

---

## Auth

### POST /api/auth/register

Créer un compte utilisateur.

**Body**
```json
{
  "username": "alice",
  "email": "alice@example.com",
  "password": "motdepasse"
}
```

**Réponse** `201`
```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com"
}
```

---

### POST /api/auth/login

Obtenir un token JWT.

**Body**
```json
{
  "username": "alice",
  "password": "motdepasse"
}
```

**Réponse** `200`
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

## Posts

### GET /api/posts

Liste des articles publiés, triés par date de publication décroissante.

**Paramètres**

| Paramètre | Type | Défaut | Description |
|---|---|---|---|
| page | int | 1 | Numéro de page |
| page_size | int | 10 | Articles par page |
| category | string | — | Slug de catégorie |
| tag | string | — | Slug de tag |

**Réponse** `200`
```json
{
  "total": 42,
  "page": 1,
  "page_size": 10,
  "results": [
    {
      "id": 1,
      "title": "Mon article",
      "slug": "mon-article",
      "excerpt": "Introduction courte...",
      "cover_image": "/media/posts/image.jpg",
      "category": { "id": 1, "name": "Dev web", "slug": "dev-web" },
      "tags": [{ "id": 1, "name": "Python", "slug": "python" }],
      "published_at": "2026-05-01T10:00:00Z"
    }
  ]
}
```

---

### GET /api/posts/{slug}

Détail d'un article avec ses commentaires approuvés.

**Réponse** `200`
```json
{
  "id": 1,
  "title": "Mon article",
  "slug": "mon-article",
  "content": "Contenu en markdown...",
  "excerpt": "Introduction courte...",
  "cover_image": "/media/posts/image.jpg",
  "category": { "id": 1, "name": "Dev web", "slug": "dev-web" },
  "tags": [{ "id": 1, "name": "Python", "slug": "python" }],
  "published_at": "2026-05-01T10:00:00Z",
  "comments": [
    {
      "id": 1,
      "author": "alice",
      "content": "Super article !",
      "created_at": "2026-05-02T08:30:00Z"
    }
  ]
}
```

**Erreurs**

| Code | Description |
|---|---|
| 404 | Article non trouvé ou non publié |

---

### GET /api/posts/categories

Liste de toutes les catégories.

**Réponse** `200`
```json
[
  { "id": 1, "name": "Développement web", "slug": "developpement-web" }
]
```

---

### GET /api/posts/tags

Liste de tous les tags.

**Réponse** `200`
```json
[
  { "id": 1, "name": "Python", "slug": "python" }
]
```

---

## Commentaires

### POST /api/posts/{slug}/comments

Poster un commentaire sur un article. Authentification requise.

**Header** : `Authorization: Bearer <token>`

**Body**
```json
{
  "content": "Très bon article !"
}
```

**Réponse** `201`
```json
{
  "id": 42,
  "author": "alice",
  "content": "Très bon article !",
  "created_at": "2026-05-22T14:00:00Z"
}
```

**Erreurs**

| Code | Description |
|---|---|
| 401 | Token manquant ou invalide |
| 404 | Article non trouvé |
