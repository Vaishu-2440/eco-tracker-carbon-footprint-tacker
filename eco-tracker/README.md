Eco Tracker - AI/ML Carbon Footprint Tracker

Setup on Windows PowerShell:
1) Create venv: py -m venv .venv
2) Install deps: .\.venv\Scripts\python -m pip install -r requirements.txt
3) Train model: .\.venv\Scripts\python src\train_model.py
4) Run app: .\.venv\Scripts\python -m streamlit run app.py

Open the Streamlit URL shown to use the app.

# 🌱 EcoTracker - AI-Powered Carbon Footprint Tracker

A comprehensive carbon footprint tracking application that uses AI and machine learning to help users monitor, predict, and reduce their environmental impact.

## 🚀 Features

### Core Functionality
- **Real-time Carbon Footprint Tracking** - Log daily activities across transportation, energy, food, and waste
- **AI-Powered Predictions** - Machine learning models predict future emissions and trends
- **Smart Recommendations** - Personalized suggestions based on your usage patterns
- **Advanced Analytics** - Interactive visualizations and detailed insights
- **Goal Setting & Tracking** - Set reduction targets and monitor progress

### AI & Machine Learning
- **Multiple ML Models** - Random Forest, XGBoost, LightGBM, and Gradient Boosting
- **Predictive Analytics** - Forecast future carbon footprint trends
- **Pattern Recognition** - Identify emission patterns and optimization opportunities
- **Intelligent Recommendations** - Context-aware suggestions with impact estimates

### Visualizations
- Interactive dashboards with Plotly
- Trend analysis and seasonal patterns
- Category breakdowns and comparisons
- Goal progress tracking
- Emission forecasting charts

## 📋 Installation

1. **Clone or download the project**
   ```bash
   cd C:\Users\mani3\Downloads\eco-tracker
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to `http://localhost:8501`

## 🏗️ Project Structure

```
eco-tracker/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── data/                 # Database and data files
├── models/               # Trained ML models
└── src/                  # Source code modules
    ├── carbon_calculator.py    # Core carbon footprint calculations
    ├── ml_models.py           # Machine learning models
    ├── data_manager.py        # Database management
    ├── ai_recommendations.py  # AI recommendation engine
    └── visualizations.py      # Advanced visualizations
```

## 🎯 How to Use

1. **Create Profile** - Start by creating your user profile
2. **Log Daily Activities** - Input your transportation, energy, food, and waste data
3. **View Dashboard** - Monitor your emissions with interactive charts
4. **Get AI Predictions** - Use ML models to predict your annual footprint
5. **Analyze Patterns** - Explore advanced analytics to understand your habits
6. **Set Goals** - Create reduction targets and track progress
7. **Follow Recommendations** - Implement AI-generated suggestions

## 🤖 AI Models

The application uses several machine learning models:

- **Random Forest** - Robust ensemble method for baseline predictions
- **XGBoost** - Gradient boosting for high-accuracy predictions
- **LightGBM** - Fast gradient boosting for real-time inference
- **Time Series Analysis** - Trend prediction and forecasting

## 📊 Data Categories

### Transportation
- Car travel (gasoline, diesel, electric)
- Public transportation
- Flights (domestic/international)
- Alternative transport (cycling, walking)

### Energy
- Electricity consumption
- Natural gas usage
- Heating oil
- Renewable energy sources

### Food
- Meat consumption (beef, chicken, etc.)
- Dairy products
- Local vs. imported food
- Food waste

### Waste
- Landfill waste
- Recycling rates
- Composting
- Waste reduction efforts

## 🌍 Environmental Impact

The average person's carbon footprint:
- **Global Average**: 4.8 tons CO₂/year
- **US Average**: 16 tons CO₂/year
- **Paris Agreement Target**: 2.3 tons CO₂/year by 2030

## 🔧 Technical Details

- **Backend**: Python with SQLite database
- **Frontend**: Streamlit web interface
- **ML Libraries**: scikit-learn, XGBoost, LightGBM, TensorFlow
- **Visualization**: Plotly, Matplotlib, Seaborn
- **Data Processing**: Pandas, NumPy

## 🤝 Contributing

This is an open-source project. Feel free to contribute by:
- Adding new emission factors
- Improving ML model accuracy
- Enhancing visualizations
- Adding new features

## 📄 License

MIT License - Feel free to use and modify for your projects.

## 🆘 Support

If you encounter any issues:
1. Check that all dependencies are installed correctly
2. Ensure you have Python 3.8+ installed
3. Verify the database permissions in the data/ directory

---

**Start tracking your carbon footprint today and make a positive impact on the environment! 🌱**