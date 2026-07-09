# Employee Attrition Prediction: End-to-End ML System

This project contains an end-to-end Machine Learning pipeline to predict employee attrition risk, using the IBM HR Analytics Employee Attrition dataset. It includes data preprocessing, class imbalance handling (SMOTE), hyperparameter-tuned model training, a **FastAPI** backend REST API, and a premium **Streamlit** dashboard frontend.

---

## Project Structure

```
ideas-eap/
├── ideas/                                            # Virtual environment (venv)
├── data/
│   └── WA_Fn-UseC_-HR-Employee-Attrition.csv         # Raw dataset
├── models/
│   ├── preprocessor.joblib                           # Fitted scaling & encoding ColumnTransformer
│   └── best_model.pkl                                # Best selected model (joblib serialization)
├── src/
│   ├── __init__.py
│   ├── config.py                                     # Central config (paths, features, exclusions)
│   ├── preprocessing.py                              # Loading, encoding targets, and scaling pipelines
│   ├── train.py                                      # Local experiment loops, SMOTE, and model selection
│   └── predict.py                                    # Inference wrapper and risk-factor extractor
├── backend/
│   ├── __init__.py
│   ├── main.py                                       # FastAPI server endpoints
│   └── schemas.py                                    # Pydantic validation models
├── frontend/
│   └── app.py                                        # Premium Streamlit web app
├── .gitignore                                        # Standard git ignore definitions
├── requirements.txt                                  # Dependency declarations
└── run.py                                            # Central script execution manager
```

---

## Setup & Running the Services

The project uses the `ideas` virtual environment. A centralized wrapper script `run.py` is provided in the project root to run any step using the correct environment.

### 1. Train the Models
Run the training pipeline. This will load the raw data, build and fit the preprocessor pipeline, apply SMOTE to balance classes, run training for Tuned Logistic Regression, Tuned XGBoost, and Random Forest, compare performance, and save the best model assets locally under `models/`.
```bash
python run.py train
```

### 2. Start the FastAPI Backend
Start the backend web server to expose inference API endpoints:
```bash
python run.py backend
```
The REST API will be available at **`http://localhost:8000`**. You can access interactive Swagger documentation and test the endpoints at **`http://localhost:8000/docs`**.

### 3. Launch the Streamlit Frontend
Launch the human resources dashboard:
```bash
python run.py frontend
```
The dashboard will open automatically in your browser at **`http://localhost:8501`**.

> **Note on Fallback Mode**: The Streamlit frontend has an automatic API fallback. If the FastAPI backend is offline, it will import the inference code directly and run predictions locally.

---

## Model Details & Preprocessing

* **Target Variable**: `Attrition` (encoded as `Yes` -> 1, `No` -> 0).
* **Excluded Columns**: Constant features (`EmployeeCount`, `StandardHours`, `Over18`) and identifiers (`EmployeeNumber`) are dropped.
* **Categorical Encoding**: One-Hot Encoding with `drop='first'` to prevent multi-collinearity.
* **Numerical Scaling**: Standard scaling applied to all numeric and ordinal rating features.
* **Imbalance Treatment**: SMOTE (Synthetic Minority Over-sampling Technique) is applied only to the training split.
* **Primary Evaluated Model**: Tuned Logistic Regression (selected as the best model due to its high F1-Score of `0.50` and Recall of `0.70` for the minority class in the test split).
