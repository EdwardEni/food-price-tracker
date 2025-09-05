import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# Set page layout
st.set_page_config(page_title="Food Price Tracker Dashboard", layout="wide")

# Absolute path to forecasts folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "fpt", "forecasts")

# Load forecast CSV
forecast_file = next((f for f in os.listdir(DATA_DIR) if "30_day_forecast" in f), None)
if not (forecast_file and os.path.exists(os.path.join(DATA_DIR, forecast_file))):
    st.error("Forecast data not found in 'fpt/forecasts'. Please check your files.")
    st.stop()
forecast_df = pd.read_csv(os.path.join(DATA_DIR, forecast_file))

# Sidebar filters based on forecast data columns
st.sidebar.header("Filters")
admin_id = st.sidebar.selectbox("Select Admin ID", options=sorted(forecast_df['admin_id'].unique()))
mkt_id = st.sidebar.selectbox("Select Market ID", options=sorted(forecast_df['mkt_id'].unique()))
cm_id = st.sidebar.selectbox("Select Commodity ID", options=sorted(forecast_df['cm_id'].unique()))

# Filter forecast data based on selections
forecast_filtered = forecast_df[
    (forecast_df['admin_id'] == admin_id) &
    (forecast_df['mkt_id'] == mkt_id) &
    (forecast_df['cm_id'] == cm_id)
]

# Alert threshold input
alert_threshold = st.sidebar.number_input("Set Alert Threshold", min_value=0, value=100, step=1)

# Plot forecast plus confidence intervals
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=forecast_filtered['ds'],
    y=forecast_filtered['yhat'],
    mode='lines+markers',
    name='Forecast'
))
fig.add_trace(go.Scatter(
    x=list(forecast_filtered['ds']) + list(forecast_filtered['ds'][::-1]),
    y=list(forecast_filtered['yhat_upper']) + list(forecast_filtered['yhat_lower'][::-1]),
    fill='toself',
    fillcolor='rgba(0,100,80,0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    showlegend=False,
    name='Confidence Interval'
))
fig.add_hline(y=alert_threshold, line_dash="dash", line_color="red", annotation_text="Alert Threshold")
fig.update_layout(
    title="Price Forecast",
    xaxis_title="Date",
    yaxis_title="Price"
)

# Display plot in Streamlit app
st.plotly_chart(fig, use_container_width=True)
