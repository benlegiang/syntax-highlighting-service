#! /bin/bash
git clone https://github.com/benlegiang/syntax-highlighting-service.git
cd syntax-highlighting-service/
docker compose build
docker compose push
docker compose down
docker compose up
