import pytest
import pandas as pd
from src.etl.load_to_db import process_data  # Adjust based on your actual function

class TestETL:
    
    def test_process_data_valid(self, sample_price_data):
        """Test data processing with valid data"""
        processed = process_data(sample_price_data)
        
        assert not processed.empty
        assert 'price' in processed.columns
        assert 'date' in processed.columns
        assert processed['price'].dtype in ['float64', 'int64']
    
    def test_process_data_empty(self):
        """Test data processing with empty DataFrame"""
        empty_df = pd.DataFrame()
        processed = process_data(empty_df)
        
        assert processed.empty
    
    def test_process_data_missing_columns(self):
        """Test data processing with missing required columns"""
        incomplete_df = pd.DataFrame({'price': [100, 200]})
        
        with pytest.raises(ValueError):
            process_data(incomplete_df)
