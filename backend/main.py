from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from backend.schemas import EmployeeFeatures, PredictionResponse
from src.predict import InferenceEngine

app = FastAPI(
    title="Employee Attrition Prediction API",
    description="Backend service for predicting the probability of an employee leaving the organization.",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global inference engine instance
try:
    engine = InferenceEngine()
except Exception:
    engine = None


@app.get("/")
def home():
    return {
        "message": "Welcome to the Employee Attrition Prediction API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "home": "/",
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }


@app.get("/health", status_code=status.HTTP_200_OK)
def health_check():
    """Health check endpoint to ensure API and model are available."""
    if engine is None or engine.model is None or engine.preprocessor is None:
        return {
            "status": "warning",
            "message": "API is healthy but ML model assets are missing. Please run model training."
        }
    return {
        "status": "healthy",
        "message": "Inference engine is online and model assets are loaded."
    }


@app.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
def predict_attrition(employee: EmployeeFeatures):
    """
    Predicts attrition probability and risk level for a single employee.
    """
    global engine

    if engine is None or engine.model is None:
        try:
            engine = InferenceEngine()
        except Exception:
            pass

    if engine is None or engine.model is None or engine.preprocessor is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Model files are missing. Please run src/train.py to train and save the model."
        )

    try:
        raw_dict = employee.model_dump()
        result = engine.predict(raw_dict)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference error: {str(e)}"
        )