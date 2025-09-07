import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import joblib
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = FastAPI(title="Food Price Forecast API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace "*" with your dashboard URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Models directory path
MODEL_DIR = "/fpt/models"

def check_models_directory():
    if not os.path.exists(MODEL_DIR):
        print(f"⚠️ Warning: Model directory not found, creating: {MODEL_DIR}")
        os.makedirs(MODEL_DIR, exist_ok=True)
        return False
    return True

# Load Prophet models at startup
loaded_models = {}
print(f"Looking for models in: {MODEL_DIR}")

if check_models_directory():
    try:
        files = os.listdir(MODEL_DIR)
        print(f"Files in model directory: {files}")
        for fname in files:
            if fname.endswith(".joblib"):
                try:
                    model_path = os.path.join(MODEL_DIR, fname)
                    print(f"Loading model: {fname}")
                    loaded_models[fname] = joblib.load(model_path)
                    print(f"✅ Loaded model: {fname}")
                except Exception as e:
                    print(f"❌ Failed to load model {fname}: {e}")
    except Exception as e:
        print(f"❌ Error accessing models directory: {e}")
else:
    print(f"⚠️ Model directory not found and was created: {MODEL_DIR}")

print(f"Total models loaded: {len(loaded_models)}")
print(f"Models loaded: {list(loaded_models.keys())}")

def get_model(admin_id, mkt_id, cm_id):
    print(f"get_model called with admin_id={admin_id} ({type(admin_id)}), mkt_id={mkt_id} ({type(mkt_id)}), cm_id={cm_id} ({type(cm_id)})")
    admin_str = str(admin_id)
    mkt_str = str(int(mkt_id))
    cm_str = str(cm_id)
    expected_key = f"prophet_model_{admin_str}__{mkt_str}__{cm_str}.joblib"
    print(f"Looking for model: {expected_key}")
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
    models_dir_exists = check_models_directory()
    return {
        "status": "healthy",
        "message": "API is working",
        "models_dir_exists": models_dir_exists,
        "models_loaded": len(loaded_models),
    }

@app.get("/test-model")
def test_model():
    try:
        model_key = "prophet_model_1.0__266__0.0.joblib"
        if model_key in loaded_models:
            model = loaded_models[model_key]
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
        print(f"admin_id: {admin_id}, mkt_id: {mkt_id}, cm_id: {cm_id}")

        model = get_model(admin_id, mkt_id, cm_id)
        if model is None:
            return {
                "error": "Model not found for given group",
                "requested": f"{admin_id}_{mkt_id}_{cm_id}",
                "available": list(loaded_models.keys())
            }

        future = model.make_future_dataframe(periods=periods, freq="D")
        forecast_df = model.predict(future).tail(periods)

        result = forecast_df[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_dict(orient="records")

        print("✅ Forecast successful")
        return {
            "admin_id": admin_id,
            "mkt_id": mkt_id,
            "cm_id": cm_id,
            "forecast": result
        }

    except Exception as e:
        print(f"❌ Error in forecast: {e}")
        return {"error": f"Internal server error: {str(e)}"}
