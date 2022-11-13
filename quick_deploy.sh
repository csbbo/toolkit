docker-compose -f docker-compose.yml down
docker build -t tk_openresty ./openresty
docker build -t tk_server .
docker-compose -f docker-compose.yml up -d
