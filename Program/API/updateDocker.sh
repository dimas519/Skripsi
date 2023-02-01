docker container rm apimain

docker image rm main-api:1.0.0

docker build --tag main-api:1.0.0 . -f .docker/Dockerfile 

docker container create --name apimain --network skripsi_network -p  5000:5000 main-api:1.0.0

docker container start apimain