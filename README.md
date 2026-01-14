# FastAPI Item Management API

A production-ready REST API for managing items, built with FastAPI and modern Python practices.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ Input validation with Pydantic
- ✅ Auto-generated OpenAPI documentation
- ✅ Comprehensive error handling
- ✅ Health check endpoint
- ✅ Type hints throughout

## Tech Stack

- **Framework:** FastAPI 0.115.0
- **Validation:** Pydantic 2.0+
- **Server:** Uvicorn

## Getting Started

### Installation

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Run

\`\`\`bash
uvicorn main:app --reload
\`\`\`

### API Documentation

Visit http://localhost:8000/docs for interactive API documentation.

## API Endpoints

- `GET /items` - List all items
- `POST /items` - Create new item
- `GET /items/{id}` - Get single item
- `DELETE /items/{id}` - Delete item
- `GET /health` - Health check

## Project Status

🚧 **Week 1 of 6-week ML Engineering Roadmap** 🚧

Part of my journey to become a production-r. Follow along as I build:
- Week 1: FastAPI + Docker + AWS deployment
- Week 2: Multi-model recommendation system
- Week 3-6: Production features, databases, and more!

## Author

Alexander Ioffrida - NYU Neuroscience + CS Student
