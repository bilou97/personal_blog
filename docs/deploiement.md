# Déploiement en production

## Prérequis

- VM Linux avec Docker + Docker Compose installés
- Nom de domaine pointant vers l'IP de la VM
- Ports 80 et 443 ouverts

## Première installation

```bash
# 1. Cloner le repo sur la VM
git clone https://github.com/bilou97/personal_blog.git && cd personal_blog

# 2. Configurer l'environnement
cp .env.example .env
```

Éditer `.env` et renseigner :

```
SECRET_KEY=<clé aléatoire longue>
JWT_SECRET_KEY=<clé aléatoire longue>
DB_PASSWORD=<mot de passe fort>
ALLOWED_HOSTS=ton-domaine.ch
DJANGO_SETTINGS_MODULE=config.settings.prod
```

```bash
# 3. Obtenir le certificat SSL
bash scripts/init-letsencrypt.sh ton-domaine.ch admin@exemple.com

# 4. Lancer en production
bash scripts/start-prod.sh

# 5. Créer le superuser admin
docker compose exec backend python manage.py createsuperuser
```

## Mises à jour

```bash
git pull
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

Les migrations sont appliquées automatiquement au redémarrage du conteneur.

## Renouvellement SSL

Let's Encrypt renouvelle automatiquement le certificat via le conteneur `certbot` configuré dans `docker-compose.prod.yml`. Aucune action manuelle requise.

## Sauvegarde de la base de données

```bash
# Dump
docker compose exec db pg_dump -U $DB_USER $DB_NAME > backup_$(date +%Y%m%d).sql

# Restauration
docker compose exec -T db psql -U $DB_USER $DB_NAME < backup_20260101.sql
```

## Vérifications post-déploiement

```bash
# État des conteneurs
docker compose ps

# Logs backend
docker compose logs -f backend

# Tester l'API
curl https://ton-domaine.ch/api/posts
```
