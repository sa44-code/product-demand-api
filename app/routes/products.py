from fastapi import APIRouter
from app.database import get_connection

router = APIRouter()

@router.get("/products")
def get_products():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, category
        FROM products
        ORDER BY id
    """)

    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "category": row[2]
        }
        for row in rows
    ]

