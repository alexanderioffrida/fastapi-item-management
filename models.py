from pydantic import BaseModel, Field, model_validator

class ItemBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=100, description="Name of the item")
    description: str | None = Field(None, max_length=300, description="Description of the item")
    price: float = Field(..., gt=0, description="Price of the item | Must be greater than 0")
    quantity: int = Field(default=1, ge=0, description="Quantity of the item | Must be greater than or equal to 0")

class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    """Model for partial updates - all fields optional."""
    name: str | None = Field(None, min_length=3, max_length=100, description="Name of the item")
    description: str | None = Field(None, max_length=300, description="Description of the item")
    price: float | None = Field(None, gt=0, description="Price of the item | Must be greater than 0")
    quantity: int | None = Field(None, ge=0, description="Quantity of the item | Must be greater than or equal to 0")


class Item(ItemBase):
    id: int = Field(..., gt=0, description="The unique ID of the item")

    class Config:
        # Enables ORM mode for compatibility with SQLAlchemy
        from_attributes = True

class ItemResponse(BaseModel):
    message: str = Field(..., description="Message about the item")
    item: Item | None = None

class ErrorResponse(BaseModel):
    detail: str = Field(..., description="Error message")

class ValidationErrorDetail(BaseModel):
    loc: list
    msg: str
    type: str

class ValidationErrorResponse(BaseModel):
    detail: str
    errors: list[ValidationErrorDetail]

class PaginationParams(BaseModel):
    skip: int = Field(default=0, ge=0, description="Number of items to skip")
    limit: int = Field(default=10, ge=1, le=100, description="Number of items to return")

class ItemFilters(BaseModel):
    name: str | None = Field(None, description="Filter items by name (case-insensitive contains)")
    min_price: float | None = Field(None, ge=0, description="Minimum price filter")
    max_price: float | None = Field(None, ge=0, description="Maximum price filter")
    in_stock: bool | None = Field(None, description="Filter items by stock status")

    @model_validator(mode="after")
    def validate_price_range(self):
        if self.min_price is not None and self.max_price is not None:
            if self.min_price > self.max_price:
                raise ValueError("Minimum price must be less than or equal to maximum price")
        return self