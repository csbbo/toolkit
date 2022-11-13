docker-compose -f docker-compose.yml down
docker build -t tk_server .
docker build -t tk_nginx nginx
docker-compose -f docker-compose.yml up -d
