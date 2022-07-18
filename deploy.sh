#! /bin/bash
docker compose build
docker compose push
docker compose down
docker compose up -d
