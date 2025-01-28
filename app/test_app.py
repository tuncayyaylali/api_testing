from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_data():
    response = client.get("/data/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_data_item():
    response = client.get("/data/536373")
    if response.status_code == 200:
        assert "InvoiceNo" in response.json()[0]
    else:
        assert response.status_code == 404

def test_calculate_summary():
    response = client.get("/sales_summary/")
    if response.status_code == 200:
        assert "total_sales" in response.json()
    else:
        assert response.status_code == 400