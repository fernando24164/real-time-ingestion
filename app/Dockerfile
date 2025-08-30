FROM python:3.13-slim

WORKDIR /application

COPY requirements.txt ./app/ ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--config", "app/core/gunicorn_config.py", "app.main:app"]
