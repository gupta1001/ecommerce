# E-Commerce Platform API

This repository contains a production-grade RESTful API for a simple e-commerce platform built with FastAPI and MongoDB.

## Features

- **Endpoints:**
  - `GET /api/getproducts`: Retrieve a list of all available products.
  - `POST /api/addproducts`: Add a new product.
  - `POST /orders`: Place an order (with stock and product_id validation).

- **Data Models:**
  - **Product:** `name`, `description`, `price`, `stock`.
  - **Order:** List of ordered items, `total_price`, `status`.

- **Business Logic:**
  - Validates product stock before processing an order.
  - Deducts stock upon successful order placement.

- **Testing:**
  - Comprehensive tests using `pytest-asyncio` and `httpx.AsyncClient`.
  - Utilise docker CLI to run the test scripts
  - Run pytest tests/test_main.py

- **Dockerized:**
  - Both the application and MongoDB are containerized using Docker and Docker Compose.

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)

### Running with Docker Compose

1. **Build and start the containers:**

   ```bash
   docker-compose up --build