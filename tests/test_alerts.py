import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.alerts.price_alert import PriceAlert
from src.alerts.email_alert import EmailAlert

def test_price_spike_detection():
    alert_system = PriceAlert(threshold_percent=20)
    
    # Test spike detection
    historical = [100, 105, 95, 110, 100]
    current = 150  # 50% increase
    
    is_spike, percent = alert_system.detect_spike(current, historical)
    print(f"Spike detected: {is_spike}, Change: {percent:.2f}%")
    
    # Test normal price
    current_normal = 115  # 15% increase
    is_spike, percent = alert_system.detect_spike(current_normal, historical)
    print(f"Spike detected: {is_spike}, Change: {percent:.2f}%")

if __name__ == "__main__":
    test_price_spike_detection()
