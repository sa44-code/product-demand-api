from fastapi import FastAPI
from app.routes import products
from app.routes import sales
from app.routes import predictions
from app.routes.inventory import router as inventory_router


app = FastAPI(title="Product Demand Forecasting API",
    description="API for product sales and demand forecasting",
    version="1.0.0")
app.include_router(inventory_router)


@app.get("/")
def home():
    return {
        "message": "Product Demand API is running!"
    }

app.include_router(products.router)
app.include_router(sales.router)
app.include_router(predictions.router)

















# @app.get("/predict/{product_id}")
# def predict_product_demand(product_id: int):

#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("""
#         SELECT date, quantity_sold
#         FROM sales
#         WHERE product_id = %s
#         ORDER BY date
#     """, (product_id,))

#     rows = cursor.fetchall()

#     cursor.close()
#     conn.close()

#     if not rows:
#         return {
#             "product_id": product_id,
#             "message": "No sales data found"
#         }

#     sales_data = []

#     for row in rows:
#         sales_data.append({
#             "product_id": product_id,
#             "date": row[0],
#             "quantity_sold": row[1]
#         })

#     predictions = predict_demand(sales_data)

#     return {
#         "product_id": product_id,
#         "forecast": predictions
#     }

