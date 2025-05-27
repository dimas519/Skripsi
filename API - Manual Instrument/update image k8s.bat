@REM docker container stop testing_otel

@REM docker container rm testing_otel

@REM docker image rm dimas519/skripsi-api:otel_instumentation



docker build --tag skripsi_api:otel_instumentation . -f .docker/Dockerfile

@REM docker push skripsi_api:otel_instumentation

kubectl delete -f ./.docker/apiService.yaml

kubectl apply -f ./.docker/apiService.yaml


@REM kubectl rollout restart deployment deployment-api -n testing-api



@REM docker container create --name testing_otel --network skripsi_network -p  50

@REM docker container start testing_otel
