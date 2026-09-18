"""Database models for the DealerOps application."""

from sqlalchemy import Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Vehicle(Base):
    """Represent a vehicle stored in the dealership inventory database."""

    # Name of the database table.
    __tablename__ = "vehicles"

    # Automatically generated unique identification number.
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    # Vehicle manufacturer, such as Toyota or Honda.
    make: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Vehicle model, such as Corolla or Civic.
    model: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Model year of the vehicle.
    year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Vehicle identification number.
    # unique=True prevents two vehicles from having the same VIN.
    vin: Mapped[str] = mapped_column(
        String(17),
        unique=True,
        nullable=False,
        index=True,
    )

    # Current advertised price.
    price: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    # Inventory status, such as available, reserved or sold.
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="available",
    )
