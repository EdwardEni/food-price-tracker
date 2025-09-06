from fastapi import FastAPI, Query
import joblib
import pandas as pd
import os

app = FastAPI(title="Food Price Forecast API")

# Set base directory to project root (food-price-tracker)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Absolute path to models folder inside fpt/
MODEL_DIR = "/fpt/models"

# Load all Prophet models at startup
loaded_models = {}

print(f"Looking for models in: {MODEL_DIR}")
print(f"Directory exists: {os.path.exists(MODEL_DIR)}")

if os.path.exists(MODEL_DIR):
    print(f"Loading models from {MODEL_DIR}")
    try:
        files = os.listdir(MODEL_DIR)
        print(f"Files in directory: {files}")
        
        for fname in files:
            if fname.endswith(".joblib"):
                try:
                    model_path = os.path.join(MODEL_DIR, fname)
                    loaded_models[fname] = joblib.load(model_path)
                    print(f"✅ Loaded model: {fname}")
                except Exception as e:
                    print(f"❌ Error loading model {fname}: {e}")
    except Exception as e:
        print(f"❌ Error reading directory: {e}")
else:
    print(f"⚠️  Model directory not found: {MODEL_DIR}")

print(f"Total models loaded: {len(loaded_models)}")

# Helper: Select model for product/region
def get_model(admin_id, mkt_id, cm_id):
    key = f"prophet_model_{admin_id}_{mkt_id}_{cm_id}.joblib"
    return loaded_models.get(key)

@app.get("/")
def index():
    return {"message": "Welcome to Food Price Forecast API"}

@app.get("/forecast/")
def forecast(
    admin_id: int = Query(...),
    mkt_id: int = Query(...),
    cm_id: int = Query(...),
    periods: int = Query(30, ge=1, le=30)
):
    model = get_model(admin_id, mkt_id, cm_id)
    if model is None:
        return {"error": "Model not found for given group"}

    # Generate future dates, predict
    future = model.make_future_dataframe(periods=periods, freq="D")
    forecast_df = model.predict(future).tail(periods)

    # Filter to key columns for output
    result = forecast_df[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_dict(orient="records")
    return {
        "admin_id": admin_id,
        "mkt_id": mkt_id,
        "cm_id": cm_id,
        "forecast": result
    }