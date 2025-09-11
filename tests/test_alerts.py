import sys
import os
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.alerts.price_alert import PriceAlert

def test_price_spike_detection():
    alert_system = PriceAlert(threshold_percent=20)
    
    # Test 1: Clear spike detection (50% increase) - need at least 7 data points
    historical = [100, 105, 95, 110, 100, 98, 102]  # 7 points, Average = 101.43
    current = 150  # 48% increase from average
    
    is_spike, percent = alert_system.detect_spike(current, historical)
    print(f"Test 1 - Spike: {is_spike}, Change: {percent:.2f}%")
    assert is_spike == True, f"Expected True, got {is_spike} for 48% increase"
    assert percent > 40, f"Expected >40%, got {percent}%"
    
    # Test 2: Normal price (15% increase - below threshold)
    current_normal = 117  # 15% increase from average (101.43 * 1.15 = 116.64)
    is_spike, percent = alert_system.detect_spike(current_normal, historical)
    print(f"Test 2 - Spike: {is_spike}, Change: {percent:.2f}%")
    assert is_spike == False, f"Expected False, got {is_spike} for 15% increase"
    assert 10 < percent < 20, f"Expected 10-20%, got {percent}%"
    
    print("✅ Spike detection tests passed!")

def test_edge_cases():
    alert_system = PriceAlert(threshold_percent=20)
    
    # Test with empty historical data
    is_spike, percent = alert_system.detect_spike(100, [])
    print(f"Empty data - Spike: {is_spike}, Change: {percent}%")
    assert is_spike == False
    assert percent == 0
    
    # Test with insufficient data (less than 7 points)
    is_spike, percent = alert_system.detect_spike(100, [100, 105, 95])
    print(f"Insufficient data - Spike: {is_spike}, Change: {percent}%")
    assert is_spike == False
    assert percent == 0
    
    # Test with zero average price (edge case protection)
    is_spike, percent = alert_system.detect_spike(100, [0, 0, 0, 0, 0, 0, 0])
    print(f"Zero average - Spike: {is_spike}, Change: {percent}%")
    assert is_spike == False, f"Expected False for zero average, got {is_spike}"
    assert percent == 0, f"Expected 0% change for zero average, got {percent}%"
    
    print("✅ Edge case tests passed!")

if __name__ == "__main__":
    try:
        test_price_spike_detection()
        test_edge_cases()
        print("🎉 All tests passed! ✅")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        # Debug: Let's see what the actual calculation is
        alert_system = PriceAlert(threshold_percent=20)
        historical = [100, 105, 95, 110, 100, 98, 102]  # 7 points
        current = 150
        avg = np.mean(historical)
        change = ((current - avg) / avg) * 100
        print(f"Debug: Historical={historical}")
        print(f"Debug: Avg={avg:.2f}, Current={current}, Change={change:.2f}%")
        print(f"Debug: Length check: {len(historical)} >= 7? {len(historical) >= 7}")