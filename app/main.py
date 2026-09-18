# Import FastAPI, the framework used to create the website's backend API.
from fastapi import FastAPI

# Import BaseModel, which validates the vehicle information users submit.
from pydantic import BaseModel


# Create the DealerOps Cloud application.
# This information will appear on the automatic API documentation page.
app = FastAPI(
    title="DealerOps Cloud",
    description="Cloud-based dealership inventory management system",
    version="0.1.0",
)


# Create a Vehicle model.
# This defines the information required for each vehicle in the system.
class Vehicle(BaseModel):
    # A unique identification number for the vehicle record.
    id: int

    # The model year of the vehicle, such as 2024.
    year: int

    # The vehicle manufacturer, such as Toyota or Jeep.
    make: str

    # The vehicle model, such as Corolla or Wrangler.
    model: str

    # The advertised selling price of the vehicle.
    price: float

    # The vehicle's current inventory status.
    # If no status is provided, it will automatically be "available."
    status: str = "available"


# This temporary list acts like a small database.
# Vehicles created through the API will be stored here while the app is running.
# The information will disappear whenever the application restarts.
# We will replace this list with a PostgreSQL database later.
vehicles: list[Vehicle] = []


# The @app.get("/") line creates the application's main URL.
# When someone visits the home address, this function returns basic app details.
@app.get("/")
def home():
    return {
        "application": "DealerOps Cloud",
        "version": "0.1.0",
        "status": "running",
    }


# This creates a health-check endpoint.
# AWS and monitoring systems can use it to confirm the application is running.
@app.get("/health")
def health():
    return {"status": "healthy"}


# This creates an endpoint that returns every vehicle in inventory.
# A GET request reads information without changing it.
@app.get("/vehicles")
def get_vehicles():
    return vehicles


# This creates an endpoint for adding a vehicle.
# A POST request sends new information to the application.
# The 201 status code means that a new record was created successfully.
@app.post("/vehicles", status_code=201)
def create_vehicle(vehicle: Vehicle):
    # Add the validated vehicle to the temporary inventory list.
    vehicles.append(vehicle)

    # Return the new vehicle so the user can confirm what was saved.
    return vehicle
