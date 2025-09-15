import pytest
import sys
import os

# Set environment variables before importing the app
os.environ['DATABASE_URL'] = 'sqlite:///./test.db'
os.environ['MODELS_PATH'] = './test_models'
os.environ['LOG_DIR'] = './test_logs'

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from api.main import app
    from fastapi.testclient import TestClient
    API_AVAILABLE = True
except ImportError as e:
    API_AVAILABLE = False
    pytest.skip(f"API module not available: {e}", allow_module_level=True)

@pytest.mark.skipif(not API_AVAILABLE, reason="API not available")
class TestAPI:
    
    @pytest.fixture
    def client(self):
        return TestClient(app)
    
    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test"""
        # Create test directories
        os.makedirs('./test_models', exist_ok=True)
        os.makedirs('./test_logs', exist_ok=True)
        
        yield
        
        # Cleanup after tests
        import shutil
        if os.path.exists('./test.db'):
            os.remove('./test.db')
        if os.path.exists('./test_models'):
            shutil.rmtree('./test_models')
        if os.path.exists('./test_logs'):
            shutil.rmtree('./test_logs')
    
    def test_health_endpoint(self, client):
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
        assert "models_path" in response.json()
        assert response.json()["models_path"] == "./test_models"
    
    def test_root_endpoint_detailed(self, client):
        """Test root endpoint with detailed checks"""
        response = client.get("/")
        
        assert response.status_code == 200
        assert "message" in response.json()
        assert "Food Price Forecast API" in response.json()["message"]
    
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

    def test_test_model_endpoint(self, client):
        """Test the test-model endpoint"""
        response = client.get("/test-model")
        assert response.status_code == 200
        assert "status" in response.json()
        # This endpoint should return either success or error, both are valid responses
        assert response.json()["status"] in ["success", "error"]

    def test_environment_variables_used(self, client):
        """Test that the environment variables are properly used"""
        response = client.get("/health")
        data = response.json()
        
        assert data["models_path"] == "./test_models"
        # Database URL should contain the test database path
        assert "test.db" in data.get("database_url", "")