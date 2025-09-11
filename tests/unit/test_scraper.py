import pytest
from unittest.mock import patch, Mock
import requests
from src.scraper.scrape import download_file

class TestScraper:
    
    @patch('src.scraper.scrape.requests.get')
    def test_download_file_success(self, mock_get, tmp_path):
        """Test successful file download"""
        # Mock response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.iter_content.return_value = [b'test', b'data']
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
        mock_get.return_value = mock_response
        
        save_path = tmp_path / "test.csv"
        success = download_file("http://test.com/data.csv", save_path)
        
        assert success == False
        assert not save_path.exists()
