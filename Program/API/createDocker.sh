docker network create skripsi_network

docker container create --name api-db-1 --network skripsi_network -p  9926:3306 mysql:8.0

docker container create --name api-phpmyadmin-1 --network skripsi_network -p  9927:80 phpmyadmin/phpmyadmin:5.1.3



docker container rm apimain

docker image rm main-api:1.0.0

docker build --tag main-api:1.0.0 . -f .docker/Dockerfile 

docker container create --name apimain --network skripsi_network -p  5000:5000 main-api:1.0.0

docker container start apimain