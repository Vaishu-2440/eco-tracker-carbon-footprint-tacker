#!/usr/bin/env python3
"""
Training script for carbon footprint prediction models
"""

import os
import sys
import pandas as pd
from ml_models import CarbonFootprintPredictor

def main():
    """Train and save ML models"""
    print("Training Carbon Footprint Prediction Models...")
    
    # Initialize predictor
    predictor = CarbonFootprintPredictor()
    
    # Generate synthetic training data
    print("Generating synthetic training data...")
    training_data = predictor.generate_synthetic_data(2000)
    print(f"Generated {len(training_data)} training samples")
    
    # Train models
    print("Training ML models...")
    results = predictor.train_models(training_data)
    
    # Display results
    print("\nModel Performance:")
    print("-" * 50)
    for model_name, metrics in results.items():
        print(f"{model_name.upper()}:")
        print(f"  R² Score: {metrics['r2']:.4f}")
        print(f"  RMSE: {metrics['rmse']:.2f}")
        print(f"  CV Mean: {metrics['cv_mean']:.4f} ± {metrics['cv_std']:.4f}")
        print()
    
    # Save models
    print("Saving trained models...")
    os.makedirs("models", exist_ok=True)
    predictor.save_models("models")
    
    print("Model training completed successfully!")
    print("You can now run the main application: streamlit run app.py")

if __name__ == "__main__":
    main()
