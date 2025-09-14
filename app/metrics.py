import time
from collections.abc import Callable
from functools import wraps
from typing import Any

from fastapi import FastAPI, Request, Response
from loguru import logger
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    Summary,
    generate_latest,
    start_http_server,
)
from starlette.middleware.base import BaseHTTPMiddleware

# Create HTTP request metrics
REQUEST_COUNT = Counter(
    "app_requests_total",
    "Total number of requests",
    ["method", "endpoint", "status"],
)

ACTIVE_REQUESTS = Gauge("app_active_requests", "Current number of active requests")

REQUEST_DURATION = Histogram(
    "app_request_duration_seconds",
    "Request duration in seconds",
    ["method", "endpoint"],
    buckets=[0.1, 0.3, 0.5, 0.7, 1, 3, 5, 7, 10],
)

REQUEST_SIZE = Summary(
    "app_request_size_bytes",
    "Request size in bytes",
    ["method", "endpoint"],
)

# Application-specific metrics
DB_QUERY_DURATION = Histogram(
    "app_db_query_duration_seconds",
    "Database query duration in seconds",
    ["query_type", "table"],
    buckets=[0.01, 0.05, 0.1, 0.5, 1.0, 2.0, 5.0],
)

CACHE_HIT_COUNTER = Counter(
    "app_cache_hits_total",
    "Total number of cache hits",
    ["cache_name"],
)

CACHE_MISS_COUNTER = Counter(
    "app_cache_misses_total",
    "Total number of cache misses",
    ["cache_name"],
)


def start_metrics_server(port: int = 8001) -> None:
    start_http_server(port)
    logger.info(f"Prometheus metrics available at http://localhost:{port}/metrics")


class PrometheusMiddleware(BaseHTTPMiddleware):
    """
    FastAPI middleware for collecting Prometheus metrics
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Track request count and duration
        method = request.method
        path = request.url.path

        # Exclude metrics endpoint itself from metrics
        if path == "/metrics":
            return await call_next(request)

        ACTIVE_REQUESTS.inc()
        start_time = time.time()

        try:
            response = await call_next(request)
            status = response.status_code
            REQUEST_SIZE.labels(method=method, endpoint=path).observe(
                int(response.headers.get("content-length", 0)),
            )
            return response
        except Exception as e:
            status = 500
            raise e
        finally:
            duration = time.time() - start_time
            REQUEST_DURATION.labels(method=method, endpoint=path).observe(duration)
            REQUEST_COUNT.labels(method=method, endpoint=path, status=status).inc()
            ACTIVE_REQUESTS.dec()


def track_request_duration(method: str, endpoint: str) -> Callable:
    """Legacy decorator to measure request duration (non-async)"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            ACTIVE_REQUESTS.inc()
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                status = "success"
                return result
            except Exception as e:
                status = "error"
                raise e
            finally:
                duration = time.time() - start_time
                REQUEST_DURATION.labels(method=method, endpoint=endpoint).observe(
                    duration,
                )
                REQUEST_COUNT.labels(
                    method=method,
                    endpoint=endpoint,
                    status=status,
                ).inc()
                ACTIVE_REQUESTS.dec()

        return wrapper

    return decorator


def track_db_query_duration(query_type: str, table: str) -> Callable:
    """Decorator to track database query duration"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.time()
            try:
                return await func(*args, **kwargs)
            finally:
                duration = time.time() - start_time
                DB_QUERY_DURATION.labels(query_type=query_type, table=table).observe(
                    duration,
                )

        return wrapper

    return decorator


def track_cache(cache_name: str) -> Callable:
    """Decorator to track cache hits and misses"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = await func(*args, **kwargs)
            if result is None:
                CACHE_MISS_COUNTER.labels(cache_name=cache_name).inc()
            else:
                CACHE_HIT_COUNTER.labels(cache_name=cache_name).inc()
            return result

        return wrapper

    return decorator


def setup_metrics(
    app: FastAPI,
    metrics_endpoint: bool = True,
    metrics_port: int | None = None,
) -> FastAPI:
    """
    Setup Prometheus metrics collection for a FastAPI app

    Args:
        app: FastAPI application
        metrics_endpoint: Whether to add a /metrics endpoint to the app
        metrics_port: If provided, starts a separate metrics server on this port
    """
    # Add middleware for tracking requests
    app.add_middleware(PrometheusMiddleware)

    if metrics_endpoint:

        @app.get("/metrics")
        def metrics() -> Response:
            return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)

    if metrics_port:
        start_metrics_server(metrics_port)

    return app
