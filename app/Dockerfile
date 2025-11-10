FROM python:3.13-slim


RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && ln -s /root/.local/bin/uv /usr/local/bin/uv

ENV UV_COMPILE_BYTECODE=1

WORKDIR /application

COPY pyproject.toml uv.lock ./app/ ./
RUN uv sync --locked --no-dev

COPY ./app ./app

EXPOSE 8000

CMD ["uv", "run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--config", "app/core/gunicorn_config.py", "app.main:app"]
