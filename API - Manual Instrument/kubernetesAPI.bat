@REM docker container stop testing_otel

@REM docker container rm testing_otel

@REM docker image rm dimas519/skripsi-api:otel_instumentation


kubectl port-forward db-mysql-myadmin-0  30009:80

docker build --tag dimas519/skripsi-api:otel_instumentation . -f .docker/Dockerfile

docker build --tag ghcr.io/dimas519/skripsi-api:otel_instumentation . -f .docker/Dockerfile

docker push dimas519/skripsi-api:otel_instumentation

docker push ghcr.io/dimas519/skripsi-api:otel_instumentation


kubectl apply -f ./.docker/apiService.yaml


@REM kubectl rollout restart deployment deployment-api -n testing-api



@REM docker container create --name testing_otel --network skripsi_network -p  50

@REM docker container start testing_otel
