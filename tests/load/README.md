# Load Testing with Locust

This directory contains load tests for the Customer Insights API using Locust.

## Running the Tests

1. Make sure your FastAPI application is running:
```bash
uvicorn app.main:app --reload
```
or with the docker compose file


2. Start Locust (from the project root):
```bash
locust -f tests/load/locustfile.py --config tests/load/locust.conf
```

3. Open the Locust web interface:
   - Visit http://localhost:8089
   - Enter the number of users to simulate
   - Enter the spawn rate (users per second)
   - Click "Start swarming"

## Configuration

- Default settings in `locust.conf`:
  - Host: http://localhost:8000
  - Web UI Port: 8089
  - Default Users: 10
  - Default Spawn Rate: 1
  - Default Run Time: 1 minute

## Test Scenarios

The load test simulates users requesting customer insights for the three test users from the seed data:
- User 1: retrogamer
- User 2: collector
- User 3: casual_player

## Metrics Collected

- Response time (min, max, average)
- Requests per second
- Failure rate
- Number of users