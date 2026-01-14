from pydantic import BaseModel, Field

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