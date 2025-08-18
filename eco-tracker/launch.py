#!/usr/bin/env python3
"""
Simple launcher for EcoTracker application
"""

import os
import sys
import subprocess

def main():
    """Launch EcoTracker application"""
    print("Starting EcoTracker Carbon Footprint Tracker...")
    
    # Create necessary directories
    os.makedirs("data", exist_ok=True)
    os.makedirs("models", exist_ok=True)
    os.makedirs("exports", exist_ok=True)
    
    # Check if models exist, train if needed
    if not os.path.exists("models/xgboost_model.pkl"):
        print("Training ML models (first time setup)...")
        try:
            subprocess.run([sys.executable, "src/train_model.py"], check=True)
            print("Model training completed!")
        except subprocess.CalledProcessError:
            print("Warning: Model training failed, but app will still work")
    
    # Launch Streamlit app
    print("Launching EcoTracker application...")
    print("App will be available at: http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"], check=True)
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"Error launching app: {e}")
        print("Try running: python -m streamlit run app.py")

if __name__ == "__main__":
    main()
