from fastapi import APIRouter, HTTPException
from app.database import get_connection
from ml.model import predict_demand

router = APIRouter()

@router.get("/demand/{product_id}")
def get_demand(product_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, category
        FROM products
        WHERE id = %s
    """, (product_id,))

    product = cursor.fetchone()

    if not product:
        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found"
        )

    cursor.execute("""
        SELECT date, quantity_sold
        FROM sales
        WHERE product_id = %s
        ORDER BY date
    """, (product_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return {
            "product": {
                "id": product[0],
                "name": product[1],
                "category": product[2]
            },
            "message": "No sales data found"
        }

    sales_data = []

    for row in rows:
        sales_data.append({
            "product_id": product_id,
            "date": row[0],
            "quantity_sold": row[1]
        })

    average_demand = sum(
        item["quantity_sold"]
        for item in sales_data
    ) / len(sales_data)

    forecast = predict_demand(sales_data)

    return {
        "product": {
            "id": product[0],
            "name": product[1],
            "category": product[2]
        },
        "average_daily_demand": round(average_demand, 2),
        "historical_sales": [
            {
                "date": item["date"],
                "quantity_sold": item["quantity_sold"]
            }
            for item in sales_data
        ],
        "forecast": forecast
    }

@router.get("/forecast/{product_id}")
def forecast_demand(product_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, quantity_sold
        FROM sales
        WHERE product_id = %s
        ORDER BY date
    """, (product_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return {
            "product_id": product_id,
            "message": "No sales data found"
        }

    sales_data = [
        {
            "date": row[0],
            "quantity_sold": row[1]
        }
        for row in rows
    ]

    last_days = sales_data[-3:]

    forecast = sum(
        item["quantity_sold"]
        for item in last_days
    ) / len(last_days)

    return {
        "product_id": product_id,
        "method": "3-day moving average",
        "forecast": round(forecast, 2)
    }

@router.get("/predict/{product_id}")
def predict_product_demand(product_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT date, quantity_sold
        FROM sales
        WHERE product_id = %s
        ORDER BY date
    """, (product_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    if not rows:
        return {
            "product_id": product_id,
            "message": "No sales data found"
        }

    sales_data = [
        {
            "product_id": product_id,
            "date": row[0],
            "quantity_sold": row[1]
        }
        for row in rows
    ]

    predictions = predict_demand(sales_data)

    return {
        "product_id": product_id,
        "forecast": predictions
    }
