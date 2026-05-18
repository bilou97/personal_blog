#!/bin/bash
set -e

if [ ! -f .env ]; then
  cp .env.example .env
  echo ".env créé depuis .env.example — pense à renseigner les secrets."
fi

docker compose up --build
