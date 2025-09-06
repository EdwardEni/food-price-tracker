import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
import requests

# Set page layout
st.set_page_config(page_title="Food Price Tracker Dashboard", layout="wide")

st.title("Food Price Tracker Dashboard")

# Test API connection
try:
    response = requests.get("http://api:8000/", timeout=5)
    if response.status_code == 200:
        st.success("✅ Connected to API")
    else:
        st.error(f"❌ API connection failed: {response.status_code}")
except requests.exceptions.RequestException as e:
    st.error(f"❌ Cannot connect to API: {e}")


# Use the mounted volume path directly
DATA_DIR = "fpt/forecasts"

if not os.path.exists(DATA_DIR):
    st.warning("📁 Forecasts directory not found. Running scraper will create data.")
    st.write("Please run the scraper to generate forecast data.")
    
    # Create sample data for demonstration
    sample_dates = pd.date_range(start='2024-01-01', periods=30, freq='D')
    sample_data = pd.DataFrame({
        'ds': sample_dates,
        'yhat': [100 + i*2 for i in range(30)],
        'yhat_lower': [90 + i*2 for i in range(30)],
        'yhat_upper': [110 + i*2 for i in range(30)],
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
    
    # Load and display actual forecast data
    try:
        # Find the latest forecast file
        import glob
        csv_files = glob.glob(os.path.join(DATA_DIR, "*forecast*.csv"))
        if csv_files:
            latest_file = sorted(csv_files)[-1]
            forecast_df = pd.read_csv(latest_file)
            
            st.write("### Latest Forecast Data")
            st.dataframe(forecast_df.head())
            
            # Create forecast plot
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['yhat'],
                                   mode='lines+markers', name='Forecast', line=dict(color='blue')))
            fig.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['yhat_lower'],
                                   fill=None, mode='lines', name='Lower Bound', line=dict(color='lightblue')))
            fig.add_trace(go.Scatter(x=forecast_df['ds'], y=forecast_df['yhat_upper'],
                                   fill='tonexty', mode='lines', name='Upper Bound', line=dict(color='lightblue')))
            
            fig.update_layout(
                title="Food Price Forecast with Confidence Interval",
                xaxis_title="Date",
                yaxis_title="Price",
                hovermode='x unified'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No forecast files found in the directory")
    except Exception as e:
        st.error(f"Error loading forecast data: {e}")