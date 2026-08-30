from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_sales():

    response = client.get("/sales")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
def test_invalid_sale_quantity():

    response = client.post(
        "/sales",
        json={
            "product_id": 2,
            "date": "2026-08-25",
            "quantity_sold": -10
        }
    )

    assert response.status_code == 422
