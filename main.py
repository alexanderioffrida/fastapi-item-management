from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from models import Item, ItemCreate, ItemResponse, ErrorResponse

app = FastAPI(
    title="Item Management API",
    description="A simple FastAPI application for managing items",
    version="1.0.0",
)

# In-memory storage (replace with a database in production)
items_db: list[Item] = []
next_id = 1

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
    description="Retrieve a list of all items in the database",
)
async def get_items():
    return items_db

@app.post(
    "/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    tags=["Items"],
    summary="Create a new item",
    description="Create a new item in the database",
)
async def create_item(item: ItemCreate):
    global next_id
    new_item = Item(id=next_id, **item.model_dump())
    items_db.append(new_item)
    next_id += 1
    return new_item

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
    for index, item in enumerate(items_db):
        if item.id == item_id:
            deleted_item = items_db.pop(index)
            return ItemResponse(
                message=f"Item with ID {item_id} has been deleted successfully",
                item=deleted_item
            )

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Item with ID {item_id} not found"
    )

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "items_count": len(items_db),
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)