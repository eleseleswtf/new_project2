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
class GarageCreate(BaseModel):
    availabilityId: str
    anyPlaceFree: bool
    bothPlacesFree: bool
    checkedAt: date
    parkingplace: Optional[List[int]] = None  # 1:N Relationship


class ParkingPlaceCreate(BaseModel):
    isFree: bool
    lastUpdated: date
    placeId: str
    locationDescription: Optional[str] = None
    hasPlaces: int  # N:1 Relationship (mandatory)


