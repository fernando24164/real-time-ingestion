# Real time ingestion

Project to check how FastAPI can handle real-time data ingestion and serve through a REST API.

## How to install

1. Install Dependencies:
    Ensure you have Python 3.9+ installed. Then, install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage Examples
Launch docker-compose

```bash
docker-compose up -d
```

Run REST API in localhost:

```bash
uvicorn main:app.main:app --reload
```

The swagger UI can be accessed at `http://127.0.0.1:8000/docs`.

## Testing Instructions
To run the tests, use the following command:

```bash
pytest tests/
```
The test suite includes unit tests for the Athena client, S3 client, and PostgreSQL exporter. Mocking is used extensively to avoid dependencies on external services.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
