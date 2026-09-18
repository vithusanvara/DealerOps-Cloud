# Import TestClient so we can send test requests to the application
# without starting a real web server.
from fastapi.testclient import TestClient

# Import the DealerOps FastAPI application from app/main.py.
from app.main import app


# Create a test client connected to the DealerOps application.
client = TestClient(app)


# Test that the application's health-check endpoint is working.
def test_health_check():
    # Send a GET request to the /health endpoint.
    response = client.get("/health")

    # Confirm that the application responds successfully.
    assert response.status_code == 200

    # Confirm that the response contains the expected health message.
    assert response.json() == {"status": "healthy"}


# Test that a dealership employee can add a vehicle.
def test_create_vehicle():
    # Create sample vehicle information to send to the application.
    vehicle = {
        "id": 1,
        "year": 2024,
        "make": "Toyota",
        "model": "Corolla",
        "price": 29995.00,
        "status": "available",
    }

    # Send the sample vehicle to the POST /vehicles endpoint.
    response = client.post("/vehicles", json=vehicle)

    # Confirm that the vehicle was created successfully.
    # HTTP status code 201 means "Created."
    assert response.status_code == 201

    # Confirm that the returned vehicle information is correct.
    assert response.json()["id"] == 1
    assert response.json()["make"] == "Toyota"
    assert response.json()["model"] == "Corolla"
    assert response.json()["status"] == "available"


# Test that the application can return its current vehicle inventory.
def test_get_vehicles():
    # Send a GET request to retrieve all stored vehicles.
    response = client.get("/vehicles")

    # Confirm that the request was successful.
    assert response.status_code == 200

    # Confirm that the response is a list.
    assert isinstance(response.json(), list)
