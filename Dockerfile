# Use a lightweight official Python 3.12 image as the starting environment.
FROM python:3.12-slim

# Create /app inside the container and make it the working directory.
WORKDIR /app

# Copy the dependency file first.
# This lets Docker reuse installed dependencies when only application code changes.
COPY requirements.txt .

# Install the Python packages required by the application.
# --no-cache-dir keeps the final container image smaller.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application's Python package into the container.
COPY app ./app

# Document that the FastAPI application listens on port 8000.
EXPOSE 8000

# Start the application using the Uvicorn web server.
# 0.0.0.0 allows traffic to reach the application from outside the container.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
