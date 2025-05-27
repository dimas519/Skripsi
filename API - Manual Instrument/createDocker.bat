docker container stop testing_otel

docker container rm testing_otel

docker image rm dimas519/skripsi-api:otel_instumentation




docker build --tag dimas519/skripsi_api:otel_instrumentation . -f .docker/Dockerfile

docker push dimas519/skripsi_api:otel_instrumentation

docker build --tag ghcr.io/dimas519/skripsi_api:otel_instrumentation . -f .docker/Dockerfile

docker push ghcr.io/dimas519/skripsi_api:otel_instrumentation




docker container create --name testing_otel --network skripsi_network -p  5000:5000 dimas519/skripsi-api:otel_instumentation

docker container start testing_otel
