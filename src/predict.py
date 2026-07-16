import os
import sys
from pathlib import Path

import pandas as pd
import numpy as np
import joblib

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import config

class InferenceEngine:
    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.load_assets()
        
    def load_assets(self):
        """Loads fitted ColumnTransformer and best model from disk."""
        if os.path.exists(config.MODEL_PATH) and os.path.exists(config.PREPROCESSOR_PATH):
            self.model = joblib.load(config.MODEL_PATH)
            self.preprocessor = joblib.load(config.PREPROCESSOR_PATH)
        else:
            self.model = None
            self.preprocessor = None

    def get_contributing_factors(self, data_dict):
        """
        Extracts key contributing risk factors from raw input features
        based on domain knowledge and EDA results.
        """
        factors = []
        
        # Overtime risk
        overtime = data_dict.get("OverTime", "No")
        if overtime == "Yes":
            factors.append("Working Overtime: Overtime is a strong driver of burnout and attrition.")
            
        # Job Satisfaction risk
        job_sat = int(data_dict.get("JobSatisfaction", 4))
        if job_sat <= 2:
            factors.append(f"Low Job Satisfaction: Rated {job_sat}/4. Dissatisfaction with day-to-day work.")
            
        # Environment Satisfaction risk
        env_sat = int(data_dict.get("EnvironmentSatisfaction", 4))
        if env_sat <= 2:
            factors.append(f"Low Environment Satisfaction: Rated {env_sat}/4. Negative workspace sentiment.")
            
        # Work-Life Balance risk
        wlb = int(data_dict.get("WorkLifeBalance", 4))
        if wlb <= 2:
            factors.append(f"Poor Work-Life Balance: Rated {wlb}/4. Inadequate time for personal life.")
            
        # Career growth / Promotion delay
        years_since_promo = int(data_dict.get("YearsSinceLastPromotion", 0))
        if years_since_promo >= 5:
            factors.append(f"Delayed Promotion: Last promoted {years_since_promo} years ago. Stagnation risk.")
            
        # Distance from home
        distance = int(data_dict.get("DistanceFromHome", 0))
        if distance >= 15:
            factors.append(f"Long Commute: Living {distance} km away from work creates travel strain.")
            
        # Salary hike
        hike = int(data_dict.get("PercentSalaryHike", 11))
        if hike < 13:
            factors.append(f"Low Salary Hike: {hike}% increment is below expectations.")
            
        # Stock Option Level
        stock_level = int(data_dict.get("StockOptionLevel", 0))
        if stock_level == 0:
            factors.append("No Stock Options: Level is 0. Missing equity retention incentive.")
            
        # Role & travel frequency
        travel = data_dict.get("BusinessTravel", "Travel_Rarely")
        if travel == "Travel_Frequently":
            factors.append("Frequent Business Travel: High travel demands impact personal routine.")

        if not factors:
            factors.append("No severe workplace risk factors identified. Sentiment is stable.")
            
        return factors

    def predict(self, raw_features_dict):
        """
        Runs prediction for a single set of employee features.
        
        Args:
            raw_features_dict: Dict containing the 30 raw feature columns.
            
        Returns:
            dict: Prediction result containing risk level, probability, and risk factors.
        """
        if self.model is None or self.preprocessor is None:
            # reload if assets weren't loaded initially
            self.load_assets()
            if self.model is None or self.preprocessor is None:
                raise FileNotFoundError(
                    "Model or Preprocessor files not found. Please run model training (src/train.py) first."
                )
                
        # Convert dictionary to DataFrame
        df_input = pd.DataFrame([raw_features_dict])
        
        # Ensure all columns required are present in correct order
        # (categorical + numerical lists from config)
        required_cols = config.CATEGORICAL_FEATURES + config.NUMERICAL_FEATURES
        # Reorder/select columns
        df_input = df_input[required_cols]
        
        # Transform using ColumnTransformer
        X_processed = self.preprocessor.transform(df_input)
        
        # Convert processed features back to DataFrame to preserve feature name consistency for models like XGBoost
        try:
            feature_names = self.preprocessor.get_feature_names_out()
        except AttributeError:
            feature_names = [f"f_{i}" for i in range(X_processed.shape[1])]
            
        X_processed_df = pd.DataFrame(X_processed, columns=feature_names)
        
        # Predict probability & risk label
        prob = float(self.model.predict_proba(X_processed_df)[0, 1])
        prediction = int(self.model.predict(X_processed_df)[0])
        
        risk_level = "High" if prob >= 0.5 else "Low"
        factors = self.get_contributing_factors(raw_features_dict) if risk_level == "High" else []
        
        return {
            "prediction": prediction,
            "probability": round(prob, 4),
            "risk_level": risk_level,
            "risk_factors": factors
        }
