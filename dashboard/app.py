import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import requests
from urllib.parse import urljoin
import glob

# Set page layout
st.set_page_config(page_title="Food Price Tracker Dashboard", layout="wide")

st.title("Food Price Tracker Dashboard")

# Get API URL from environment variable or use default
API_URL = os.getenv('API_URL', 'http://localhost:8000')

# Test API connection with better error handling
try:
    response = requests.get(f"{API_URL}/", timeout=5)
    if response.status_code == 200:
        st.success(f"✅ Connected to API: {API_URL}")
    elif response.status_code == 429:
        st.warning("⚠️ API rate limit exceeded. Please wait a moment.")
    else:
        st.error(f"❌ API connection failed: {response.status_code}")
except requests.exceptions.RequestException as e:
    st.warning(f"⚠️ API connection issue: {e}")

# Use the correct path for forecasts
DATA_DIR = "/app/fpt/forecasts"

if not os.path.exists(DATA_DIR):
    st.warning("📁 Forecasts directory not found. Forecast data will appear here once generated.")
    
    # Create the directory if it doesn't exist
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        st.info("📁 Created forecasts directory")
    except Exception as e:
        st.error(f"❌ Could not create forecasts directory: {e}")
    
    # Create sample data for demonstration
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

else:
    st.success("✅ Forecast data directory found")
    
    # Load and display actual forecast data with error handling
    try:
        # Find the latest forecast file
        csv_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv') and 'forecast' in f.lower()]
        if csv_files:
            latest_file = sorted(csv_files)[-1]
            file_path = os.path.join(DATA_DIR, latest_file)
            forecast_df = pd.read_csv(file_path)
            
            st.write(f"### Latest Forecast Data ({latest_file})")
            st.dataframe(forecast_df.head())
            
            # Check what columns we have and adapt accordingly
            st.write("#### Available Columns:")
            st.write(list(forecast_df.columns))
            
            # Try to create a plot with available data
            if 'ds' in forecast_df.columns and 'yhat' in forecast_df.columns:
                # This is a Prophet-style forecast file
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
                
            elif 'persistence_forecast' in forecast_df.columns or 'moving_average_forecast' in forecast_df.columns:
                # This is a baseline forecast file - show different visualization
                st.info("📊 Baseline forecast data loaded")
                st.metric("Persistence Forecast", f"${forecast_df['persistence_forecast'].iloc[0]:.2f}")
                st.metric("Moving Average Forecast", f"${forecast_df['moving_average_forecast'].iloc[0]:.2f}")
                
            else:
                st.warning("📋 Unknown forecast format. Showing raw data.")
                st.dataframe(forecast_df)
                
        else:
            st.info("📊 No forecast files found. Run the forecast generator to create data.")
            
    except Exception as e:
        st.error(f"❌ Error loading forecast data: {e}")
        # Show available files for debugging
        if 'DATA_DIR' in locals():
            try:
                files = os.listdir(DATA_DIR)
                st.write("📁 Files in forecast directory:", files)
            except:
                pass