#! /bin/bash
docker compose build
docker compose push
docker compose down
docker network prune
docker compose up -d
