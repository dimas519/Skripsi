FROM python:3.9

WORKDIR /app

COPY Program /app


RUN pip install uvicorn==0.20.0 fastapi==0.87.0 mysql-connector-python==8.0.29

CMD [ "python", "/app/Main.py" ]