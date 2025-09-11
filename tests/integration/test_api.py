import pytest
from fastapi.testclient import TestClient
from api.main import app

class TestAPI:
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    def test_health_endpoint(self, client):
        """Test health endpoint"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "message" in response.json()
    
    def test_forecast_endpoint(self, client):
        """Test forecast endpoint"""
        response = client.get("/forecast/?admin_id=1.0&mkt_id=266&cm_id=0.0")
        
        assert response.status_code == 200
        assert "forecast" in response.json()
