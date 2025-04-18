# Use the official Python image from the Docker Hub
FROM python:3.13

# Set the working directory in the container
WORKDIR /application

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the FastAPI application code into the container
COPY ./app ./app

EXPOSE 8000

# Command to run the FastAPI application using Python config file
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "--config", "app/core/gunicorn_config.py", "app.main:app"]
