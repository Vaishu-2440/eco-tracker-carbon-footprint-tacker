#!/usr/bin/env python3
"""
Main runner script for EcoTracker application
"""

import os
import sys
import subprocess
import argparse

def setup_environment():
    """Set up the environment and install dependencies"""
    print("🔧 Setting up EcoTracker environment...")
    
    # Check if virtual environment exists
    venv_path = ".venv"
    if not os.path.exists(venv_path):
        print("📦 Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", venv_path], check=True)
    
    # Install dependencies
    print("📥 Installing dependencies...")
    if os.name == 'nt':  # Windows
        pip_path = os.path.join(venv_path, "Scripts", "pip")
        python_path = os.path.join(venv_path, "Scripts", "python")
    else:  # Unix/Linux/Mac
        pip_path = os.path.join(venv_path, "bin", "pip")
        python_path = os.path.join(venv_path, "bin", "python")
    
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)
    
    return python_path

def train_models(python_path):
    """Train the ML models"""
    print("🤖 Training ML models...")
    subprocess.run([python_path, "src/train_model.py"], check=True)

def run_app(python_path):
    """Run the Streamlit application"""
    print("🚀 Starting EcoTracker application...")
    subprocess.run([python_path, "-m", "streamlit", "run", "app.py"], check=True)

def main():
    parser = argparse.ArgumentParser(description="EcoTracker Application Runner")
    parser.add_argument("--setup-only", action="store_true", 
                       help="Only setup environment, don't run app")
    parser.add_argument("--train-only", action="store_true",
                       help="Only train models, don't run app")
    parser.add_argument("--skip-training", action="store_true",
                       help="Skip model training and run app directly")
    
    args = parser.parse_args()
    
    try:
        # Setup environment
        python_path = setup_environment()
        
        if args.setup_only:
            print("✅ Environment setup complete!")
            return
        
        # Train models (unless skipped)
        if not args.skip_training:
            train_models(python_path)
        
        if args.train_only:
            print("✅ Model training complete!")
            return
        
        # Run the application
        run_app(python_path)
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 EcoTracker stopped by user")
        sys.exit(0)

if __name__ == "__main__":
    main()
