# Real time ingestion

Project to check how FastAPI can handle real-time data ingestion and serve through a REST API.

## Features

Customers interactions will be sent to a multiple backends in the ingestion service. PostgresSQL will be store the data, and Redis will be used to store the last viewed product information.
Another service that depend on Redis will retrieve a list of last product viewed by the customers let the platform can personalize the product recommendations.

<img src="media/diagram.png" alt="Diagram" style="display:block;margin-left:auto;margin-right:auto;">

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
uvicorn app.main:app --reload
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
