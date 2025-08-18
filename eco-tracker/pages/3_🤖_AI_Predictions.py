import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from ml_models import CarbonFootprintPredictor
from data_manager import DataManager
from config import Config

st.set_page_config(page_title="AI Predictions", page_icon="🤖", layout="wide")

# Initialize components
@st.cache_resource
def load_predictor():
    predictor = CarbonFootprintPredictor()
    if not predictor.models:
        synthetic_data = predictor.generate_synthetic_data(1500)
        predictor.train_models(synthetic_data)
    return predictor

predictor = load_predictor()
data_manager = DataManager()

st.title("🤖 AI-Powered Carbon Footprint Predictions")

# Check if user is logged in
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.warning("Please create a user profile first from the main app!")
    st.stop()

# Prediction input form
st.subheader("🔮 Predict Your Annual Carbon Footprint")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("**👤 Demographics**")
        age = st.number_input("Age", min_value=18, max_value=100, value=30)
        income = st.number_input("Annual Income ($)", min_value=0, value=50000, step=5000)
        household_size = st.number_input("Household Size", min_value=1, max_value=10, value=2)
        location_type = st.selectbox("Location Type", ["urban", "suburban", "rural"])
        
    with col2:
        st.write("**🚗 Transportation**")
        car_miles_week = st.number_input("Car Miles/Week", min_value=0.0, value=100.0)
        public_transport_days = st.number_input("Public Transport Days/Week", min_value=0, max_value=7, value=2)
        flights_year = st.number_input("Flights/Year", min_value=0, value=2)
        vehicle_type = st.selectbox("Primary Vehicle", ["gasoline", "diesel", "electric", "hybrid"])
        
    with col3:
        st.write("**🏠 Lifestyle**")
        electricity_monthly = st.number_input("Monthly Electricity (kWh)", min_value=0.0, value=900.0)
        natural_gas_monthly = st.number_input("Monthly Natural Gas (therms)", min_value=0.0, value=50.0)
        home_size = st.number_input("Home Size (sq ft)", min_value=0, value=2000)
        renewable_energy = st.selectbox("Renewable Energy", [0, 1], format_func=lambda x: "Yes" if x else "No")
        
        meat_meals_week = st.number_input("Meat Meals/Week", min_value=0, max_value=21, value=10)
        local_food_percent = st.slider("Local Food %", 0, 100, 30)
        recycling_percent = st.slider("Recycling Rate %", 0, 100, 50)
    
    predict_button = st.form_submit_button("🔮 Generate AI Prediction", type="primary")

if predict_button:
    # Prepare prediction data
    prediction_data = {
        'age': age,
        'income': income,
        'household_size': household_size,
        'location_type': location_type,
        'car_miles_per_week': car_miles_week,
        'public_transport_usage': public_transport_days,
        'flights_per_year': flights_year,
        'vehicle_type': vehicle_type,
        'electricity_kwh_monthly': electricity_monthly,
        'natural_gas_therms_monthly': natural_gas_monthly,
        'home_size_sqft': home_size,
        'renewable_energy': renewable_energy,
        'meat_meals_per_week': meat_meals_week,
        'local_food_percentage': local_food_percent,
        'organic_food_percentage': 20,  # Default
        'waste_kg_per_week': 15,  # Default
        'recycling_percentage': recycling_percent,
        'composting': 1 if recycling_percent > 70 else 0
    }
    
    # Make prediction
    predicted_footprint = predictor.predict_footprint(prediction_data)
    daily_prediction = predicted_footprint / 365
    
    # Display results
    st.success("🎯 AI Prediction Complete!")
    
    # Main prediction metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Predicted Annual", f"{predicted_footprint:.0f} kg CO₂")
    with col2:
        st.metric("📅 Daily Average", f"{daily_prediction:.1f} kg CO₂")
    with col3:
        us_average = Config.get_benchmark('us_average')
        vs_average = ((predicted_footprint - us_average) / us_average * 100)
        st.metric("🇺🇸 vs US Average", f"{vs_average:+.0f}%")
    with col4:
        paris_target = Config.get_benchmark('paris_target_2030')
        vs_target = ((predicted_footprint - paris_target) / paris_target * 100)
        st.metric("🌍 vs Paris Target", f"{vs_target:+.0f}%")
    
    # Comparison chart
    st.subheader("📊 How You Compare")
    
    benchmarks = {
        'Your Prediction': predicted_footprint,
        'US Average': Config.get_benchmark('us_average'),
        'EU Average': Config.get_benchmark('eu_average'),
        'Global Average': Config.get_benchmark('global_average'),
        'Paris 2030 Target': Config.get_benchmark('paris_target_2030')
    }
    
    fig_comparison = px.bar(
        x=list(benchmarks.keys()),
        y=list(benchmarks.values()),
        title="Annual Carbon Footprint Comparison",
        color=list(benchmarks.values()),
        color_continuous_scale='RdYlGn_r'
    )
    fig_comparison.update_layout(
        xaxis_title="Category",
        yaxis_title="CO₂ Emissions (kg/year)",
        showlegend=False
    )
    st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Feature importance
    st.subheader("🎯 What Impacts Your Footprint Most?")
    importance = predictor.get_feature_importance()
    
    if importance:
        # Get top 10 features
        top_features = dict(list(importance.items())[:10])
        
        fig_importance = px.bar(
            x=list(top_features.values()),
            y=list(top_features.keys()),
            orientation='h',
            title="Top Factors Affecting Your Carbon Footprint",
            color=list(top_features.values()),
            color_continuous_scale='viridis'
        )
        fig_importance.update_layout(
            xaxis_title="Importance Score",
            yaxis_title="Factors"
        )
        st.plotly_chart(fig_importance, use_container_width=True)
    
    # Future trend prediction
    st.subheader("📈 30-Day Trend Forecast")
    
    # Get historical data for trend
    historical_data = data_manager.get_footprint_history(st.session_state.user_id, 30)
    
    if len(historical_data) >= 7:
        historical_emissions = historical_data['total_emissions'].tolist()
        future_trend = predictor.predict_future_trend(historical_emissions, 30)
        
        # Create forecast chart
        dates_historical = pd.date_range(end=datetime.now(), periods=len(historical_emissions))
        dates_future = pd.date_range(start=datetime.now() + pd.Timedelta(days=1), periods=30)
        
        fig_forecast = go.Figure()
        
        # Historical data
        fig_forecast.add_trace(go.Scatter(
            x=dates_historical,
            y=historical_emissions,
            mode='lines+markers',
            name='Historical',
            line=dict(color='blue')
        ))
        
        # Future prediction
        fig_forecast.add_trace(go.Scatter(
            x=dates_future,
            y=future_trend,
            mode='lines',
            name='AI Forecast',
            line=dict(color='red', dash='dash')
        ))
        
        fig_forecast.update_layout(
            title="30-Day Emissions Forecast",
            xaxis_title="Date",
            yaxis_title="CO₂ Emissions (kg)"
        )
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # Forecast summary
        avg_predicted = np.mean(future_trend)
        avg_historical = np.mean(historical_emissions[-7:])
        trend_change = ((avg_predicted - avg_historical) / avg_historical * 100)
        
        if trend_change > 5:
            st.warning(f"⚠️ Forecast shows {trend_change:.1f}% increase in emissions")
        elif trend_change < -5:
            st.success(f"🎉 Forecast shows {trend_change:.1f}% decrease in emissions")
        else:
            st.info(f"📊 Forecast shows stable emissions ({trend_change:+.1f}% change)")
    
    else:
        st.info("📝 Need at least 7 days of historical data for trend forecasting. Keep logging your daily activities!")

