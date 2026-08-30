from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from datetime import date
from app.database import get_connection

router = APIRouter()


class SaleCreate(BaseModel):
    product_id: int = Field(gt=0)
    date: date
    quantity_sold: int = Field(ge=0)

@router.get("/sales")
def get_sales():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_id, date, quantity_sold
        FROM sales
        ORDER BY date
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "product_id": row[0],
            "date": str(row[1]),
            "quantity_sold": row[2]
        }
        for row in rows
    ]

@router.get("/sales/{product_id}")
def get_product_sales(product_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_id, date, quantity_sold
        FROM sales
        WHERE product_id = %s
        ORDER BY date
    """, (product_id,))

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "product_id": row[0],
            "date": str(row[1]),
            "quantity_sold": row[2]
        }
        for row in rows
    ]

@router.post("/sales")
def create_sale(sale: SaleCreate):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM products WHERE id = %s",
        (sale.product_id,)
    )

    product = cursor.fetchone()

    if not product:
        cursor.close()
        conn.close()

        raise HTTPException(
            status_code=404,
            detail=f"Product {sale.product_id} not found"
        )

    cursor.execute("""
        INSERT INTO sales (product_id, date, quantity_sold)
        VALUES (%s, %s, %s)
        RETURNING id, product_id, date, quantity_sold
    """, (
        sale.product_id,
        sale.date,
        sale.quantity_sold
    ))

    new_sale = cursor.fetchone()

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "id": new_sale[0],
        "product_id": new_sale[1],
        "date": str(new_sale[2]),
        "quantity_sold": new_sale[3]
    }
