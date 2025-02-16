import json
from pathlib import Path

import httpx


def create_index(index_name: str, host: str = "http://localhost:9200"):
    """
    Creates an index in OpenSearch with the specified settings and mappings.

    Args:
        index_name (str): The name of the index to create.
        host (str, optional): The OpenSearch host. Defaults to "http://localhost:9200".

    Returns:
        dict: The JSON response from OpenSearch.
    """
    url = f"{host}/{index_name}"
    path = Path.cwd() / "app" / "models" / "ingestion_mapping.json"
    with path.open("r") as file:
        payload = json.load(file)
    headers = {"Content-Type": "application/json"}
    try:
        response = httpx.put(url, headers=headers, data=payload)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error: {e}")
        return None
    except httpx.RequestError as e:
        print(f"Request error: {e}")
        return None


if __name__ == "__main__":
    index_name = "ingestion"

    result = create_index(index_name)

    if result:
        print(json.dumps(result, indent=2))
