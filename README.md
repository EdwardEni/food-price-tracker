# Real-Time Local Food Price Tracker & Forecasting Dashboard
A Python-based project to track and forecast local food prices in real-time using web scraping, time-series analysis, and visualization.

## Project Overview

This project aims to scrape local food prices daily, store data in PostgreSQL, perform ETL and exploratory data analysis, forecast prices using Prophet or ARIMA, and display results via a Streamlit dashboard. It includes automated deployment and a REST API for forecast access.

## Setup

1. Clone the repository:
git clone https://github.com/EdwardEni/food-price-tracker.git
cd food-price-tracker


2. Create and activate a Python virtual environment:

python -m venv venv
source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows


3. Install dependencies:

pip install -r requirements.txt


## Usage

- Run the scraper:
python src/scraper.py


- Run data processing:
python src/etl.py


- Launch the dashboard:
streamlit run src/dashboard.py

- Access forecasts via REST API: available at `/api/forecast`

## Folder Structure

- `data/` — Store raw and processed data files  
- `src/` — Source code for scraping, ETL, modeling, and dashboard  
- `notebooks/` — Exploratory data analysis and prototypes  
- `tests/` — Unit and integration tests  

## Contact

Author: Edward Eniang 
Email: semekray@yahoo.com  
GitHub: [EdwardEni](https://github.com/EdwardEni)
