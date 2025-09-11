import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import logging

logger = logging.getLogger("email_alerts")

class EmailAlert:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_username = os.getenv('SMTP_USERNAME')
        self.smtp_password = os.getenv('SMTP_PASSWORD')
        self.from_email = os.getenv('FROM_EMAIL', 'alerts@foodpricetracker.com')
        
    def send_alert(self, to_email, subject, message):
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(message, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
                
            logger.info(f"Alert email sent to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
            return False

# Example usage
def send_alert(product_id, current_price, percent_change, forecast_date):
    emailer = EmailAlert()
    
    subject = f"🚨 Price Spike Alert: {product_id}"
    message = f"""
    <h2>Price Spike Detected!</h2>
    <p><strong>Product:</strong> {product_id}</p>
    <p><strong>Current Price:</strong> ${current_price:.2f}</p>
    <p><strong>Price Increase:</strong> {percent_change:.2f}%</p>
    <p><strong>Forecast Date:</strong> {forecast_date}</p>
    <p>This may indicate a significant market change.</p>
    """
    
    # Send to admin email (you can make this configurable)
    admin_email = os.getenv('ALERT_EMAIL', 'your-email@example.com')
    emailer.send_alert(admin_email, subject, message)
