import pytest
import pandas as pd
import numpy as np

def test_basic_math():
    """Basic test that should always pass"""
    assert 1 + 1 == 2

def test_dataframe_creation():
    """Test pandas functionality"""
    df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
    assert len(df) == 2
    assert list(df.columns) == ['a', 'b']

def test_numpy_operations():
    """Test numpy functionality"""
    arr = np.array([1, 2, 3])
    assert arr.sum() == 6
