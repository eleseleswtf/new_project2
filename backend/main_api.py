import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "Garage", "description": "Operations for Garage entities"},
        {"name": "Garage Relationships", "description": "Manage Garage relationships"},
        {"name": "Garage Methods", "description": "Execute Garage methods"},
        {"name": "ParkingPlace", "description": "Operations for ParkingPlace entities"},
        {"name": "ParkingPlace Relationships", "description": "Manage ParkingPlace relationships"},
        {"name": "ParkingPlace Methods", "description": "Execute ParkingPlace methods"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["garage_count"] = database.query(Garage).count()
    stats["parkingplace_count"] = database.query(ParkingPlace).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   Garage functions
#
############################################

@app.get("/garage/", response_model=None, tags=["Garage"])
def get_all_garage(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Garage)
        garage_list = query.all()

        # Serialize with relationships included
        result = []
        for garage_item in garage_list:
            item_dict = garage_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            parkingplace_list = database.query(ParkingPlace).filter(ParkingPlace.hasPlaces_id == garage_item.id).all()
            item_dict['parkingplace'] = []
            for parkingplace_obj in parkingplace_list:
                parkingplace_dict = parkingplace_obj.__dict__.copy()
                parkingplace_dict.pop('_sa_instance_state', None)
                item_dict['parkingplace'].append(parkingplace_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Garage).all()


@app.get("/garage/count/", response_model=None, tags=["Garage"])
def get_count_garage(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Garage entities"""
    count = database.query(Garage).count()
    return {"count": count}


@app.get("/garage/paginated/", response_model=None, tags=["Garage"])
def get_paginated_garage(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Garage entities"""
    total = database.query(Garage).count()
    garage_list = database.query(Garage).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": garage_list
        }

    result = []
    for garage_item in garage_list:
        parkingplace_ids = database.query(ParkingPlace.id).filter(ParkingPlace.hasPlaces_id == garage_item.id).all()
        item_data = {
            "garage": garage_item,
            "parkingplace_ids": [x[0] for x in parkingplace_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/garage/search/", response_model=None, tags=["Garage"])
def search_garage(
    database: Session = Depends(get_db)
) -> list:
    """Search Garage entities by attributes"""
    query = database.query(Garage)


    results = query.all()
    return results


@app.get("/garage/{garage_id}/", response_model=None, tags=["Garage"])
async def get_garage(garage_id: int, database: Session = Depends(get_db)) -> Garage:
    db_garage = database.query(Garage).filter(Garage.id == garage_id).first()
    if db_garage is None:
        raise HTTPException(status_code=404, detail="Garage not found")

    parkingplace_ids = database.query(ParkingPlace.id).filter(ParkingPlace.hasPlaces_id == db_garage.id).all()
    response_data = {
        "garage": db_garage,
        "parkingplace_ids": [x[0] for x in parkingplace_ids]}
    return response_data



@app.post("/garage/", response_model=None, tags=["Garage"])
async def create_garage(garage_data: GarageCreate, database: Session = Depends(get_db)) -> Garage:


    db_garage = Garage(
        availabilityId=garage_data.availabilityId,        anyPlaceFree=garage_data.anyPlaceFree,        bothPlacesFree=garage_data.bothPlacesFree,        checkedAt=garage_data.checkedAt        )

    database.add(db_garage)
    database.commit()
    database.refresh(db_garage)

    if garage_data.parkingplace:
        # Validate that all ParkingPlace IDs exist
        for parkingplace_id in garage_data.parkingplace:
            db_parkingplace = database.query(ParkingPlace).filter(ParkingPlace.id == parkingplace_id).first()
            if not db_parkingplace:
                raise HTTPException(status_code=400, detail=f"ParkingPlace with id {parkingplace_id} not found")

        # Update the related entities with the new foreign key
        database.query(ParkingPlace).filter(ParkingPlace.id.in_(garage_data.parkingplace)).update(
            {ParkingPlace.hasPlaces_id: db_garage.id}, synchronize_session=False
        )
        database.commit()



    parkingplace_ids = database.query(ParkingPlace.id).filter(ParkingPlace.hasPlaces_id == db_garage.id).all()
    response_data = {
        "garage": db_garage,
        "parkingplace_ids": [x[0] for x in parkingplace_ids]    }
    return response_data


@app.post("/garage/bulk/", response_model=None, tags=["Garage"])
async def bulk_create_garage(items: list[GarageCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Garage entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_garage = Garage(
                availabilityId=item_data.availabilityId,                anyPlaceFree=item_data.anyPlaceFree,                bothPlacesFree=item_data.bothPlacesFree,                checkedAt=item_data.checkedAt            )
            database.add(db_garage)
            database.flush()  # Get ID without committing
            created_items.append(db_garage.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Garage entities"
    }


@app.delete("/garage/bulk/", response_model=None, tags=["Garage"])
async def bulk_delete_garage(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Garage entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_garage = database.query(Garage).filter(Garage.id == item_id).first()
        if db_garage:
            database.delete(db_garage)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Garage entities"
    }

@app.put("/garage/{garage_id}/", response_model=None, tags=["Garage"])
async def update_garage(garage_id: int, garage_data: GarageCreate, database: Session = Depends(get_db)) -> Garage:
    db_garage = database.query(Garage).filter(Garage.id == garage_id).first()
    if db_garage is None:
        raise HTTPException(status_code=404, detail="Garage not found")

    setattr(db_garage, 'availabilityId', garage_data.availabilityId)
    setattr(db_garage, 'anyPlaceFree', garage_data.anyPlaceFree)
    setattr(db_garage, 'bothPlacesFree', garage_data.bothPlacesFree)
    setattr(db_garage, 'checkedAt', garage_data.checkedAt)
    if garage_data.parkingplace is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(ParkingPlace).filter(ParkingPlace.hasPlaces_id == db_garage.id).update(
            {ParkingPlace.hasPlaces_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if garage_data.parkingplace:
            # Validate that all IDs exist
            for parkingplace_id in garage_data.parkingplace:
                db_parkingplace = database.query(ParkingPlace).filter(ParkingPlace.id == parkingplace_id).first()
                if not db_parkingplace:
                    raise HTTPException(status_code=400, detail=f"ParkingPlace with id {parkingplace_id} not found")

            # Update the related entities with the new foreign key
            database.query(ParkingPlace).filter(ParkingPlace.id.in_(garage_data.parkingplace)).update(
                {ParkingPlace.hasPlaces_id: db_garage.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_garage)

    parkingplace_ids = database.query(ParkingPlace.id).filter(ParkingPlace.hasPlaces_id == db_garage.id).all()
    response_data = {
        "garage": db_garage,
        "parkingplace_ids": [x[0] for x in parkingplace_ids]    }
    return response_data


@app.delete("/garage/{garage_id}/", response_model=None, tags=["Garage"])
async def delete_garage(garage_id: int, database: Session = Depends(get_db)):
    db_garage = database.query(Garage).filter(Garage.id == garage_id).first()
    if db_garage is None:
        raise HTTPException(status_code=404, detail="Garage not found")
    database.delete(db_garage)
    database.commit()
    return db_garage


@app.get("/garage/{garage_id}/parkingplace/", response_model=None, tags=["Garage Relationships"])
async def get_parkingplace_of_garage(garage_id: int, database: Session = Depends(get_db)):
    """Get all ParkingPlace entities related to this Garage through parkingplace"""
    db_garage = database.query(Garage).filter(Garage.id == garage_id).first()
    if db_garage is None:
        raise HTTPException(status_code=404, detail="Garage not found")

    parkingplace_list = database.query(ParkingPlace).filter(ParkingPlace.hasPlaces_id == garage_id).all()

    return {
        "garage_id": garage_id,
        "parkingplace_count": len(parkingplace_list),
        "parkingplace": parkingplace_list
    }



############################################
#   Garage Method Endpoints
############################################




@app.post("/garage/methods/refreshAvailabilityStatus/", response_model=None, tags=["Garage Methods"])
async def garage_refreshAvailabilityStatus(
    database: Session = Depends(get_db)
):
    """
    Execute the refreshAvailabilityStatus class method on Garage.
    This method operates on all Garage entities or performs class-level operations.
    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output


        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "Garage",
            "method": "refreshAvailabilityStatus",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")




############################################
#
#   ParkingPlace functions
#
############################################

@app.get("/parkingplace/", response_model=None, tags=["ParkingPlace"])
def get_all_parkingplace(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ParkingPlace)
        query = query.options(joinedload(ParkingPlace.hasPlaces))
        parkingplace_list = query.all()

        # Serialize with relationships included
        result = []
        for parkingplace_item in parkingplace_list:
            item_dict = parkingplace_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if parkingplace_item.hasPlaces:
                related_obj = parkingplace_item.hasPlaces
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['hasPlaces'] = related_dict
            else:
                item_dict['hasPlaces'] = None


            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ParkingPlace).all()


@app.get("/parkingplace/count/", response_model=None, tags=["ParkingPlace"])
def get_count_parkingplace(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ParkingPlace entities"""
    count = database.query(ParkingPlace).count()
    return {"count": count}


@app.get("/parkingplace/paginated/", response_model=None, tags=["ParkingPlace"])
def get_paginated_parkingplace(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ParkingPlace entities"""
    total = database.query(ParkingPlace).count()
    parkingplace_list = database.query(ParkingPlace).offset(skip).limit(limit).all()
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": parkingplace_list
    }


@app.get("/parkingplace/search/", response_model=None, tags=["ParkingPlace"])
def search_parkingplace(
    database: Session = Depends(get_db)
) -> list:
    """Search ParkingPlace entities by attributes"""
    query = database.query(ParkingPlace)


    results = query.all()
    return results


@app.get("/parkingplace/{parkingplace_id}/", response_model=None, tags=["ParkingPlace"])
async def get_parkingplace(parkingplace_id: int, database: Session = Depends(get_db)) -> ParkingPlace:
    db_parkingplace = database.query(ParkingPlace).filter(ParkingPlace.id == parkingplace_id).first()
    if db_parkingplace is None:
        raise HTTPException(status_code=404, detail="ParkingPlace not found")

    response_data = {
        "parkingplace": db_parkingplace,
}
    return response_data



@app.post("/parkingplace/", response_model=None, tags=["ParkingPlace"])
async def create_parkingplace(parkingplace_data: ParkingPlaceCreate, database: Session = Depends(get_db)) -> ParkingPlace:

    if parkingplace_data.hasPlaces is not None:
        db_hasPlaces = database.query(Garage).filter(Garage.id == parkingplace_data.hasPlaces).first()
        if not db_hasPlaces:
            raise HTTPException(status_code=400, detail="Garage not found")
    else:
        raise HTTPException(status_code=400, detail="Garage ID is required")

    db_parkingplace = ParkingPlace(
        isFree=parkingplace_data.isFree,        lastUpdated=parkingplace_data.lastUpdated,        placeId=parkingplace_data.placeId,        locationDescription=parkingplace_data.locationDescription,        hasPlaces_id=parkingplace_data.hasPlaces        )

    database.add(db_parkingplace)
    database.commit()
    database.refresh(db_parkingplace)




    return db_parkingplace


@app.post("/parkingplace/bulk/", response_model=None, tags=["ParkingPlace"])
async def bulk_create_parkingplace(items: list[ParkingPlaceCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ParkingPlace entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item
            if not item_data.hasPlaces:
                raise ValueError("Garage ID is required")

            db_parkingplace = ParkingPlace(
                isFree=item_data.isFree,                lastUpdated=item_data.lastUpdated,                placeId=item_data.placeId,                locationDescription=item_data.locationDescription,                hasPlaces_id=item_data.hasPlaces            )
            database.add(db_parkingplace)
            database.flush()  # Get ID without committing
            created_items.append(db_parkingplace.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ParkingPlace entities"
    }


@app.delete("/parkingplace/bulk/", response_model=None, tags=["ParkingPlace"])
async def bulk_delete_parkingplace(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ParkingPlace entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_parkingplace = database.query(ParkingPlace).filter(ParkingPlace.id == item_id).first()
        if db_parkingplace:
            database.delete(db_parkingplace)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ParkingPlace entities"
    }

@app.put("/parkingplace/{parkingplace_id}/", response_model=None, tags=["ParkingPlace"])
async def update_parkingplace(parkingplace_id: int, parkingplace_data: ParkingPlaceCreate, database: Session = Depends(get_db)) -> ParkingPlace:
    db_parkingplace = database.query(ParkingPlace).filter(ParkingPlace.id == parkingplace_id).first()
    if db_parkingplace is None:
        raise HTTPException(status_code=404, detail="ParkingPlace not found")

    setattr(db_parkingplace, 'isFree', parkingplace_data.isFree)
    setattr(db_parkingplace, 'lastUpdated', parkingplace_data.lastUpdated)
    setattr(db_parkingplace, 'placeId', parkingplace_data.placeId)
    setattr(db_parkingplace, 'locationDescription', parkingplace_data.locationDescription)
    if parkingplace_data.hasPlaces is not None:
        db_hasPlaces = database.query(Garage).filter(Garage.id == parkingplace_data.hasPlaces).first()
        if not db_hasPlaces:
            raise HTTPException(status_code=400, detail="Garage not found")
        setattr(db_parkingplace, 'hasPlaces_id', parkingplace_data.hasPlaces)
    database.commit()
    database.refresh(db_parkingplace)

    return db_parkingplace


@app.delete("/parkingplace/{parkingplace_id}/", response_model=None, tags=["ParkingPlace"])
async def delete_parkingplace(parkingplace_id: int, database: Session = Depends(get_db)):
    db_parkingplace = database.query(ParkingPlace).filter(ParkingPlace.id == parkingplace_id).first()
    if db_parkingplace is None:
        raise HTTPException(status_code=404, detail="ParkingPlace not found")
    database.delete(db_parkingplace)
    database.commit()
    return db_parkingplace




############################################
#   ParkingPlace Method Endpoints
############################################




@app.post("/parkingplace/methods/updateAvailability/", response_model=None, tags=["ParkingPlace Methods"])
async def parkingplace_updateAvailability(
    params: dict = Body(default=None, embed=True),
    database: Session = Depends(get_db)
):
    """
    Execute the updateAvailability class method on ParkingPlace.
    This method operates on all ParkingPlace entities or performs class-level operations.

    Parameters (pass as JSON body):
    - freeStatus: bool    """
    try:
        # Capture stdout to include print outputs in the response
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Extract parameters from request body
        params = params or {}
        freeStatus = params.get('freeStatus')

        # Method body not defined
        result = None

        # Restore stdout
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Handle result serialization
        if hasattr(result, '__iter__') and not isinstance(result, (str, dict)):
            # It's a list of entities
            result_data = []
            for item in result:
                if hasattr(item, '__dict__'):
                    item_dict = {k: v for k, v in item.__dict__.items() if not k.startswith('_')}
                    result_data.append(item_dict)
                else:
                    result_data.append(str(item))
            result = result_data
        elif hasattr(result, '__dict__'):
            result = {k: v for k, v in result.__dict__.items() if not k.startswith('_')}

        return {
            "class": "ParkingPlace",
            "method": "updateAvailability",
            "status": "executed",
            "result": result,
            "output": output if output else None
        }
    except Exception as e:
        sys.stdout = sys.__stdout__
        raise HTTPException(status_code=500, detail=f"Method execution failed: {str(e)}")






############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



