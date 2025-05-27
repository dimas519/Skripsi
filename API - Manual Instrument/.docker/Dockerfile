FROM  python:3.9-slim-bullseye

WORKDIR /app


COPY Program /app

RUN  python -m pip install mysql-connector-python==8.0.29 uvicorn==0.20.0 fastapi==0.87.0 bcrypt==3.2.0 numpy==1.21.4 opentelemetry-api==1.31.1 opentelemetry-sdk==1.31.1 opentelemetry-exporter-otlp-proto-http==1.31.1


CMD [ "python","/app/Main.py"]