# Model performance info
with st.expander("🔬 AI Model Information"):
    st.write("**Available Models:**")
    
    model_info = {
        'XGBoost': 'High-accuracy gradient boosting (recommended)',
        'Random Forest': 'Robust ensemble method',
        'LightGBM': 'Fast gradient boosting',
        'Gradient Boosting': 'Traditional boosting algorithm'
    }
    
    for model, description in model_info.items():
        st.write(f"• **{model}**: {description}")
    
    st.write("**Model Features:**")
    st.write("• Trained on 1500+ synthetic data points")
    st.write("• Considers demographics, lifestyle, and consumption patterns")
    st.write("• Continuously improved with user data")
    st.write("• Cross-validated for accuracy")

# Prediction scenarios
st.subheader("🎭 What-If Scenarios")

col1, col2 = st.columns(2)

with col1:
    st.write("**🌱 Eco-Friendly Scenario**")
    if st.button("Predict Eco Lifestyle"):
        eco_data = prediction_data.copy()
        eco_data.update({
            'car_miles_per_week': car_miles_week * 0.5,  # 50% less driving
            'renewable_energy': 1,  # 100% renewable
            'meat_meals_per_week': meat_meals_week * 0.3,  # 70% less meat
            'recycling_percentage': 90,  # High recycling
            'public_transport_usage': min(public_transport_days + 3, 7)  # More public transport
        })
        
        eco_prediction = predictor.predict_footprint(eco_data)
        reduction = predicted_footprint - eco_prediction
        
        st.success(f"🌱 Eco Footprint: {eco_prediction:.0f} kg CO₂/year")
        st.success(f"💚 Potential Reduction: {reduction:.0f} kg CO₂/year ({reduction/predicted_footprint*100:.1f}%)")

with col2:
    st.write("**🏭 High-Impact Scenario**")
    if st.button("Predict High-Impact Lifestyle"):
        high_impact_data = prediction_data.copy()
        high_impact_data.update({
            'car_miles_per_week': car_miles_week * 1.5,  # 50% more driving
            'flights_per_year': flights_year + 4,  # More flights
            'meat_meals_per_week': min(meat_meals_week * 1.5, 21),  # More meat
            'electricity_kwh_monthly': electricity_monthly * 1.3,  # Higher energy use
            'recycling_percentage': max(recycling_percent * 0.5, 10)  # Less recycling
        })
        
        high_prediction = predictor.predict_footprint(high_impact_data)
        increase = high_prediction - predicted_footprint
        
        st.error(f"🏭 High-Impact Footprint: {high_prediction:.0f} kg CO₂/year")
        st.error(f"📈 Potential Increase: {increase:.0f} kg CO₂/year ({increase/predicted_footprint*100:.1f}%)")
