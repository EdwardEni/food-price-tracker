def test_basic_math():
    assert 1 + 1 == 2

def test_imports():
    try:
        import pandas
        import numpy
        import requests
        assert True
    except ImportError:
        assert False
