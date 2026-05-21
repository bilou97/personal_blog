# Développement local

## Prérequis

- Docker + Docker Compose
- Git

## Première installation

```bash
# 1. Copier les variables d'environnement
cp .env.example .env

# 2. Lancer les conteneurs (build inclus)
docker compose up -d --build

# 3. Créer le superuser admin
docker compose exec backend python manage.py createsuperuser
```

Les migrations sont appliquées automatiquement au démarrage du conteneur.

## Les fois suivantes

```bash
docker compose up -d
```

## URLs locales

| URL | Description |
|---|---|
| http://localhost:5173 | Frontend Vue.js |
| http://localhost:8000/admin | Django Admin |
| http://localhost:8000/docs | Swagger UI (FastAPI) |
| http://localhost:8000/redoc | ReDoc (FastAPI) |

## Données de test

Un management command génère des données fictives (catégories, tags, articles, commentaires) :

```bash
# Injecter les données
docker compose exec backend python manage.py seed_data

# Réinitialiser et réinjecter
docker compose exec backend python manage.py seed_data --clear
```

## Gestion des mots de passe

```bash
# Changer le mot de passe d'un utilisateur (avec validation)
docker compose exec backend python manage.py changepassword <username>

# Forcer un mot de passe sans validation (utile en local)
docker compose exec backend python manage.py shell -c "
from django.contrib.auth.models import User
u = User.objects.get(username='<username>')
u.set_password('nouveaumotdepasse')
u.save()
"
```

## Tests

Les tests utilisent pytest + pytest-django et tournent contre la base PostgreSQL du conteneur.

```bash
# Lancer tous les tests
docker compose exec backend pytest tests/ -v

# Lancer un fichier ou un test spécifique
docker compose exec backend pytest tests/test_posts.py -v
docker compose exec backend pytest tests/test_posts.py::test_list_posts -v
```

La base de test (`test_blog`) est réutilisée entre les runs grâce à `--reuse-db` dans `pytest.ini`.

## Commandes utiles

```bash
# Voir les logs en temps réel
docker compose logs -f backend
docker compose logs -f frontend

# Entrer dans le container backend
docker compose exec backend bash

# Shell Django
docker compose exec backend python manage.py shell

# Créer de nouvelles migrations après modification d'un modèle
docker compose exec backend python manage.py makemigrations blog

# Reset complet (supprime les volumes)
docker compose down -v && docker compose up -d --build
```
