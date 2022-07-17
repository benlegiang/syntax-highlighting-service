#! /bin/bash
docker stop syntax-highlighting-service-rest-api
docker rm syntax-highlighting-service-rest-api
docker rmi benlegiang/syntax-highlighting-service-rest-api:master
docker pull benlegiang/syntax-highlighting-service-rest-api:master

docker run -t -d -p syntax-highlighting-service-rest-api benlegiang/syntax-highlighting-service-rest-api:master
