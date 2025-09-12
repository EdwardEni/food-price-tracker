import pytest
import pandas as pd
import tempfile
import os
# Add this to the top of each test file
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

@pytest.fixture
def sample_price_data():
    """Sample price data for testing"""
    return pd.DataFrame({
        'admin_id': [1.0, 1.0, 1.0],
        'mkt_id': [266, 266, 266],
        'cm_id': [0.0, 0.0, 0.0],
        'price': [100, 105, 110],
        'date': ['2024-01-01', '2024-01-02', '2024-01-03']
    })

@pytest.fixture
def temp_csv_file(sample_price_data):
    """Create temporary CSV file for testing"""
    with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
        sample_price_data.to_csv(tmp.name, index=False)
        yield tmp.name
    os.unlink(tmp.name)
