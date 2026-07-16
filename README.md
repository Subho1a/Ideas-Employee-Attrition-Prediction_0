# Employee Attrition Prediction: End-to-End ML System

This project contains an end-to-end Machine Learning pipeline to predict employee attrition risk, using the IBM HR Analytics Employee Attrition dataset. It includes data preprocessing, class imbalance handling (SMOTE), hyperparameter-tuned model training, a **FastAPI** backend REST API, and a premium **Streamlit** dashboard frontend.

---
![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-ML-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)
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

```
---

## 🚀 Live Demo

### 🌐 Streamlit Frontend
https://employee-attrition-prediction0.streamlit.app/

### ⚡ FastAPI Backend
https://employee-attrition-prediction-aabn.onrender.com/

### 📖 API Documentation
https://employee-attrition-prediction-aabn.onrender.com/docs

---

## Setup & Running the Services for local

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Subho1a/Ideas-Employee-Attrition-Prediction_0
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn backend.main:app --reload
```

Run Streamlit

```bash
streamlit run frontend/app.py
```

---
