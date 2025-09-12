import pytest
import sys
import os

# Add the root directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from api.main import app
    from fastapi.testclient import TestClient
    HAS_API = True
except ImportError:
    HAS_API = False
    pytest.skip("API module not available", allow_module_level=True)

@pytest.mark.skipif(not HAS_API, reason="API module not available")
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
    
    def test_health_endpoint_detailed(self, client):
        """Test health endpoint with detailed checks"""
        response = client.get("/health")
        
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
        assert "message" in response.json()
    
    def test_root_endpoint_detailed(self, client):
        """Test root endpoint with detailed checks"""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "message" in response.json()
        assert "Food Price Tracker API" in response.json()["message"]
    
    def test_forecast_endpoint_success(self, client):
        """Test forecast endpoint with valid parameters"""
        response = client.get("/forecast/?admin_id=1.0&mkt_id=266&cm_id=0.0")
        
        # Should return 200 even if no forecast data exists yet
        assert response.status_code == 200
        assert "forecast" in response.json() or "error" in response.json() or "message" in response.json()
    
    def test_forecast_endpoint_missing_params(self, client):
        """Test forecast endpoint with missing parameters"""
        response = client.get("/forecast/")
        
        # Should return 422 (validation error) for missing required params
        assert response.status_code == 422
    
    def test_forecast_endpoint_invalid_params(self, client):
        """Test forecast endpoint with invalid parameters"""
        response = client.get("/forecast/?admin_id=invalid&mkt_id=abc&cm_id=xyz")
        
        # Should return 422 (validation error) for invalid parameter types
        assert response.status_code == 422
    
    def test_nonexistent_endpoint(self, client):
        """Test non-existent endpoint returns 404"""
        response = client.get("/nonexistent-endpoint")
        
        assert response.status_code == 404
    
    def test_api_docs_available(self, client):
        """Test that API documentation endpoints are available"""
        response = client.get("/docs")
        assert response.status_code == 200
        
        response = client.get("/redoc")
        assert response.status_code == 200