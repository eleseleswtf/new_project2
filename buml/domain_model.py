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
Garage = Class(name="Garage")

# ParkingPlace class attributes and methods
ParkingPlace_placeId: Property = Property(name="placeId", type=StringType, visibility="private")
ParkingPlace_isFree: Property = Property(name="isFree", type=BooleanType, visibility="private")
ParkingPlace_lastUpdated: Property = Property(name="lastUpdated", type=DateType, visibility="private")
ParkingPlace_locationDescription: Property = Property(name="locationDescription", type=StringType, visibility="private", is_optional=True)
ParkingPlace_m_updateAvailability: Method = Method(name="updateAvailability", parameters={Parameter(name='freeStatus', type=BooleanType)}, implementation_type=MethodImplementationType.NONE)
ParkingPlace.attributes={ParkingPlace_isFree, ParkingPlace_lastUpdated, ParkingPlace_locationDescription, ParkingPlace_placeId}
ParkingPlace.methods={ParkingPlace_m_updateAvailability}

# Garage class attributes and methods
Garage_availabilityId: Property = Property(name="availabilityId", type=StringType, visibility="private")
Garage_checkedAt: Property = Property(name="checkedAt", type=DateType, visibility="private")
Garage_anyPlaceFree: Property = Property(name="anyPlaceFree", type=BooleanType, visibility="private", is_derived=True)
Garage_bothPlacesFree: Property = Property(name="bothPlacesFree", type=BooleanType, visibility="private", is_derived=True)
Garage_m_refreshAvailabilityStatus: Method = Method(name="refreshAvailabilityStatus", parameters={}, implementation_type=MethodImplementationType.NONE)
Garage.attributes={Garage_anyPlaceFree, Garage_availabilityId, Garage_bothPlacesFree, Garage_checkedAt}
Garage.methods={Garage_m_refreshAvailabilityStatus}

# Relationships
hasPlaces: BinaryAssociation = BinaryAssociation(
    name="hasPlaces",
    ends={
        Property(name="parkingplace", type=ParkingPlace, multiplicity=Multiplicity(2, 2)),
        Property(name="hasPlaces", type=Garage, multiplicity=Multiplicity(1, 1))
    }
)

# Domain Model
domain_model = DomainModel(
    name="Class_Diagram",
    types={ParkingPlace, Garage},
    associations={hasPlaces},
    generalizations={},
    metadata=None
)
