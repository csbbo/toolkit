docker-compose -f docker-compose.yml down
docker build -t toolkit .
docker-compose -f docker-compose.yml up -d
