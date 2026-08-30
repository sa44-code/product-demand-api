from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.database import get_connection
from ml.model import predict_demand

from datetime import date, timedelta
from app.services.inventory import calculate_reorder_quantity


router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


class InventoryUpdate(BaseModel):
    quantity: int = Field(ge=0)


@router.get("/")
def get_inventory():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            inventory.product_id,
            products.name,
            inventory.quantity
        FROM inventory
        JOIN products
            ON inventory.product_id = products.id
        ORDER BY inventory.product_id
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "product_id": row[0],
            "product_name": row[1],
            "quantity": row[2]
        }
        for row in rows
    ]


@router.get("/{product_id}")
def get_product_inventory(product_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            inventory.product_id,
            products.name,
            inventory.quantity
        FROM inventory
        JOIN products
            ON inventory.product_id = products.id
        WHERE inventory.product_id = %s
    """, (product_id,))

    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        raise HTTPException(
            status_code=404,
            detail=f"Inventory for product {product_id} not found"
        )

    return {
        "product_id": row[0],
        "product_name": row[1],
        "quantity": row[2]
    }


@router.put("/{product_id}")
def update_inventory(
    product_id: int,
    inventory: InventoryUpdate
):

    conn = get_connection()
    cursor = conn.cursor()

    # Check product
    cursor.execute(
        "SELECT id FROM products WHERE id = %s",
        (product_id,)
    )

    product = cursor.fetchone()

    if not product:
        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail=f"Product {product_id} not found"
        )

    # Check inventory
    cursor.execute(
        "SELECT id FROM inventory WHERE product_id = %s",
        (product_id,)
    )

    existing = cursor.fetchone()

    if existing:

        cursor.execute("""
            UPDATE inventory
            SET quantity = %s
            WHERE product_id = %s
            RETURNING product_id, quantity
        """, (
            inventory.quantity,
            product_id
        ))

    else:

        cursor.execute("""
            INSERT INTO inventory (product_id, quantity)
            VALUES (%s, %s)
            RETURNING product_id, quantity
        """, (
            product_id,
            inventory.quantity
        ))

    result = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "product_id": result[0],
        "quantity": result[1]
    }

@router.get("/recommendation/{product_id}")
def get_reorder_recommendation(product_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    # Get product
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

    # Get inventory
    cursor.execute("""
        SELECT quantity
        FROM inventory
        WHERE product_id = %s
    """, (product_id,))

    inventory_row = cursor.fetchone()

    if not inventory_row:
        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail=f"Inventory for product {product_id} not found"
        )

    current_inventory = inventory_row[0]

    # Get sales
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
            "product_name": product[1],
            "message": "No sales data found"
        }

    sales_data = []

    for row in rows:
        sales_data.append({
            "product_id": product_id,
            "date": row[0],
            "quantity_sold": row[1]
        })

    # Generate ML forecast
    forecast = predict_demand(sales_data)

    # Calculate reorder quantity
    recommendation = calculate_reorder_quantity(
        current_inventory,
        forecast
    )

    return {
        "product_id": product[0],
        "product_name": product[1],
        "current_inventory": current_inventory,
        "forecast": forecast,
        "forecast_7_days": recommendation["forecast_7_days"],
        "recommended_order": recommendation["recommended_order"]
    }
