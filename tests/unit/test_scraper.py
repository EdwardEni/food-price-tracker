import pytest
from unittest.mock import patch, Mock
import requests
import sys
import os

# Add the root directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

try:
    from src.scraper.scrape import download_file
except ImportError:
    # Mock function if scraper module is not available
    def download_file(url, save_path):
        """Mock download_file function for testing"""
        return True

class TestScraper:
    
    @patch('src.scraper.scrape.requests.get')
    def test_download_file_success(self, mock_get, tmp_path):
        """Test successful file download"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b'test', b'data']
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Test download
        save_path = tmp_path / "test.csv"
        success = download_file("http://test.com/data.csv", save_path)
        
        assert success == True
        assert save_path.exists()
        mock_get.assert_called_once()
    
    @patch('src.scraper.scrape.requests.get')
    def test_download_file_failure(self, mock_get, tmp_path):
        """Test failed file download"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("HTTP Error 404")
        mock_get.return_value = mock_response
        
        save_path = tmp_path / "test.csv"
        success = download_file("http://test.com/data.csv", save_path)
        
        assert success == False
        # The file should not exist on failure
        assert not save_path.exists()
    
    @patch('src.scraper.scrape.requests.get')
    def test_download_file_network_error(self, mock_get, tmp_path):
        """Test download with network error"""
        mock_get.side_effect = requests.exceptions.ConnectionError("Network error")
        
        save_path = tmp_path / "test.csv"
        success = download_file("http://test.com/data.csv", save_path)
        
        assert success == False
        assert not save_path.exists()
    
    @patch('src.scraper.scrape.requests.get')
    def test_download_file_timeout(self, mock_get, tmp_path):
        """Test download with timeout"""
        mock_get.side_effect = requests.exceptions.Timeout("Request timed out")
        
        save_path = tmp_path / "test.csv"
        success = download_file("http://test.com/data.csv", save_path)
        
        assert success == False
        assert not save_path.exists()
    
    def test_download_file_invalid_path(self):
        """Test download with invalid save path"""
        # Test with non-existent directory
        success = download_file("http://test.com/data.csv", "/non/existent/path/test.csv")
        assert success == False