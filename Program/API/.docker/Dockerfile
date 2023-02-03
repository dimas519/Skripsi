FROM python:3.9

WORKDIR /app

COPY Program /app

RUN  python -m pip install mysql-connector-python==8.0.29 uvicorn==0.20.0 fastapi==0.87.0

CMD [ "python", "/app/Main.py" ]