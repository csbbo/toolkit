docker-compose -f docker-compose.yml down
docker build -t forrich_server .
docker-compose -f docker-compose.yml up -d
