import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
import lightgbm as lgb
import joblib
import os
from typing import Dict, Tuple, List
import warnings
warnings.filterwarnings('ignore')

class CarbonFootprintPredictor:
    """
    Machine Learning models for predicting carbon footprint and trends
    """
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.encoders = {}
        self.feature_names = []
        
    def generate_synthetic_data(self, n_samples: int = 1000) -> pd.DataFrame:
        """Generate synthetic training data for carbon footprint prediction"""
        np.random.seed(42)
        
        data = {
            # Demographics
            'age': np.random.randint(18, 80, n_samples),
            'income': np.random.normal(50000, 20000, n_samples),
            'household_size': np.random.randint(1, 6, n_samples),
            'location_type': np.random.choice(['urban', 'suburban', 'rural'], n_samples),
            
            # Transportation
            'car_miles_per_week': np.random.exponential(100, n_samples),
            'public_transport_usage': np.random.randint(0, 7, n_samples),  # days per week
            'flights_per_year': np.random.poisson(2, n_samples),
            'vehicle_type': np.random.choice(['gasoline', 'diesel', 'electric', 'hybrid'], n_samples),
            
            # Energy
            'electricity_kwh_monthly': np.random.normal(900, 300, n_samples),
            'natural_gas_therms_monthly': np.random.normal(50, 20, n_samples),
            'home_size_sqft': np.random.normal(2000, 800, n_samples),
            'renewable_energy': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
            
            # Food
            'meat_meals_per_week': np.random.randint(0, 21, n_samples),
            'local_food_percentage': np.random.uniform(0, 100, n_samples),
            'organic_food_percentage': np.random.uniform(0, 100, n_samples),
            
            # Waste
            'waste_kg_per_week': np.random.normal(15, 5, n_samples),
            'recycling_percentage': np.random.uniform(0, 100, n_samples),
            'composting': np.random.choice([0, 1], n_samples, p=[0.6, 0.4]),
        }
        
        df = pd.DataFrame(data)
        
        # Calculate target variable (annual carbon footprint in kg CO2)
        df['carbon_footprint'] = (
            # Transportation component
            df['car_miles_per_week'] * 52 * 0.411 +  # Car emissions
            df['flights_per_year'] * 1000 * 0.225 +  # Flight emissions
            
            # Energy component
            df['electricity_kwh_monthly'] * 12 * 0.92 * (1 - df['renewable_energy'] * 0.8) +
            df['natural_gas_therms_monthly'] * 12 * 5.3 +
            
            # Food component
            df['meat_meals_per_week'] * 52 * 2.5 +
            
            # Waste component
            df['waste_kg_per_week'] * 52 * 0.57 * (1 - df['recycling_percentage'] / 100)
        )
        
        # Add some noise and ensure positive values
        df['carbon_footprint'] += np.random.normal(0, 500, n_samples)
        df['carbon_footprint'] = np.maximum(df['carbon_footprint'], 1000)
        
        return df
    
    def preprocess_data(self, df: pd.DataFrame, is_training: bool = True) -> pd.DataFrame:
        """Preprocess data for ML models"""
        df_processed = df.copy()
        
        # Handle categorical variables
        categorical_cols = ['location_type', 'vehicle_type']
        
        for col in categorical_cols:
            if col in df_processed.columns:
                if is_training:
                    self.encoders[col] = LabelEncoder()
                    df_processed[col] = self.encoders[col].fit_transform(df_processed[col])
                else:
                    if col in self.encoders:
                        df_processed[col] = self.encoders[col].transform(df_processed[col])
        
        # Scale numerical features
        if is_training:
            feature_cols = [col for col in df_processed.columns if col != 'carbon_footprint']
            self.feature_names = feature_cols
            self.scalers['features'] = StandardScaler()
            df_processed[feature_cols] = self.scalers['features'].fit_transform(df_processed[feature_cols])
        else:
            if 'features' in self.scalers:
                df_processed[self.feature_names] = self.scalers['features'].transform(df_processed[self.feature_names])
        
        return df_processed
    
    def train_models(self, df: pd.DataFrame) -> Dict:
        """Train multiple ML models for carbon footprint prediction"""
        # Preprocess data
        df_processed = self.preprocess_data(df, is_training=True)
        
        # Prepare features and target
        X = df_processed.drop('carbon_footprint', axis=1)
        y = df_processed['carbon_footprint']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Initialize models
        models_to_train = {
            'random_forest': RandomForestRegressor(n_estimators=100, random_state=42),
            'gradient_boosting': GradientBoostingRegressor(n_estimators=100, random_state=42),
            'xgboost': xgb.XGBRegressor(n_estimators=100, random_state=42),
            'lightgbm': lgb.LGBMRegressor(n_estimators=100, random_state=42, verbose=-1)
        }
        
        results = {}
        
        # Train and evaluate each model
        for name, model in models_to_train.items():
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate metrics
            mse = mean_squared_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
            
            # Store model and results
            self.models[name] = model
            results[name] = {
                'mse': mse,
                'rmse': np.sqrt(mse),
                'r2': r2,
                'cv_mean': cv_scores.mean(),
                'cv_std': cv_scores.std()
            }
        
        return results
    
    def predict_footprint(self, user_data: Dict, model_name: str = 'xgboost') -> float:
        """Predict carbon footprint for new user data"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained yet")
        
        # Convert user data to DataFrame
        df_user = pd.DataFrame([user_data])
        
        # Preprocess
        df_processed = self.preprocess_data(df_user, is_training=False)
        
        # Make prediction
        prediction = self.models[model_name].predict(df_processed[self.feature_names])
        
        return prediction[0]
    
    def get_feature_importance(self, model_name: str = 'xgboost') -> Dict:
        """Get feature importance from trained model"""
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not trained yet")
        
        model = self.models[model_name]
        
        if hasattr(model, 'feature_importances_'):
            importance_dict = dict(zip(self.feature_names, model.feature_importances_))
            return dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
        else:
            return {}
    
    def predict_future_trend(self, historical_data: List[float], days_ahead: int = 30) -> List[float]:
        """Predict future carbon footprint trend using time series analysis"""
        if len(historical_data) < 7:
            # If not enough data, return flat projection
            return [historical_data[-1]] * days_ahead
        
        # Simple trend analysis
        recent_data = np.array(historical_data[-30:])  # Last 30 days
        
        # Calculate trend
        x = np.arange(len(recent_data))
        coeffs = np.polyfit(x, recent_data, 1)
        trend_slope = coeffs[0]
        
        # Project future values
        last_value = historical_data[-1]
        future_values = []
        
        for i in range(1, days_ahead + 1):
            projected_value = last_value + (trend_slope * i)
            # Add some realistic variation
            variation = np.random.normal(0, abs(projected_value) * 0.05)
            future_values.append(max(0, projected_value + variation))
        
        return future_values
    
    def save_models(self, model_dir: str = "models"):
        """Save trained models and preprocessors"""
        os.makedirs(model_dir, exist_ok=True)
        
        # Save models
        for name, model in self.models.items():
            joblib.dump(model, os.path.join(model_dir, f"{name}_model.pkl"))
        
        # Save preprocessors
        joblib.dump(self.scalers, os.path.join(model_dir, "scalers.pkl"))
        joblib.dump(self.encoders, os.path.join(model_dir, "encoders.pkl"))
        joblib.dump(self.feature_names, os.path.join(model_dir, "feature_names.pkl"))
    
    def load_models(self, model_dir: str = "models"):
        """Load trained models and preprocessors"""
        try:
            # Load models
            model_files = ['random_forest_model.pkl', 'gradient_boosting_model.pkl', 
                          'xgboost_model.pkl', 'lightgbm_model.pkl']
            
            for model_file in model_files:
                model_path = os.path.join(model_dir, model_file)
                if os.path.exists(model_path):
                    model_name = model_file.replace('_model.pkl', '')
                    self.models[model_name] = joblib.load(model_path)
            
            # Load preprocessors
            self.scalers = joblib.load(os.path.join(model_dir, "scalers.pkl"))
            self.encoders = joblib.load(os.path.join(model_dir, "encoders.pkl"))
            self.feature_names = joblib.load(os.path.join(model_dir, "feature_names.pkl"))
            
            return True
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
