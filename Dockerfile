FROM python:3.7-slim

ENV tech-mavericks /app

WORKDIR tech-mavericks

COPY . ./

RUN \  
    apt-get update && \
    apt-get -y install libpq-dev gcc && \
    pip install --upgrade pip && \
    pip install --upgrade -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app
