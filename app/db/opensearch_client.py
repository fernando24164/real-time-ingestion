from opensearchpy._async.client import AsyncOpenSearch

from app.core.config import Settings, get_settings


def connect_opensearch(
    settings: Settings = get_settings(),
) -> AsyncOpenSearch:
    try:
        return AsyncOpenSearch(
            hosts=settings.OPENSEARCH_CONFIG["host"],
            port=settings.OPENSEARCH_CONFIG["port"],
            http_auth=(settings.OPENSEARCH_CONFIG["username"], settings.OPENSEARCH_CONFIG["password"]),
            use_ssl=False,
            verify_certs=False,
            connection_class=AsyncOpenSearch,
        )
    except Exception as e:
        raise ConnectionError(f"Failed to connect to OpenSearch: {e}")
