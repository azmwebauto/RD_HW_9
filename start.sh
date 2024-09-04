docker-compose -f ./web_app/docker-compose.yaml --env-file=./web_app/.env up --build -d
docker-compose -f ./scraper/docker-compose.yaml --env-file=./scraper/.env up --build -d