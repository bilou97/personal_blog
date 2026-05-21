# Architecture

## Vue d'ensemble

```
Navigateur
    │
    ├── / et /post/*         → Vue.js SPA (port 5173 en dev, nginx en prod)
    ├── /api/*               → FastAPI  (REST, JWT)
    ├── /admin/              → Django Admin
    ├── /static/             → fichiers Django collectés
    └── /media/              → uploads images
```

**Django et FastAPI cohabitent dans le même conteneur.** Le fichier `config/asgi.py` route les requêtes `/api/*` vers FastAPI et tout le reste vers Django. Django fournit l'ORM, les migrations et l'admin. FastAPI expose les endpoints REST que Vue.js consomme.

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
│   │   ├── migrations/
│   │   └── management/commands/
│   │       └── seed_data.py      # données de test
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
├── docs/                         # documentation
│
└── scripts/
    ├── start-dev.sh              # copie .env + docker compose up
    ├── start-prod.sh             # docker compose prod up -d
    └── init-letsencrypt.sh       # obtenir le premier certificat SSL
```

## Modèles de données

### Post
| Champ | Type | Notes |
|---|---|---|
| title | CharField | max 200 caractères |
| slug | SlugField | auto-généré depuis title |
| content | TextField | Markdown |
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

### Category
| Champ | Type | Notes |
|---|---|---|
| name | CharField | unique, max 100 caractères |
| slug | SlugField | auto-généré |

### Tag
| Champ | Type | Notes |
|---|---|---|
| name | CharField | unique, max 50 caractères |
| slug | SlugField | auto-généré |

## Authentification

JWT sans état. Le token est stocké dans le store Pinia (mémoire) et injecté dans chaque requête via un intercepteur axios. Un intercepteur de réponse gère le logout automatique sur erreur 401.

- Access token : durée courte
- Pas de refresh token pour l'instant
