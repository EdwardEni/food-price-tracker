import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import requests
from urllib.parse import urljoin
import glob
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("/app/logs/dashboard.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("dashboard")

# Set page layout
st.set_page_config(page_title="Food Price Tracker Dashboard", layout="wide")

st.title("Food Price Tracker Dashboard")

# Get API URL from environment variable or use default
API_URL = os.getenv('API_URL', 'http://localhost:8000')
logger.info(f"Using API URL: {API_URL}")

# Test API connection with better error handling
try:
    logger.info(f"Testing API connection to {API_URL}")
    response = requests.get(f"{API_URL}/", timeout=5)
    if response.status_code == 200:
        st.success(f"✅ Connected to API: {API_URL}")
        logger.info(f"API connection successful: {response.status_code}")
    elif response.status_code == 429:
        st.warning("⚠️ API rate limit exceeded. Please wait a moment.")
        logger.warning("API rate limit exceeded")
    else:
        st.error(f"❌ API connection failed: {response.status_code}")
        logger.error(f"API connection failed with status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    st.warning(f"⚠️ API connection issue: {e}")
    logger.error(f"API connection exception: {e}")

# Use the correct path for forecasts
DATA_DIR = "/app/fpt/forecasts"
logger.info(f"Checking forecast data directory: {DATA_DIR}")

if not os.path.exists(DATA_DIR):
    st.warning("📁 Forecasts directory not found. Forecast data will appear here once generated.")
    logger.warning(f"Forecast directory not found: {DATA_DIR}")
    
    # Create the directory if it doesn't exist
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        st.info("📁 Created forecasts directory")
        logger.info(f"Created forecast directory: {DATA_DIR}")
    except Exception as e:
        st.error(f"❌ Could not create forecasts directory: {e}")
        logger.error(f"Failed to create forecast directory: {e}")
    
    # Create sample data for demonstration
    logger.info("Generating sample forecast data for demonstration")
    sample_dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    sample_data = pd.DataFrame({
        'ds': sample_dates,
        'yhat': [100 + i * 2 for i in range(30)],
        'yhat_lower': [90 + i * 2 for i in range(30)],
        'yhat_upper': [110 + i * 2 for i in range(30)],
        'admin_id': [1] * 30,
        'mkt_id': [266] * 30,
        'cm_id': [0] * 30
    })
    
    st.write("### Sample Forecast Data (Demo)")
    st.dataframe(sample_data.head())
    
    # Create sample plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sample_data['ds'], y=sample_data['yhat'], 
                             mode='lines+markers', name='Forecast'))
    fig.update_layout(title="Sample Price Forecast", xaxis_title="Date", yaxis_title="Price")
    st.plotly_chart(fig, use_container_width=True)
    logger.info("Displayed sample forecast data and chart")

else:
    st.success("✅ Forecast data directory found")
    logger.info(f"Forecast directory found: {DATA_DIR}")
    
    # Load and display actual forecast data with error handling
    try:
        # Find the latest forecast file
        logger.info("Searching for forecast files")
        csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv') and 'forecast' in f.lower()]
        logger.info(f"Found {len(csv_files)} forecast files: {csv_files}")
        
        if csv_files:
            latest_file = sorted(csv_files)[-1]
            file_path = os.path.join(DATA_DIR, latest_file)
            logger.info(f"Loading latest forecast file: {latest_file}")
            
            forecast_df = pd.read_csv(file_path)
            logger.info(f"Loaded forecast data with shape: {forecast_df.shape}")
            
            st.write(f"### Latest Forecast Data ({latest_file})")
            st.dataframe(forecast_df.head())
            
            # Check what columns we have and adapt accordingly
            logger.info(f"Available columns: {list(forecast_df.columns)}")
            st.write("#### Available Columns:")
            st.write(list(forecast_df.columns))
            
            # Try to create a plot with available data
            if 'ds' in forecast_df.columns and 'yhat' in forecast_df.columns:
                logger.info("Creating Prophet-style forecast visualization")
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['yhat'],
                                       mode='lines+markers', name='Forecast', line=dict(color='blue')))
                if 'yhat_lower' in forecast_df.columns and 'yhat_upper' in forecast_df.columns:
                    fig.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['yhat_lower'],
                                           fill=None, mode='lines', name='Lower Bound', line=dict(color='lightblue')))
                    fig.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['yhat_upper'],
                                           fill='tonexty', mode='lines', name='Upper Bound', line=dict(color='lightblue')))
                
                fig.update_layout(
                    title="Food Price Forecast",
                    xaxis_title="Date",
                    yaxis_title="Price",
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
                logger.info("Displayed Prophet forecast chart")
                
            elif 'persistence_forecast' in forecast_df.columns or 'moving_average_forecast' in forecast_df.columns:
                logger.info("Creating baseline forecast visualization")
                st.info("📊 Baseline forecast data loaded")
                if 'persistence_forecast' in forecast_df.columns:
                    st.metric("Persistence Forecast", f"${forecast_df['persistence_forecast'].iloc[0]:.2f}")
                if 'moving_average_forecast' in forecast_df.columns:
                    st.metric("Moving Average Forecast", f"${forecast_df['moving_average_forecast'].iloc[0]:.2f}")
                logger.info("Displayed baseline forecast metrics")
                
            else:
                st.warning("📋 Unknown forecast format. Showing raw data.")
                logger.warning(f"Unknown forecast format. Columns: {list(forecast_df.columns)}")
                st.dataframe(forecast_df)
                
        else:
            st.info("📊 No forecast files found. Run the forecast generator to create data.")
            logger.info("No forecast files found in directory")
            
    except Exception as e:
        error_msg = f"Error loading forecast data: {e}"
        st.error(f"❌ {error_msg}")
        logger.error(error_msg, exc_info=True)
        
        # Show available files for debugging
        if 'DATA_DIR' in locals():
            try:
                files = os.listdir(DATA_DIR)
                st.write("📁 Files in forecast directory:", files)
                logger.info(f"Files in forecast directory: {files}")
            except Exception as dir_error:
                logger.error(f"Error listing directory contents: {dir_error}")

# Add footer with timestamp
st.markdown("---")
st.caption(f"Dashboard last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
logger.info("Dashboard rendering completed")