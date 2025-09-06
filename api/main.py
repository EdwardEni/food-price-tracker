from fastapi import FastAPI, Query, HTTPException
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
print(f"Models loaded: {list(loaded_models.keys())}")

# Helper: Select model for product/region
def get_model(admin_id, mkt_id, cm_id):
    # Convert all parameters to strings and remove .0 if needed
    admin_str = str(admin_id).rstrip('.0') if isinstance(admin_id, float) else str(admin_id)
    mkt_str = str(mkt_id).rstrip('.0') if isinstance(mkt_id, float) else str(mkt_id)
    cm_str = str(cm_id).rstrip('.0') if isinstance(cm_id, float) else str(cm_id)
    
    expected_key = f"prophet_model_{admin_str}__{mkt_str}__{cm_str}.joblib"
    print(f"Looking for model: {expected_key}")
    
    # Check if the exact key exists
    if expected_key in loaded_models:
        print(f"✅ Found exact model: {expected_key}")
        return loaded_models[expected_key]
    else:
        print(f"❌ Exact model not found: {expected_key}")
        print(f"Available models: {list(loaded_models.keys())}")
        return None

@app.get("/")
def index():
    return {"message": "Welcome to Food Price Forecast API", "models_loaded": len(loaded_models)}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is working", "models_loaded": len(loaded_models)}

@app.get("/forecast/")
def forecast(
    admin_id: float = Query(...),
    mkt_id: float = Query(...),
    cm_id: float = Query(...),
    periods: int = Query(30, ge=1, le=30)
):
    try:
        print(f"Forecast request: admin_id={admin_id}, mkt_id={mkt_id}, cm_id={cm_id}")
        
        model = get_model(admin_id, mkt_id, cm_id)
        if model is None:
            raise HTTPException(status_code=404, detail="Model not found for given group")

        # Generate future dates, predict
        future = model.make_future_dataframe(periods=periods, freq="D")
        forecast_df = model.predict(future).tail(periods)

        # Filter to key columns for output
        result = forecast_df[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_dict(orient="records")
        
        print(f"Forecast successful for {admin_id}_{mkt_id}_{cm_id}")
        return {
            "admin_id": admin_id,
            "mkt_id": mkt_id,
            "cm_id": cm_id,
            "forecast": result
        }
        
    except Exception as e:
        print(f"Error in forecast endpoint: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")