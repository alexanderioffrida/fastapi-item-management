# FastAPI Item Management API

A production-ready REST API for managing items, built with FastAPI and modern Python practices.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ Pagination and filtering support
- ✅ Input validation with Pydantic
- ✅ Auto-generated OpenAPI documentation
- ✅ Comprehensive error handling with custom exceptions
- ✅ Health check endpoint
- ✅ Type hints throughout
- ✅ Thread-safe ID generation
- ✅ O(1) item lookups with dict-based storage
- ✅ Structured logging

## Tech Stack

- **Framework:** FastAPI 0.115.0
- **Validation:** Pydantic 2.10+
- **Server:** Uvicorn
- **Testing:** pytest, pytest-asyncio, httpx

## Getting Started

### Installation

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run

```bash
uvicorn main:app --reload
```

### Run Tests

```bash
pytest
```

### API Documentation

Visit http://localhost:8000/docs for interactive Swagger UI documentation.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message and API info |
| `GET` | `/items` | List items (with filtering & pagination) |
| `GET` | `/items/{id}` | Get item by ID |
| `POST` | `/items` | Create new item |
| `PUT` | `/items/{id}` | Replace item (full update) |
| `PATCH` | `/items/{id}` | Update item (partial update) |
| `DELETE` | `/items/{id}` | Delete item by ID |
| `GET` | `/health` | Health check |

### Query Parameters for `GET /items`

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `skip` | int | 0 | Number of items to skip (pagination offset) |
| `limit` | int | 10 | Max items to return (1-100) |
| `name` | string | — | Filter by name (case-insensitive) |
| `min_price` | float | — | Filter by minimum price |
| `max_price` | float | — | Filter by maximum price |
| `in_stock` | bool | — | Filter by stock availability |

**Example:**
```
GET /items?min_price=10&max_price=50&skip=0&limit=5
```

## Project Status

🚧 **Week 1 of 6-week ML Engineering Interview Prep** 🚧

Part of my journey to become a production-ready ML engineer. Follow along as I build:
- Week 1: FastAPI + Docker + AWS deployment
- Week 2: Multi-model recommendation system
- Week 3-6: Production features, databases, and more!

## Author

Alexander Ioffrida - NYU Neuroscience + CS Student
