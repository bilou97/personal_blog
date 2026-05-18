#!/bin/bash
set -e

docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
echo "Conteneurs démarrés. Pour créer un superuser admin :"
echo "  docker compose exec backend python manage.py createsuperuser"
