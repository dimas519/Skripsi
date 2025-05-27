docker network create skripsi_network

docker-compose -f .docker/docker-compose.yml up -d

docker network connect skripsi_network skripsi-db

docker network connect skripsi_network skripsi-phpmyadmin

@REM #sleep untuk memastikan mysql sudah start
timeout 30 >null 

docker exec -i skripsi-db mysql -uroot -proot --database="skripsi" < "Template/databaseCreate.sql"

docker build --tag dimas519/skripsi-api:otel_instumentation . -f .docker/Dockerfile

docker container create --name testing_otel --network skripsi_network -p  5000:5000 dimas519/skripsi-api:otel_instumentation

docker container start testing_otel
