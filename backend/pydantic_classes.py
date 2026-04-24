from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

############################################
# Classes are defined here
############################################
class ParkingAvailabilityCreate(BaseModel):
    anyPlaceFree: bool
    checkedAt: date
    bothPlacesFree: bool
    availabilityId: str
    hasPlaces: Optional[List[int]] = None  # 1:N Relationship


class ParkingPlaceCreate(BaseModel):
    placeId: str
    lastUpdated: date
    isFree: bool = true
    locationDescription: Optional[str] = None
    parkingavailability: int  # N:1 Relationship (mandatory)


