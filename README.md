# Blog — Vue.js + FastAPI + Django

Blog personnel dockerisé. Frontend Vue.js, API FastAPI, backend Django (admin + ORM), base PostgreSQL.

---

## Stack

| Couche | Technologie |
|---|---|
| Frontend | Vue 3 + Vite + Pinia + Vue Router |
| API | FastAPI (Python 3.12) |
| Backend | Django 5 (ORM, Admin, migrations) |
| Base de données | PostgreSQL 16 |
| Proxy (prod) | Nginx + Let's Encrypt |
| Conteneurs | Docker Compose |

---

## Architecture

```
Navigateur
    │
    ├── / et /post/*         → Vue.js SPA
    ├── /api/*               → FastAPI  (REST, JWT)
    ├── /admin/              → Django Admin
    ├── /static/             → fichiers Django collectés
    └── /media/              → uploads images
```

**Django et FastAPI cohabitent dans le même conteneur.** Le fichier `config/asgi.py`
route les requêtes `/api/*` vers FastAPI et tout le reste vers Django. Django fournit
l'ORM, les migrations et l'admin. FastAPI expose les endpoints REST que Vue.js consomme.

---

## Structure du projet

```
blog/
├── docker-compose.yml            # base partagée
├── docker-compose.override.yml   # overrides dev (appliqués automatiquement)
├── docker-compose.prod.yml       # overrides prod
├── .env.example                  # template des variables d'environnement
├── .gitignore
│
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   ├── config/
│   │   ├── asgi.py               # routage Django ↔ FastAPI
│   │   ├── urls.py               # routes Django (/admin, /static, /media)
│   │   └── settings/
│   │       ├── base.py           # settings communs
│   │       ├── dev.py            # DEBUG=True, CORS ouvert
│   │       └── prod.py           # HTTPS, HSTS, ALLOWED_HOSTS depuis .env
│   ├── blog/                     # app Django
│   │   ├── models.py             # Post, Category, Tag, Comment
│   │   ├── admin.py              # configuration de l'interface admin
│   │   └── migrations/
│   └── api/                      # app FastAPI
│       ├── main.py               # instance FastAPI + middleware CORS
│       ├── deps.py               # JWT : création, vérification, get_current_user
│       ├── routers/
│       │   ├── posts.py          # GET /api/posts, GET /api/posts/{slug}
│       │   ├── auth.py           # POST /api/auth/register|login
│       │   └── comments.py       # POST /api/posts/{slug}/comments
│       └── schemas/
│           ├── posts.py          # PostListOut, PostDetailOut, CategoryOut, TagOut
│           ├── auth.py           # RegisterRequest, LoginRequest, TokenOut
│           └── comments.py       # CommentCreate, CommentOut
│
├── frontend/
│   ├── Dockerfile                # image dev (vite dev server)
│   ├── Dockerfile.prod           # image prod (build → nginx)
│   ├── nginx.conf                # nginx interne au conteneur prod
│   ├── package.json
│   ├── vite.config.js            # proxy /api → backend:8000
│   └── src/
│       ├── main.js
│       ├── App.vue               # layout : navbar + <RouterView>
│       ├── api.js                # instance axios (injecte le token JWT)
│       ├── router/index.js       # routes Vue
│       ├── stores/auth.js        # Pinia : token JWT, login, logout
│       └── views/
│           ├── HomeView.vue      # liste des articles
│           ├── PostView.vue      # article + commentaires
│           ├── LoginView.vue
│           └── RegisterView.vue
│
├── nginx/
│   └── nginx.prod.conf           # reverse proxy HTTPS + Let's Encrypt
│
└── scripts/
    ├── start-dev.sh              # copie .env + docker compose up
    ├── start-prod.sh             # docker compose prod up -d
    └── init-letsencrypt.sh       # obtenir le premier certificat SSL
```

---

## Démarrage en dev (local)

### Première fois

```bash
# 1. Copier les variables d'environnement
cp .env.example .env

# 2. Lancer les conteneurs
docker compose up --build

# 3. Générer les fichiers de migration (une seule fois, puis committer)
docker compose exec backend python manage.py makemigrations blog

# 4. Appliquer les migrations
docker compose exec backend python manage.py migrate

# 5. Créer le superuser admin
docker compose exec backend python manage.py createsuperuser
```

### Les fois suivantes

```bash
docker compose up
```

Les migrations sont appliquées automatiquement au démarrage du conteneur.

| URL | Description |
|---|---|
| http://localhost:5173 | Frontend Vue.js |
| http://localhost:8000/admin | Django Admin |
| http://localhost:8000/docs | Swagger UI FastAPI |
| http://localhost:8000/redoc | ReDoc FastAPI |

---

## Déploiement en production (VM)

### Première installation

```bash
# 1. Cloner le repo sur la VM
git clone <repo> && cd blog

# 2. Configurer l'environnement
cp .env.example .env
# Éditer .env : SECRET_KEY, JWT_SECRET_KEY, DB_PASSWORD, ALLOWED_HOSTS, DJANGO_SETTINGS_MODULE=config.settings.prod

# 3. Obtenir le certificat SSL (remplace DOMAIN dans nginx.prod.conf et lance certbot)
bash scripts/init-letsencrypt.sh ton-domaine.com admin@exemple.com

# 4. Lancer en prod
bash scripts/start-prod.sh

# 5. Créer le superuser admin
docker compose exec backend python manage.py createsuperuser
```

### Mises à jour

```bash
git pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

---

## Modèles de données

### Post
| Champ | Type | Notes |
|---|---|---|
| title | CharField | |
| slug | SlugField | auto-généré depuis title |
| content | TextField | HTML ou Markdown brut |
| excerpt | TextField | max 500 caractères |
| cover_image | ImageField | stockée dans `/media/posts/` |
| category | ForeignKey → Category | nullable |
| tags | ManyToMany → Tag | |
| published | BooleanField | contrôle la visibilité |
| published_at | DateTimeField | nullable |

### Comment
| Champ | Type | Notes |
|---|---|---|
| post | ForeignKey → Post | |
| author | ForeignKey → User (Django) | |
| content | TextField | max 2000 caractères |
| approved | BooleanField | modération depuis l'admin |

---

## Endpoints API

| Méthode | URL | Auth | Description |
|---|---|---|---|
| GET | /api/posts | — | Liste des articles publiés (paginée) |
| GET | /api/posts/{slug} | — | Article + commentaires approuvés |
| GET | /api/posts/categories | — | Liste des catégories |
| GET | /api/posts/tags | — | Liste des tags |
| POST | /api/auth/register | — | Créer un compte |
| POST | /api/auth/login | — | Obtenir un token JWT |
| POST | /api/posts/{slug}/comments | JWT | Poster un commentaire |

Paramètres de liste : `?page=1&page_size=10&category=<slug>&tag=<slug>`

---

## Prochaines étapes

- [ ] Ajouter du style (Tailwind CSS ou similaire)
- [ ] Rendu Markdown dans les articles (`marked` ou `markdown-it`)
- [ ] Pagination UI dans HomeView
- [ ] Filtres par catégorie et tag dans la navbar
- [ ] SEO : balises meta dynamiques (vue-meta ou `useHead`)
- [ ] Gestion des erreurs globale (intercepteur axios)
- [ ] Tests backend (pytest + pytest-django)
