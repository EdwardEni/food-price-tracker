import pytest
import pandas as pd
from src.alerts.price_alert import PriceAlert

class TestPriceAlert:
    
    def test_detect_spike_positive(self):
        """Test spike detection with positive case"""
        alert = PriceAlert(threshold_percent=20)
        historical = [100, 105, 95, 110, 100]  # avg = 102
        current = 150  # ~47% increase
        
        is_spike, percent = alert.detect_spike(current, historical)
        
        assert is_spike == True
        assert percent > 40
    
    def test_detect_spike_negative(self):
        """Test no spike detection"""
        alert = PriceAlert(threshold_percent=20)
        historical = [100, 105, 95, 110, 100]
        current = 115  # ~13% increase
        
        is_spike, percent = alert.detect_spike(current, historical)
        
        assert is_spike == False
        assert percent < 20
    
    def test_detect_spike_insufficient_data(self):
        """Test with insufficient historical data"""
        alert = PriceAlert()
        is_spike, percent = alert.detect_spike(100, [])
        
        assert is_spike == False
        assert percent == 0
