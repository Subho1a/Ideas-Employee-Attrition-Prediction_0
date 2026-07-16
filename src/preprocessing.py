import sys
from pathlib import Path

import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import config

def load_and_preprocess(filepath: str):
    """
    Loads raw CSV data and binarizes target variable.
    
    Args:
        filepath: Path to the raw CSV file.
        
    Returns:
        df: Processed DataFrame
        X_raw: Features DataFrame
        y: Target Series
    """
    df = pd.read_csv(filepath)
    
    # Encode target column: Yes = 1, No = 0
    df[config.TARGET] = df["Attrition"].apply(lambda x: 1 if str(x).strip().lower() == "yes" else 0)
    
    # Target series
    y = df[config.TARGET]
    
    # Features (drop uninformative features, target column, and intermediate numeric target)
    cols_to_drop = [col for col in config.DROP_COLUMNS if col in df.columns]
    if config.TARGET in df.columns:
        cols_to_drop.append(config.TARGET)
        
    X_raw = df.drop(columns=cols_to_drop)
    
    return df, X_raw, y

def build_preprocessor_pipeline(categorical_cols, numerical_cols):
    """
    Creates an unfitted ColumnTransformer pipeline.
    
    Args:
        categorical_cols: List of categorical feature names.
        numerical_cols: List of numerical feature names.
        
    Returns:
        ColumnTransformer pipeline.
    """
    return ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_cols),
            ("cat", OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore"), categorical_cols)
        ],
        remainder="drop"
    )

def save_preprocessor(preprocessor, filepath):
    """Saves fitted preprocessor to disk."""
    joblib.dump(preprocessor, filepath)

def load_preprocessor(filepath):
    """Loads fitted preprocessor from disk."""
    return joblib.load(filepath)
