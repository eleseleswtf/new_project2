####################
# STRUCTURAL MODEL #
####################

from besser.BUML.metamodel.structural import (
    Class, Property, Method, Parameter,
    BinaryAssociation, Generalization, DomainModel,
    Enumeration, EnumerationLiteral, Multiplicity,
    StringType, IntegerType, FloatType, BooleanType,
    TimeType, DateType, DateTimeType, TimeDeltaType,
    AnyType, Constraint, AssociationClass, Metadata, MethodImplementationType
)

# Classes
ParkingPlace = Class(name="ParkingPlace")
ParkingAvailability = Class(name="ParkingAvailability")

# ParkingPlace class attributes and methods
ParkingPlace_placeId: Property = Property(name="placeId", type=StringType, visibility="private")
ParkingPlace_isFree: Property = Property(name="isFree", type=BooleanType, visibility="private", default_value="true")
ParkingPlace_lastUpdated: Property = Property(name="lastUpdated", type=DateType, visibility="private")
ParkingPlace_locationDescription: Property = Property(name="locationDescription", type=StringType, visibility="private", is_optional=True)
ParkingPlace_m_updateAvailability: Method = Method(name="updateAvailability", parameters={Parameter(name='freeStatus', type=BooleanType)}, implementation_type=MethodImplementationType.NONE)
ParkingPlace.attributes={ParkingPlace_isFree, ParkingPlace_lastUpdated, ParkingPlace_locationDescription, ParkingPlace_placeId}
ParkingPlace.methods={ParkingPlace_m_updateAvailability}

# ParkingAvailability class attributes and methods
ParkingAvailability_availabilityId: Property = Property(name="availabilityId", type=StringType, visibility="private")
ParkingAvailability_checkedAt: Property = Property(name="checkedAt", type=DateType, visibility="private")
ParkingAvailability_anyPlaceFree: Property = Property(name="anyPlaceFree", type=BooleanType, visibility="private", is_derived=True)
ParkingAvailability_bothPlacesFree: Property = Property(name="bothPlacesFree", type=BooleanType, visibility="private", is_derived=True)
ParkingAvailability_m_refreshAvailabilityStatus: Method = Method(name="refreshAvailabilityStatus", parameters={}, implementation_type=MethodImplementationType.NONE)
ParkingAvailability.attributes={ParkingAvailability_anyPlaceFree, ParkingAvailability_availabilityId, ParkingAvailability_bothPlacesFree, ParkingAvailability_checkedAt}
ParkingAvailability.methods={ParkingAvailability_m_refreshAvailabilityStatus}

# Relationships
hasPlaces: BinaryAssociation = BinaryAssociation(
    name="hasPlaces",
    ends={
        Property(name="parkingavailability", type=ParkingAvailability, multiplicity=Multiplicity(1, 1)),
        Property(name="hasPlaces", type=ParkingPlace, multiplicity=Multiplicity(2, 2))
    }
)

# Domain Model
domain_model = DomainModel(
    name="Class_Diagram",
    types={ParkingPlace, ParkingAvailability},
    associations={hasPlaces},
    generalizations={},
    metadata=None
)
