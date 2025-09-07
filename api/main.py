from fastapi import FastAPI, Query, HTTPException
import joblib
import pandas as pd
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI(title="Food Price Forecast API")

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

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
                    print(f"Attempting to load: {fname}")
                    loaded_models[fname] = joblib.load(model_path)
                    print(f"✅ Successfully loaded model: {fname}")
                except Exception as e:
                    print(f"❌ Error loading model {fname}: {str(e)}")
                    # Continue with other models
    except Exception as e:
        print(f"❌ Error reading directory: {e}")
else:
    print(f"⚠️  Model directory not found: {MODEL_DIR}")

print(f"Total models loaded: {len(loaded_models)}")
print(f"Models loaded: {list(loaded_models.keys())}")

# Helper: Select model for product/region
def get_model(admin_id, mkt_id, cm_id):
    # Debug output
    print(f"get_model called with: admin_id={admin_id} ({type(admin_id)}), "
          f"mkt_id={mkt_id} ({type(mkt_id)}), cm_id={cm_id} ({type(cm_id)})")
    
    # The actual filename is: prophet_model_1.0__266__0.0.joblib
    # Convert parameters to match the filename format
    admin_str = str(admin_id)
    mkt_str = str(int(mkt_id))  # Convert to int first to remove .0 if float
    cm_str = str(cm_id)
    
    expected_key = f"prophet_model_{admin_str}__{mkt_str}__{cm_str}.joblib"
    print(f"Looking for model: {expected_key}")
    print(f"Available models: {list(loaded_models.keys())}")
    
    # Check if the exact key exists
    if expected_key in loaded_models:
        print(f"✅ Found model: {expected_key}")
        return loaded_models[expected_key]
    else:
        print(f"❌ Model not found: {expected_key}")
        return None

@app.get("/")
def index():
    return {"message": "Welcome to Food Price Forecast API", "models_loaded": len(loaded_models)}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is working", "models_loaded": len(loaded_models)}

@app.get("/test-model")
def test_model():
    try:
        model_key = "prophet_model_1.0__266__0.0.joblib"
        if model_key in loaded_models:
            model = loaded_models[model_key]
            # Simple test - create a future dataframe
            future = model.make_future_dataframe(periods=7, freq="D")
            print("✅ Model test passed - can create future dataframe")
            return {"status": "success", "message": "Model test passed"}
        else:
            return {"status": "error", "message": "Model not found"}
    except Exception as e:
        print(f"❌ Model test failed: {e}")
        return {"status": "error", "message": f"Model test failed: {str(e)}"}

@app.get("/forecast/")
def forecast(
    admin_id: float = Query(...),
    mkt_id: float = Query(...),
    cm_id: float = Query(...),
    periods: int = Query(30, ge=1, le=30)
):
    try:
        print(f"=== FORECAST REQUEST ===")
        print(f"admin_id: {admin_id} (type: {type(admin_id)})")
        print(f"mkt_id: {mkt_id} (type: {type(mkt_id)})") 
        print(f"cm_id: {cm_id} (type: {type(cm_id)})")
        
        model = get_model(admin_id, mkt_id, cm_id)
        if model is None:
            return {"error": "Model not found for given group", 
                    "requested": f"{admin_id}_{mkt_id}_{cm_id}",
                    "available": list(loaded_models.keys())}

        # Generate future dates, predict
        future = model.make_future_dataframe(periods=periods, freq="D")
        forecast_df = model.predict(future).tail(periods)

        # Filter to key columns for output
        result = forecast_df[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_dict(orient="records")
        
        print(f"✅ Forecast successful")
        return {
            "admin_id": admin_id,
            "mkt_id": mkt_id,
            "cm_id": cm_id,
            "forecast": result
        }
        
    except Exception as e:
        print(f"❌ Error in forecast: {e}")
        return {"error": f"Internal server error: {str(e)}"}