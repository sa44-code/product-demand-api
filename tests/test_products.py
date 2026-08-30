from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_products():

    response = client.get("/products")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Product Demand API is running!"
    }
