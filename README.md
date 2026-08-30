# 1. Problem Statement

Businesses need to make inventory related decisions based on estimated future product demand using historical sales data 

# 2. Objectives

Record product and sales details
Fetch historical sales records
Forecast future demand
Track inventory
Reorder quantities recommendation

# 3. Requirements

## Functional Requirements

### Product Management
- Fetch products records
- Products identification by ID

### Sales Management
- Add sales records
- Fetch sales records
- Fetch sales by product product ID

### Demand Forecasting
- Calculate historical demand
- Generate a 7-day forecast

### Inventory
- Record current inventory
- Fetch inventory details
- Update inventory details
- Calculate reorder recommendation

## Non-Functional Requirements

- User inputs should be validated
- Database data should be availabe even after the application is restarted or system failures
- The API should respond within an acceptable time
- The API should manage errors using appropriate HTTP status codes
- Code should be easy to maintain and modify
- API endpoints should be testable

# 4. Proposed Solution

### A backend application that manages product sales data, stores it in PostgreSQL,and uses machine learning to forecast product demand for the next 7 days

## Features

#### Product management
#### Sales management
#### PostgreSQL database integration
#### REST API using FastAPI
#### Request validation using Pydantic
#### 3-day moving-average forecasting
#### Machine-learning demand forecasting using Linear Regression
#### 7-day demand predictions
#### Error handling for invalid products
#### Automated API testing


# 5. Architecture

#### The application uses a simple layered architecture

## Main components

#### app/main.py - starts the FastAPI application and registers routes
#### app/database.py - PostgreSQL connection
#### app/routes/products.py - product endpoints
#### app/routes/sales.py - sales endpoints
#### app/routes/predictions.py - demand and forecasting endpoints
#### ml/model.py - machine-learning forecasting model
### Database

# 6. Technologies

Python
FastAPI
PostgreSQL
psycopg2
Pydantic
NumPy
Scikit-learn
Uvicorn
Pytest

# 7. Database design

## The application uses PostgreSQL.

##### Products table
Column	Type
id	SERIAL
name	VARCHAR
category	VARCHAR
##### Sales table
Column	Type
id	SERIAL
product_id	INTEGER
date	DATE
quantity_sold	INTEGER

# 8. API endpoints

Products
Method	Endpoint	Description
GET	/products	Get all products
Sales
Method	Endpoint	Description
GET	/sales	Get all sales
GET	/sales/{product_id}	Get sales for a product
POST	/sales	Add a new sale
Forecasting
Method	Endpoint	Description
GET	/demand/{product_id}	Get demand analysis
GET	/forecast/{product_id}	Calculate moving-average forecast
GET	/predict/{product_id}	Generate 7-day ML forecast

## 9. How to run it

1. Clone the repository
git clone YOUR_GITHUB_REPOSITORY_URL
cd product-demand-api

2. Create a virtual environment
python -m venv .venv

3. Activate it

Windows PowerShell:

.venv\Scripts\Activate.ps1

4. Install dependencies
pip install -r requirements.txt

5. Configure PostgreSQL

Create a PostgreSQL database and configure the database connection.

6. Start the API
python -m uvicorn app.main:app --reload --port 8001


The API will be available at:

http://127.0.0.1:8001


Swagger API documentation:

http://127.0.0.1:8001/docs

## 10. ML approach

Linea regression model is used to as the baseline. The model generates a seven-day demand forecast based on historical sales.

## 11. Example requests/responses

Example Request
Add a sale
POST /sales


Request:

{
  "product_id": 2,
  "date": "2026-08-23",
  "quantity_sold": 32
}


Response:

{
  "id": 11,
  "product_id": 2,
  "date": "2026-08-23",
  "quantity_sold": 32
}

Example ML Forecast
GET /predict/2


Response:

{
  "product_id": 2,
  "forecast": [
    {
      "date": "2026-08-25",
      "predicted_quantity": 35.38
    },
    {
      "date": "2026-08-26",
      "predicted_quantity": 36.54
    }
  ]
}

# 12. Testing 

The application is tested to verify the core functionality, input validation, database operations, and error handling.

Run the test using pytest
# 13. Limitations & improvements

## Limitations
Linear Regression model is the baseline 
Supplier lead time is not considered during the reorder calculation  
Safety stock is not considered yet

## Future improvements

Authentication
Add safety stock
Add supplier lead time
Compare additional multiple forecasting models
Model evaluation using metrics
Docker deployment






