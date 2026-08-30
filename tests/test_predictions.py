def test_invalid_sale_quantity(client):

    response = client.post(
        "/sales",
        json={
            "product_id": 2,
            "date": "2026-08-25",
            "quantity_sold": -10
        }
    )

    assert response.status_code == 422
def test_forecast_product(client):

    response = client.get("/forecast/2")

    assert response.status_code == 200

    data = response.json()

    assert data["product_id"] == 2
    assert data["method"] == "3-day moving average"
    assert "forecast" in data
