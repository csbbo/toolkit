docker-compose -f docker-compose.yml down
docker build -t tool_openresty ./openresty
docker build -t tool_server .
docker-compose -f docker-compose.yml up -d
