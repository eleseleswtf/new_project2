import enum
from typing import List as List_, Optional as Optional_
from sqlalchemy import (
    create_engine, Column as Column_, ForeignKey as ForeignKey_, Table as Table_, 
    Text as Text_, Boolean as Boolean_, String as String_, Date as Date_, 
    Time as Time_, DateTime as DateTime_, Float as Float_, Integer as Integer_, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped as Mapped_, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass



# Tables definition for many-to-many relationships

# Tables definition
class ParkingAvailability(Base):
    __tablename__ = "parkingavailability"
    id: Mapped_[int] = mapped_column(primary_key=True)
    availabilityId: Mapped_[str] = mapped_column(String_(100))
    checkedAt: Mapped_[dt_date] = mapped_column(Date_)
    anyPlaceFree: Mapped_[bool] = mapped_column(Boolean_)
    bothPlacesFree: Mapped_[bool] = mapped_column(Boolean_)

class ParkingPlace(Base):
    __tablename__ = "parkingplace"
    id: Mapped_[int] = mapped_column(primary_key=True)
    placeId: Mapped_[str] = mapped_column(String_(100))
    isFree: Mapped_[bool] = mapped_column(Boolean_, default=True)
    lastUpdated: Mapped_[dt_date] = mapped_column(Date_)
    locationDescription: Mapped_[Optional_[str]] = mapped_column(String_(100), nullable=True)
    parkingavailability_id: Mapped_[int] = mapped_column(ForeignKey_("parkingavailability.id"))


#--- Relationships of the parkingavailability table
ParkingAvailability.hasPlaces: Mapped_[List_["ParkingPlace"]] = relationship("ParkingPlace", back_populates="parkingavailability", foreign_keys=[ParkingPlace.parkingavailability_id])

#--- Relationships of the parkingplace table
ParkingPlace.parkingavailability: Mapped_["ParkingAvailability"] = relationship("ParkingAvailability", back_populates="hasPlaces", foreign_keys=[ParkingPlace.parkingavailability_id])

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)