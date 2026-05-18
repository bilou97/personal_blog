#!/bin/bash
# Obtenir le premier certificat Let's Encrypt sur la VM.
# Usage : bash scripts/init-letsencrypt.sh your-domain.com admin@example.com
set -e

DOMAIN="${1:?Usage: $0 <domain> <email>}"
EMAIL="${2:?Usage: $0 <domain> <email>}"
COMPOSE="docker compose -f docker-compose.yml -f docker-compose.prod.yml"

# Remplacer le placeholder DOMAIN dans nginx.prod.conf
sed -i "s/DOMAIN/$DOMAIN/g" nginx/nginx.prod.conf

# Démarrer nginx seul (HTTP uniquement, pas de SSL encore)
$COMPOSE up -d nginx

# Obtenir le certificat
$COMPOSE run --rm certbot certbot certonly \
  --webroot -w /var/www/certbot \
  -d "$DOMAIN" -d "www.$DOMAIN" \
  --email "$EMAIL" \
  --agree-tos --no-eff-email

# Recharger nginx avec SSL
$COMPOSE exec nginx nginx -s reload

echo "Certificat obtenu. Lance maintenant : $COMPOSE up -d"
