FROM python:3.7-slim

ENV tech_mavericks /app

WORKDIR $tech_mavericks

ENV PYTHONPATH "${PYTHONPATH}:/app/app"

COPY . .

RUN apt-get update && \
    apt-get -y install gunicorn uvicorn && \
    apt-get -y install libpq-dev gcc && \
    pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8080

CMD exec gunicorn --bind 0.0.0.0:8080 --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 app.main:app
