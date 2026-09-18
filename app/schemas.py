"""Data-validation schemas for the DealerOps API."""

from pydantic import BaseModel, ConfigDict, Field


class VehicleCreate(BaseModel):
    """Validate information submitted when a vehicle is created."""

    make: str = Field(min_length=1, max_length=50)
    model: str = Field(min_length=1, max_length=50)
    year: int = Field(ge=1900, le=2100)
    vin: str = Field(min_length=17, max_length=17)
    price: float = Field(gt=0)
    status: str = Field(default="available", max_length=20)


class VehicleResponse(VehicleCreate):
    """Define the vehicle information returned by the API."""

    # Every saved vehicle receives an automatically generated ID.
    id: int

    # Allow Pydantic to create responses from SQLAlchemy database records.
    model_config = ConfigDict(from_attributes=True)
