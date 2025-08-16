FROM python:3.13.7-alpine

WORKDIR /application

COPY requirements.txt ./app/ ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--config", "app/core/gunicorn_config.py", "app.main:app"]
