# 📚 EcoTracker Documentation

## 🏗️ Architecture Overview

EcoTracker is built with a modular architecture using Python and Streamlit:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit UI  │────│  Core Modules   │────│   Data Layer    │
│                 │    │                 │    │                 │
│ • Dashboard     │    │ • Calculator    │    │ • SQLite DB     │
│ • Input Forms   │    │ • ML Models     │    │ • Data Manager  │
│ • Analytics     │    │ • AI Engine     │    │ • File Storage  │
│ • Visualizations│    │ • Utils         │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 File Structure Explained

### Core Application Files
- **`app.py`** - Main Streamlit application with user management
- **`start.bat`** - Windows batch script for easy startup
- **`run.py`** - Cross-platform Python runner script
- **`setup.py`** - Package installation configuration

### Source Code (`src/`)
- **`carbon_calculator.py`** - Core carbon footprint calculation engine
- **`ml_models.py`** - Machine learning models for predictions
- **`data_manager.py`** - Database operations and data persistence
- **`ai_recommendations.py`** - AI-powered recommendation system
- **`visualizations.py`** - Advanced plotting and chart functions
- **`utils.py`** - Utility functions and helpers
- **`config.py`** - Configuration constants and settings
- **`api_integrations.py`** - External API integrations
- **`train_model.py`** - Model training script

### Pages (`pages/`)
- **`1_🏠_Dashboard.py`** - Main dashboard overview
- **`2_📝_Daily_Input.py`** - Daily activity input forms
- **`3_🤖_AI_Predictions.py`** - ML prediction interface
- **`4_📈_Analytics.py`** - Advanced analytics and trends
- **`5_🎯_Goals.py`** - Goal setting and tracking
- **`6_💡_Recommendations.py`** - AI recommendations display

## 🚀 Quick Start Guide

### Method 1: Using Batch Script (Windows)
```bash
# Navigate to project directory
cd C:\Users\mani3\Downloads\eco-tracker

# Run the startup script
start.bat
```

### Method 2: Manual Setup
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train ML models
python src\train_model.py

# Run application
streamlit run app.py
```

## 🤖 Machine Learning Models

### Model Types
1. **Random Forest** - Ensemble method, robust to outliers
2. **XGBoost** - Gradient boosting, high accuracy (default)
3. **LightGBM** - Fast gradient boosting for real-time inference
4. **Gradient Boosting** - Traditional boosting algorithm

### Training Data
- **Synthetic Dataset**: 2000 samples with realistic patterns
- **Features**: Demographics, lifestyle, consumption patterns
- **Target**: Annual carbon footprint (kg CO₂)

### Model Performance Metrics
- **R² Score**: Coefficient of determination
- **RMSE**: Root Mean Square Error
- **Cross-Validation**: 5-fold CV for robustness

## 📊 Carbon Footprint Categories

### Transportation (kg CO₂ per mile)
- Gasoline car: 0.411
- Diesel car: 0.364
- Electric car: 0.1
- Bus: 0.089
- Train: 0.041
- Domestic flight: 0.255
- International flight: 0.195

### Energy (kg CO₂ per unit)
- Electricity: 0.92 per kWh
- Natural gas: 5.3 per therm
- Heating oil: 10.15 per gallon
- Propane: 5.68 per gallon

### Food (kg CO₂ per kg)
- Beef: 27.0
- Lamb: 39.2
- Pork: 12.1
- Chicken: 6.9
- Fish: 6.1
- Dairy: 3.2
- Vegetables: 2.0

### Waste (kg CO₂ per kg)
- Landfill: 0.57
- Recycling: 0.0
- Composting: 0.0
- Incineration: 0.7

## 🎯 Features Deep Dive

### Dashboard
- Real-time emission tracking
- Key performance indicators
- Trend visualization
- Category breakdowns
- Weekly patterns

### Daily Input
- Multi-category data entry
- Input validation
- Quick templates
- Instant calculations
- Activity logging

### AI Predictions
- Annual footprint forecasting
- Feature importance analysis
- Scenario modeling
- Benchmark comparisons
- Confidence intervals

### Analytics
- Advanced trend analysis
- Pattern recognition
- Statistical distributions
- Seasonal analysis
- Export capabilities

### Goals
- SMART goal setting
- Progress tracking
- Achievement statistics
- Suggested targets
- Deadline management

### Recommendations
- Personalized suggestions
- Impact estimations
- Difficulty assessments
- Action plans
- Community challenges

## 🔧 Configuration

### Environment Variables
Create `.env` file from `.env.example`:
```
CARBON_INTERFACE_API_KEY=your_key_here
WEATHER_API_KEY=your_key_here
DATABASE_PATH=data/eco_tracker.db
```

### Database Schema
- **users**: User profiles and authentication
- **daily_footprints**: Daily emission records
- **activities**: Individual activity logs
- **goals**: User-defined reduction targets

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**
   ```
   Solution: Ensure all dependencies are installed
   pip install -r requirements.txt
   ```

2. **Database Errors**
   ```
   Solution: Check data directory permissions
   mkdir data (if doesn't exist)
   ```

3. **Model Training Fails**
   ```
   Solution: Run training script separately
   python src\train_model.py
   ```

4. **Streamlit Port Issues**
   ```
   Solution: Use different port
   streamlit run app.py --server.port 8502
   ```

### Performance Optimization
- Models are cached using `@st.cache_resource`
- Database connections are managed efficiently
- Large datasets are paginated
- Visualizations use efficient plotting libraries

## 🔮 Future Enhancements

### Planned Features
- Real-time API integrations
- Mobile app companion
- Social features and leaderboards
- Advanced ML models (neural networks)
- Carbon offset marketplace integration
- IoT device integrations

### API Integrations
- **Carbon Interface**: Real emission factors
- **Electricity Maps**: Grid carbon intensity
- **Weather APIs**: Climate-adjusted calculations
- **Government Data**: Local recycling rates

## 📈 Data Science Methodology

### Feature Engineering
- Demographic normalization
- Seasonal adjustments
- Geographic factors
- Lifestyle clustering

### Model Validation
- Train/test split (80/20)
- Cross-validation (5-fold)
- Feature importance analysis
- Hyperparameter tuning

### Prediction Pipeline
1. Data preprocessing
2. Feature scaling
3. Model inference
4. Confidence estimation
5. Result interpretation

## 🌍 Environmental Impact

### Global Context
- **Current Global Average**: 4.8 tons CO₂/person/year
- **Paris Agreement Target**: 2.3 tons CO₂/person/year by 2030
- **Net Zero Target**: <1 ton CO₂/person/year by 2050

### Reduction Strategies
- **Transportation**: 40% of personal emissions
- **Energy**: 30% of personal emissions
- **Food**: 20% of personal emissions
- **Waste**: 10% of personal emissions

## 🔒 Privacy & Security

### Data Protection
- Local SQLite database
- No cloud data transmission
- User data encryption options
- GDPR compliance ready

### Best Practices
- Regular data backups
- Secure API key storage
- Input validation
- Error handling

---

**For technical support or feature requests, please refer to the project repository.**
