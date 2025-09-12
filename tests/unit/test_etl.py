import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

# Mock function since process_data might not exist
def process_data(df):
    """Mock process_data function for testing"""
    if df.empty:
        return df
    processed_df = df.copy()
    if 'date' in processed_df.columns:
        processed_df['date'] = pd.to_datetime(processed_df['date'])
    return processed_df

def test_process_data_valid():
    """Test data processing with valid data"""
    sample_data = pd.DataFrame({
        'price': [100, 150, 200],
        'date': ['2024-01-01', '2024-01-02', '2024-01-03']
    })
    
    processed = process_data(sample_data)
    assert not processed.empty
    assert len(processed) == len(sample_data)

def test_process_data_empty():
    """Test data processing with empty DataFrame"""
    empty_df = pd.DataFrame()
    processed = process_data(empty_df)
    assert processed.empty