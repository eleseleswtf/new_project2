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
        {"name": "ParkingAvailability", "description": "Operations for ParkingAvailability entities"},
        {"name": "ParkingAvailability Relationships", "description": "Manage ParkingAvailability relationships"},
        {"name": "ParkingAvailability Methods", "description": "Execute ParkingAvailability methods"},
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
    stats["parkingavailability_count"] = database.query(ParkingAvailability).count()
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
#   ParkingAvailability functions
#
############################################

@app.get("/parkingavailability/", response_model=None, tags=["ParkingAvailability"])
def get_all_parkingavailability(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(ParkingAvailability)
        parkingavailability_list = query.all()

        # Serialize with relationships included
        result = []
        for parkingavailability_item in parkingavailability_list:
            item_dict = parkingavailability_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            parkingplace_list = database.query(ParkingPlace).filter(ParkingPlace.parkingavailability_id == parkingavailability_item.id).all()
            item_dict['hasPlaces'] = []
            for parkingplace_obj in parkingplace_list:
                parkingplace_dict = parkingplace_obj.__dict__.copy()
                parkingplace_dict.pop('_sa_instance_state', None)
                item_dict['hasPlaces'].append(parkingplace_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(ParkingAvailability).all()


@app.get("/parkingavailability/count/", response_model=None, tags=["ParkingAvailability"])
def get_count_parkingavailability(database: Session = Depends(get_db)) -> dict:
    """Get the total count of ParkingAvailability entities"""
    count = database.query(ParkingAvailability).count()
    return {"count": count}


@app.get("/parkingavailability/paginated/", response_model=None, tags=["ParkingAvailability"])
def get_paginated_parkingavailability(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of ParkingAvailability entities"""
    total = database.query(ParkingAvailability).count()
    parkingavailability_list = database.query(ParkingAvailability).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": parkingavailability_list
        }

    result = []
    for parkingavailability_item in parkingavailability_list:
        hasPlaces_ids = database.query(ParkingPlace.id).filter(ParkingPlace.parkingavailability_id == parkingavailability_item.id).all()
        item_data = {
            "parkingavailability": parkingavailability_item,
            "hasPlaces_ids": [x[0] for x in hasPlaces_ids]        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/parkingavailability/search/", response_model=None, tags=["ParkingAvailability"])
def search_parkingavailability(
    database: Session = Depends(get_db)
) -> list:
    """Search ParkingAvailability entities by attributes"""
    query = database.query(ParkingAvailability)


    results = query.all()
    return results


@app.get("/parkingavailability/{parkingavailability_id}/", response_model=None, tags=["ParkingAvailability"])
async def get_parkingavailability(parkingavailability_id: int, database: Session = Depends(get_db)) -> ParkingAvailability:
    db_parkingavailability = database.query(ParkingAvailability).filter(ParkingAvailability.id == parkingavailability_id).first()
    if db_parkingavailability is None:
        raise HTTPException(status_code=404, detail="ParkingAvailability not found")

    hasPlaces_ids = database.query(ParkingPlace.id).filter(ParkingPlace.parkingavailability_id == db_parkingavailability.id).all()
    response_data = {
        "parkingavailability": db_parkingavailability,
        "hasPlaces_ids": [x[0] for x in hasPlaces_ids]}
    return response_data



@app.post("/parkingavailability/", response_model=None, tags=["ParkingAvailability"])
async def create_parkingavailability(parkingavailability_data: ParkingAvailabilityCreate, database: Session = Depends(get_db)) -> ParkingAvailability:


    db_parkingavailability = ParkingAvailability(
        anyPlaceFree=parkingavailability_data.anyPlaceFree,        checkedAt=parkingavailability_data.checkedAt,        bothPlacesFree=parkingavailability_data.bothPlacesFree,        availabilityId=parkingavailability_data.availabilityId        )

    database.add(db_parkingavailability)
    database.commit()
    database.refresh(db_parkingavailability)

    if parkingavailability_data.hasPlaces:
        # Validate that all ParkingPlace IDs exist
        for parkingplace_id in parkingavailability_data.hasPlaces:
            db_parkingplace = database.query(ParkingPlace).filter(ParkingPlace.id == parkingplace_id).first()
            if not db_parkingplace:
                raise HTTPException(status_code=400, detail=f"ParkingPlace with id {parkingplace_id} not found")

        # Update the related entities with the new foreign key
        database.query(ParkingPlace).filter(ParkingPlace.id.in_(parkingavailability_data.hasPlaces)).update(
            {ParkingPlace.parkingavailability_id: db_parkingavailability.id}, synchronize_session=False
        )
        database.commit()



    hasPlaces_ids = database.query(ParkingPlace.id).filter(ParkingPlace.parkingavailability_id == db_parkingavailability.id).all()
    response_data = {
        "parkingavailability": db_parkingavailability,
        "hasPlaces_ids": [x[0] for x in hasPlaces_ids]    }
    return response_data


@app.post("/parkingavailability/bulk/", response_model=None, tags=["ParkingAvailability"])
async def bulk_create_parkingavailability(items: list[ParkingAvailabilityCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple ParkingAvailability entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_parkingavailability = ParkingAvailability(
                anyPlaceFree=item_data.anyPlaceFree,                checkedAt=item_data.checkedAt,                bothPlacesFree=item_data.bothPlacesFree,                availabilityId=item_data.availabilityId            )
            database.add(db_parkingavailability)
            database.flush()  # Get ID without committing
            created_items.append(db_parkingavailability.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} ParkingAvailability entities"
    }


@app.delete("/parkingavailability/bulk/", response_model=None, tags=["ParkingAvailability"])
async def bulk_delete_parkingavailability(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple ParkingAvailability entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_parkingavailability = database.query(ParkingAvailability).filter(ParkingAvailability.id == item_id).first()
        if db_parkingavailability:
            database.delete(db_parkingavailability)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} ParkingAvailability entities"
    }

@app.put("/parkingavailability/{parkingavailability_id}/", response_model=None, tags=["ParkingAvailability"])
async def update_parkingavailability(parkingavailability_id: int, parkingavailability_data: ParkingAvailabilityCreate, database: Session = Depends(get_db)) -> ParkingAvailability:
    db_parkingavailability = database.query(ParkingAvailability).filter(ParkingAvailability.id == parkingavailability_id).first()
    if db_parkingavailability is None:
        raise HTTPException(status_code=404, detail="ParkingAvailability not found")

    setattr(db_parkingavailability, 'anyPlaceFree', parkingavailability_data.anyPlaceFree)
    setattr(db_parkingavailability, 'checkedAt', parkingavailability_data.checkedAt)
    setattr(db_parkingavailability, 'bothPlacesFree', parkingavailability_data.bothPlacesFree)
    setattr(db_parkingavailability, 'availabilityId', parkingavailability_data.availabilityId)
    if parkingavailability_data.hasPlaces is not None:
        # Clear all existing relationships (set foreign key to NULL)
        database.query(ParkingPlace).filter(ParkingPlace.parkingavailability_id == db_parkingavailability.id).update(
            {ParkingPlace.parkingavailability_id: None}, synchronize_session=False
        )

        # Set new relationships if list is not empty
        if parkingavailability_data.hasPlaces:
            # Validate that all IDs exist
            for parkingplace_id in parkingavailability_data.hasPlaces:
                db_parkingplace = database.query(ParkingPlace).filter(ParkingPlace.id == parkingplace_id).first()
                if not db_parkingplace:
                    raise HTTPException(status_code=400, detail=f"ParkingPlace with id {parkingplace_id} not found")

            # Update the related entities with the new foreign key
            database.query(ParkingPlace).filter(ParkingPlace.id.in_(parkingavailability_data.hasPlaces)).update(
                {ParkingPlace.parkingavailability_id: db_parkingavailability.id}, synchronize_session=False
            )
    database.commit()
    database.refresh(db_parkingavailability)

    hasPlaces_ids = database.query(ParkingPlace.id).filter(ParkingPlace.parkingavailability_id == db_parkingavailability.id).all()
    response_data = {
        "parkingavailability": db_parkingavailability,
        "hasPlaces_ids": [x[0] for x in hasPlaces_ids]    }
    return response_data


@app.delete("/parkingavailability/{parkingavailability_id}/", response_model=None, tags=["ParkingAvailability"])
async def delete_parkingavailability(parkingavailability_id: int, database: Session = Depends(get_db)):
    db_parkingavailability = database.query(ParkingAvailability).filter(ParkingAvailability.id == parkingavailability_id).first()
    if db_parkingavailability is None:
        raise HTTPException(status_code=404, detail="ParkingAvailability not found")
    database.delete(db_parkingavailability)
    database.commit()
    return db_parkingavailability


@app.get("/parkingavailability/{parkingavailability_id}/hasPlaces/", response_model=None, tags=["ParkingAvailability Relationships"])
async def get_hasPlaces_of_parkingavailability(parkingavailability_id: int, database: Session = Depends(get_db)):
    """Get all ParkingPlace entities related to this ParkingAvailability through hasPlaces"""
    db_parkingavailability = database.query(ParkingAvailability).filter(ParkingAvailability.id == parkingavailability_id).first()
    if db_parkingavailability is None:
        raise HTTPException(status_code=404, detail="ParkingAvailability not found")

    hasPlaces_list = database.query(ParkingPlace).filter(ParkingPlace.parkingavailability_id == parkingavailability_id).all()

    return {
        "parkingavailability_id": parkingavailability_id,
        "hasPlaces_count": len(hasPlaces_list),
        "hasPlaces": hasPlaces_list
    }



############################################
#   ParkingAvailability Method Endpoints
############################################




@app.post("/parkingavailability/methods/refreshAvailabilityStatus/", response_model=None, tags=["ParkingAvailability Methods"])
async def parkingavailability_refreshAvailabilityStatus(
    database: Session = Depends(get_db)
):
    """
    Execute the refreshAvailabilityStatus class method on ParkingAvailability.
    This method operates on all ParkingAvailability entities or performs class-level operations.
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
            "class": "ParkingAvailability",
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
        query = query.options(joinedload(ParkingPlace.parkingavailability))
        parkingplace_list = query.all()

        # Serialize with relationships included
        result = []
        for parkingplace_item in parkingplace_list:
            item_dict = parkingplace_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)
            if parkingplace_item.parkingavailability:
                related_obj = parkingplace_item.parkingavailability
                related_dict = related_obj.__dict__.copy()
                related_dict.pop('_sa_instance_state', None)
                item_dict['parkingavailability'] = related_dict
            else:
                item_dict['parkingavailability'] = None


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

    if parkingplace_data.parkingavailability is not None:
        db_parkingavailability = database.query(ParkingAvailability).filter(ParkingAvailability.id == parkingplace_data.parkingavailability).first()
        if not db_parkingavailability:
            raise HTTPException(status_code=400, detail="ParkingAvailability not found")
    else:
        raise HTTPException(status_code=400, detail="ParkingAvailability ID is required")

    db_parkingplace = ParkingPlace(
        placeId=parkingplace_data.placeId,        lastUpdated=parkingplace_data.lastUpdated,        isFree=parkingplace_data.isFree,        locationDescription=parkingplace_data.locationDescription,        parkingavailability_id=parkingplace_data.parkingavailability        )

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
            if not item_data.parkingavailability:
                raise ValueError("ParkingAvailability ID is required")

            db_parkingplace = ParkingPlace(
                placeId=item_data.placeId,                lastUpdated=item_data.lastUpdated,                isFree=item_data.isFree,                locationDescription=item_data.locationDescription,                parkingavailability_id=item_data.parkingavailability            )
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

    setattr(db_parkingplace, 'placeId', parkingplace_data.placeId)
    setattr(db_parkingplace, 'lastUpdated', parkingplace_data.lastUpdated)
    setattr(db_parkingplace, 'isFree', parkingplace_data.isFree)
    setattr(db_parkingplace, 'locationDescription', parkingplace_data.locationDescription)
    if parkingplace_data.parkingavailability is not None:
        db_parkingavailability = database.query(ParkingAvailability).filter(ParkingAvailability.id == parkingplace_data.parkingavailability).first()
        if not db_parkingavailability:
            raise HTTPException(status_code=400, detail="ParkingAvailability not found")
        setattr(db_parkingplace, 'parkingavailability_id', parkingplace_data.parkingavailability)
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



