# Déploiement en production

## Architecture

Le blog ne gère pas lui-même le SSL ni le reverse proxy. En production, un projet
**nginx-gateway** séparé (basé sur Caddy) tourne sur la même VM et achemine le trafic
vers les conteneurs du blog via le réseau Docker interne.

```
Internet → Caddy (nginx-gateway) → personal_blog_default network
                                        ├── frontend :5173
                                        └── backend  :8000
```

---

## 1. Déployer le blog

### Prérequis

- VM Linux avec Docker + Docker Compose
- Ports 80 et 443 ouverts (gérés par le projet nginx-gateway)

### Installation

```bash
# Cloner le repo sur la VM
git clone https://github.com/bilou97/personal_blog.git && cd personal_blog

# Configurer l'environnement
cp .env.example .env
```

Éditer `.env` :

```
SECRET_KEY=<clé aléatoire longue>
JWT_SECRET_KEY=<clé aléatoire longue>
DB_PASSWORD=<mot de passe fort>
ALLOWED_HOSTS=blog.ton-domaine.ch
DJANGO_SETTINGS_MODULE=config.settings.prod
```

```bash
# Lancer les conteneurs
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build

# Créer le superuser admin
docker compose exec backend python manage.py createsuperuser
```

---

## 2. Configurer le reverse proxy (nginx-gateway)

> **Requis pour exposer le blog sur internet.** Cette étape suppose que le projet
> `nginx-gateway` est déjà en place sur la VM (il peut héberger d'autres projets).

### Si nginx-gateway n'existe pas encore

Créer un projet dédié avec Caddy :

```bash
mkdir nginx-gateway && cd nginx-gateway
```

`docker-compose.yml` :

```yaml
services:
  caddy:
    image: caddy:alpine
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
      - caddy_config:/config
    networks:
      - personal_blog_default

volumes:
  caddy_data:
  caddy_config:

networks:
  personal_blog_default:
    external: true
```

`Caddyfile` :

```
blog.ton-domaine.ch {
    reverse_proxy /api/* backend:8000
    reverse_proxy /media/* backend:8000
    reverse_proxy frontend:5173
}
```

```bash
docker compose up -d
```

Caddy obtient et renouvelle automatiquement le certificat Let's Encrypt.

### Si nginx-gateway tourne déjà

Ajouter le réseau `personal_blog_default` au service Caddy existant et ajouter le
bloc `blog.ton-domaine.ch` dans le `Caddyfile`, puis `docker compose restart caddy`.

---

## Mises à jour du blog

```bash
git pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Les migrations sont appliquées automatiquement au démarrage du conteneur.

---

## Sauvegarde de la base de données

```bash
# Dump
docker compose exec db pg_dump -U $DB_USER $DB_NAME > backup_$(date +%Y%m%d).sql

# Restauration
docker compose exec -T db psql -U $DB_USER $DB_NAME < backup_20260101.sql
```

---

## Vérifications post-déploiement

```bash
docker compose ps
docker compose logs -f backend
curl https://blog.ton-domaine.ch/api/posts
```
