import logging
import threading
import traceback

from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from models import (
    Item,
    ItemCreate,
    ItemUpdate,
    ItemResponse,
    ErrorResponse,
    PaginationParams,
    ItemFilters,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ================================================================
# Custom Exception Classes
# ================================================================

class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(f"Item with ID {item_id} not found")


class DatabaseError(Exception):
    pass


# ================================================================
# Application Setup
# ================================================================

app = FastAPI(
    title="Item Management API",
    description="A simple FastAPI application for managing items",
    version="1.0.0",
)

# Thread-safe in-memory storage (replace with a database in production)
items_db: dict[int, Item] = {}
_id_lock = threading.Lock()
_next_id = 1


def get_next_id() -> int:
    """Thread-safe ID generation."""
    global _next_id
    with _id_lock:
        current_id = _next_id
        _next_id += 1
    return current_id


# ================================================================
# Dependency Functions
# ================================================================

def get_pagination(
    skip: int = Query(default=0, ge=0, description="Number of items to skip"),
    limit: int = Query(default=10, ge=1, le=100, description="Number of items to return"),
) -> PaginationParams:
    """Parse pagination query parameters."""
    return PaginationParams(skip=skip, limit=limit)


def get_item_filters(
    name: str | None = Query(default=None, description="Filter by name (case-insensitive)"),
    min_price: float | None = Query(default=None, ge=0, description="Minimum price"),
    max_price: float | None = Query(default=None, ge=0, description="Maximum price"),
    in_stock: bool | None = Query(default=None, description="Filter by stock availability"),
) -> ItemFilters:
    """Parse item filter query parameters."""
    return ItemFilters(name=name, min_price=min_price, max_price=max_price, in_stock=in_stock)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint - Returns a simple welcome message
    """
    return {
        "message": "Welcome to the Item Management API",
        "version": "1.0.0",
        "endpoints": {
            "GET /items": "Get all items",
            "POST /items": "Create a new item",
            "DELETE /items/{item_id}": "Delete an item by ID",
        }
    }

@app.get(
    "/items",
    response_model=list[Item],
    status_code=status.HTTP_200_OK,
    tags=["Items"],
    summary="Get all items",
    description="Retrieve items with optional filtering and pagination",
)
async def get_items(
    pagination: PaginationParams = Depends(get_pagination),
    filters: ItemFilters = Depends(get_item_filters),
):
    # Start with all items
    items = list(items_db.values())

    # Apply filters
    if filters.name:
        items = [i for i in items if filters.name.lower() in i.name.lower()]
    if filters.min_price is not None:
        items = [i for i in items if i.price >= filters.min_price]
    if filters.max_price is not None:
        items = [i for i in items if i.price <= filters.max_price]
    if filters.in_stock is not None:
        items = [i for i in items if (i.quantity > 0) == filters.in_stock]

    # Apply pagination
    return items[pagination.skip : pagination.skip + pagination.limit]

@app.get(
    "/items/{item_id}",
    response_model=Item,
    status_code=status.HTTP_200_OK,
    tags=["Items"],
    summary="Get an item by ID",
    description="Retrieve an item from the database by its ID",
)
async def get_item(item_id: int):
    if item_id not in items_db:
        raise ItemNotFoundError(item_id)
    return items_db[item_id]

@app.post(
    "/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    tags=["Items"],
    summary="Create a new item",
    description="Create a new item in the database",
)
async def create_item(item: ItemCreate):
    item_id = get_next_id()
    new_item = Item(id=item_id, **item.model_dump())
    items_db[item_id] = new_item
    return new_item

@app.put(
    "/items/{item_id}",
    response_model=Item,
    status_code=status.HTTP_200_OK,
    tags=["Items"],
    summary="Replace an item by ID",
    description="Replace an item in the database by its ID",
)
async def replace_item(item_id: int, item: ItemCreate):
    if item_id not in items_db:
        raise ItemNotFoundError(item_id)
    items_db[item_id] = Item(id=item_id, **item.model_dump())
    return items_db[item_id]

@app.patch(
    "/items/{item_id}",
    response_model=Item,
    status_code=status.HTTP_200_OK,
    tags=["Items"],
    summary="Partially update an item by ID",
    description="Update specific fields of an item in the database by its ID",
)
async def update_item(item_id: int, item: ItemUpdate):
    if item_id not in items_db:
        raise ItemNotFoundError(item_id)
    updated_item = items_db[item_id].model_copy(update=item.model_dump(exclude_unset=True))
    items_db[item_id] = updated_item
    return updated_item

@app.delete(
    "/items/{item_id}",
    response_model=ItemResponse,
    status_code=status.HTTP_200_OK,
    tags=["Items"],
    summary="Delete an item by ID",
    description="Delete an item from the database by its ID",
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Item not found",
        }
    }
)
async def delete_item(item_id: int):
    if item_id not in items_db:
        raise ItemNotFoundError(item_id)
    
    deleted_item = items_db.pop(item_id)
    return ItemResponse(
        message=f"Item with ID {item_id} has been deleted successfully",
        item=deleted_item
    )

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "items_count": len(items_db),
    }

# ================================================================
# Exception Handlers
# ================================================================

@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
            "item_id": exc.item_id,
            "error_type": "item_not_found",
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "error_type": "http_error",
        }
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    errors = exc.errors()

    formatted_errors = []
    for error in errors:
        formatted_errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
            "input": error.get("input"),
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error occurred",
            "error_type": "validation_error",
            "errors": formatted_errors,
        }
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request, exc: Exception):
    error_traceback = traceback.format_exc()
    logger.error(f"Internal Server Error: {error_traceback}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal server error occurred",
            "error_type": "internal_server_error",
            "message": "Please contact support if the problem persists",
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)