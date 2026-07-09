import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import xgboost as xgb
from imblearn.over_sampling import SMOTE
import joblib
from src import config
from src import preprocessing

def calculate_scale_pos_weight(y_train):
    """Calculates class balance ratio for XGBoost."""
    class_counts = y_train.value_counts()
    neg_count = class_counts.get(0, 1)
    pos_count = class_counts.get(1, 1)
    return neg_count / pos_count

def train_and_evaluate_model(model, X_train, y_train, X_test, y_test, model_name):
    """
    Fits a model, evaluates it, prints metrics, and returns the model and its F1 score.
    """
    print(f"Training {model_name}...")
    
    # Fit model
    model.fit(X_train, y_train)
    
    # Make predictions
    y_pred = model.predict(X_test)
    
    # Evaluate
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    conf = confusion_matrix(y_test, y_pred)
    
    print(f"[{model_name}] F1: {f1:.4f} | Recall: {rec:.4f} | Accuracy: {acc:.4f}")
    print(f"Confusion Matrix:\n{conf}\n")
        
    return model, f1

def main():
    # Make sure output directories exist
    os.makedirs(config.MODELS_DIR, exist_ok=True)
    
    # 1. Load and preprocess data
    print("Loading raw dataset...")
    df, X_raw, y = preprocessing.load_and_preprocess(config.RAW_DATA_PATH)
    
    # 2. Split train/test
    print("Splitting train and test sets...")
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        X_raw, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 3. Fit and apply ColumnTransformer preprocessor
    print("Fitting ColumnTransformer on train data...")
    preprocessor = preprocessing.build_preprocessor_pipeline(
        config.CATEGORICAL_FEATURES, config.NUMERICAL_FEATURES
    )
    
    X_train_processed = preprocessor.fit_transform(X_train_raw)
    X_test_processed = preprocessor.transform(X_test_raw)
    
    # Convert back to DataFrame to preserve column names if needed
    try:
        feature_names = preprocessor.get_feature_names_out()
    except AttributeError:
        feature_names = [f"f_{i}" for i in range(X_train_processed.shape[1])]
        
    X_train_df = pd.DataFrame(X_train_processed, columns=feature_names)
    X_test_df = pd.DataFrame(X_test_processed, columns=feature_names)
    
    # Save the fitted preprocessor
    preprocessing.save_preprocessor(preprocessor, config.PREPROCESSOR_PATH)
    print(f"Saved fitted preprocessor to {config.PREPROCESSOR_PATH}")
    
    # 4. Handle class imbalance using SMOTE
    print("Applying SMOTE to training data...")
    smote = SMOTE(random_state=42)
    X_train_resampled, y_train_resampled = smote.fit_resample(X_train_df, y_train)
    
    # Calculate scale_pos_weight for XGBoost
    scale_pos_weight = calculate_scale_pos_weight(y_train)
    
    runs_summary = []
    
    # 5. Train Models
    # Model 1: Tuned Logistic Regression
    lr_tuned = LogisticRegression(
        C=0.1, 
        solver='saga', 
        penalty='l2', 
        max_iter=2000, 
        class_weight='balanced', 
        random_state=42
    )
    model, f1 = train_and_evaluate_model(
        lr_tuned, X_train_resampled, y_train_resampled, X_test_df, y_test, 
        "LogisticRegression_Tuned"
    )
    runs_summary.append((model, f1, "LogisticRegression_Tuned"))
    
    # Model 2: XGBoost Tuned
    xgb_tuned = xgb.XGBClassifier(
        objective='binary:logistic',
        eval_metric='logloss',
        learning_rate=0.1,
        max_depth=5,
        n_estimators=200,
        gamma=0.2,
        scale_pos_weight=scale_pos_weight,
        random_state=42
    )
    model, f1 = train_and_evaluate_model(
        xgb_tuned, X_train_resampled, y_train_resampled, X_test_df, y_test, 
        "XGBoost_Tuned"
    )
    runs_summary.append((model, f1, "XGBoost_Tuned"))
    
    # Model 3: Random Forest Classifier
    rf_initial = RandomForestClassifier(
        n_estimators=100, 
        class_weight='balanced', 
        random_state=42
    )
    model, f1 = train_and_evaluate_model(
        rf_initial, X_train_resampled, y_train_resampled, X_test_df, y_test, 
        "RandomForest_Initial"
    )
    runs_summary.append((model, f1, "RandomForest_Initial"))
    
    # 6. Model Selection: Select the model with the highest F1-Score
    best_model_info = max(runs_summary, key=lambda x: x[1])
    best_model, best_f1, best_name = best_model_info
    
    print(f"\nSelected best model: {best_name} with F1-Score of {best_f1:.4f}")
    
    # Save the best model
    joblib.dump(best_model, config.MODEL_PATH)
    print(f"Saved best model object to {config.MODEL_PATH}")
    print("Training process finished successfully!")

if __name__ == "__main__":
    main()
