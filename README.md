# Food Price Tracker & Forecasting Dashboard

A real-time food price monitoring system with predictive analytics and automated alerts.

![Dashboard Screenshot](screenshots/dashboard.png)

## Features

- **Real-time Data Collection**: Automated web scraping of food price data
- **Predictive Analytics**: Prophet-based price forecasting
- **Interactive Dashboard**: Streamlit-based visualization
- **REST API**: FastAPI backend for forecast access
- **Price Alert System**: Email notifications for price spikes
- **Dockerized Deployment**: Easy container-based deployment

## Quick Start

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Git

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/EdwardEni/food-price-tracker.git
   cd food-price-tracker




Set up virtual environment:

python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows   

Install dependencies:

pip install -r requirements.txt



Run the application:

# Start all services
docker-compose up --build

# Or run individually
python src/scraper/scrape.py  # Run scraper
streamlit run dashboard/app.py  # Run dashboard



Access the services:

Dashboard: http://localhost:8501

API: http://localhost:8000

API Docs: http://localhost:8000/docs


Running Tests

# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test category
pytest tests/unit/  # Unit tests
pytest tests/integration/  # Integration tests



Project Structure
text
food-price-tracker/
├── api/                 # FastAPI backend
├── dashboard/           # Streamlit dashboard
├── data/               # Data storage
├── fpt/                # Forecasts and models
├── notebooks/          # Exploratory analysis
├── src/               # Source code
│   ├── alerts/        # Alert system
│   ├── etl/           # Data processing
│   └── scraper/       # Data collection
├── tests/             # Test suite
└── docker-compose.yml # Container orchestration



API Documentation
Endpoints
GET / - Welcome message

GET /health - Service health check

GET /forecast/ - Get price forecasts

Parameters: admin_id, mkt_id, cm_id



Example Usage
bash
# Get forecast for specific product
curl "http://localhost:8000/forecast/?admin_id=1.0&mkt_id=266&cm_id=0.0"

# Health check
curl http://localhost:8000/health



Deployment
Render Deployment
Connect your GitHub repository to Render

Services will auto-deploy on push to main

Environment variables are set in Render dashboard



Environment Variables
bash
API_URL=http://localhost:8000
DATABASE_URL=postgresql://user:pass@host:port/db
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=alerts@foodpricetracker.com
ALERT_EMAIL=admin@yourcompany.com
PRICE_SPIKE_THRESHOLD=25


Alert System
The system includes automated price spike detection and email alerts:

Threshold-based alerts: Configurable percentage increase threshold

SMTP integration: Supports Gmail and other email providers

Real-time monitoring: Alerts triggered during forecast generation



Contributing
Fork the repository

Create a feature branch

Add tests for new functionality

Submit a pull request


License
MIT License - see LICENSE file for details

Support
For support, please open an issue or contact semekray@yahoo.com


Real-Time Local Food Price Tracker & Forecasting Dashboard
A Python-based project to track and forecast local food prices in real-time using web scraping, time-series analysis, and visualization.

Project Overview
This project aims to scrape local food prices daily, store data in PostgreSQL, perform ETL and exploratory data analysis, forecast prices using Prophet or ARIMA, and display results via a Streamlit dashboard. It includes automated deployment and a REST API for forecast access.

Setup
Clone the repository:

bash
git clone https://github.com/EdwardEni/food-price-tracker.git
cd food-price-tracker
Create and activate a Python virtual environment:

bash
python -m venv venv
source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows
Install dependencies:

bash
pip install -r requirements.txt
Usage
Run the scraper:

bash
python src/scraper.py
Run data processing:

bash
python src/etl.py
Launch the dashboard:

bash
streamlit run src/dashboard.py
Access forecasts via REST API: available at /api/forecast

Folder Structure
data/ — Store raw and processed data files

src/ — Source code for scraping, ETL, modeling, and dashboard

notebooks/ — Exploratory data analysis and prototypes

tests/ — Unit and integration tests

Contact
Author: Edward
Email: semekray@yahoo.com
GitHub: EdwardEni