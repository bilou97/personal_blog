# Blog personnel

Blog dockerisé avec Vue.js, FastAPI, Django et PostgreSQL.

## Stack

| Couche | Technologie |
|---|---|
| Frontend | Vue 3 + Vite + Pinia + Vue Router |
| API | FastAPI (Python 3.12) |
| Backend | Django 5 (ORM, Admin, migrations) |
| Base de données | PostgreSQL 16 |
| Proxy (prod) | Nginx + Let's Encrypt |
| Conteneurs | Docker Compose |

## Démarrage rapide

```bash
cp .env.example .env
docker compose up -d --build
docker compose exec backend python manage.py createsuperuser
```

| URL | Description |
|---|---|
| http://localhost:5173 | Frontend |
| http://localhost:8000/admin | Django Admin |
| http://localhost:8000/docs | API (Swagger) |

## Documentation

- [Architecture](docs/architecture.md) — structure du projet, modèles, routage ASGI
- [Développement](docs/developpement.md) — setup local, commandes utiles, tests
- [Déploiement](docs/deploiement.md) — production, SSL, mises à jour
- [API](docs/api.md) — référence des endpoints
- [Roadmap](docs/roadmap.md) — fonctionnalités réalisées et à venir
