"""Main FastAPI application for the DealerOps inventory platform."""

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models
from app.database import engine, get_database
from app.schemas import VehicleCreate, VehicleResponse


# Create database tables that do not already exist.
# SQLAlchemy uses the models in models.py to determine the table structure.
models.Base.metadata.create_all(bind=engine)


# Create the FastAPI application.
app = FastAPI(
    title="DealerOps Cloud API",
    description="API for managing dealership vehicle inventory.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    """Return basic information confirming that the API is running."""

    return {
        "application": "DealerOps Cloud API",
        "status": "running",
    }


@app.get("/health")
def health_check():
    """Provide a health-check endpoint for Docker, AWS and monitoring tools."""

    return {
        "status": "healthy",
    }


@app.get(
    "/vehicles",
    response_model=list[VehicleResponse],
)
def get_vehicles(
    database: Session = Depends(get_database),
):
    """Retrieve all vehicles currently stored in the database."""

    return database.query(models.Vehicle).all()


@app.post(
    "/vehicles",
    response_model=VehicleResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vehicle(
    vehicle: VehicleCreate,
    database: Session = Depends(get_database),
):
    """Validate and save a new vehicle in the inventory database."""

    # Convert the validated API information into a database record.
    database_vehicle = models.Vehicle(**vehicle.model_dump())

    # Prepare the record to be saved.
    database.add(database_vehicle)

    try:
        # Permanently save the vehicle.
        database.commit()

        # Reload the record so its generated ID is available.
        database.refresh(database_vehicle)

    except IntegrityError:
        # Undo the failed transaction if the VIN already exists.
        database.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A vehicle with this VIN already exists.",
        )

    return database_vehicle
