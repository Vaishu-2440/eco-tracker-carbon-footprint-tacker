import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from carbon_calculator import CarbonFootprintCalculator
from ml_models import CarbonFootprintPredictor
from data_manager import DataManager

# Page configuration
st.set_page_config(
    page_title="EcoTracker - Carbon Footprint Monitor",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize components
@st.cache_resource
def initialize_components():
    calculator = CarbonFootprintCalculator()
    predictor = CarbonFootprintPredictor()
    data_manager = DataManager()
    
    # Train ML models if not already trained
    if not predictor.models:
        with st.spinner("Training AI models... This may take a moment."):
            synthetic_data = predictor.generate_synthetic_data(1000)
            predictor.train_models(synthetic_data)
    
    return calculator, predictor, data_manager

calculator, predictor, data_manager = initialize_components()

# Sidebar for navigation
st.sidebar.title("🌱 EcoTracker")
page = st.sidebar.selectbox(
    "Navigate",
    ["Dashboard", "Daily Input", "AI Predictions", "Analytics", "Goals", "Recommendations"]
)

# User management
if 'user_id' not in st.session_state:
    st.session_state.user_id = None

if st.session_state.user_id is None:
    st.sidebar.subheader("User Profile")
    user_name = st.sidebar.text_input("Enter your name:")
    user_email = st.sidebar.text_input("Email (optional):")
    
    if st.sidebar.button("Create Profile"):
        if user_name:
            user_id = data_manager.create_user(user_name, user_email)
            st.session_state.user_id = user_id
            st.sidebar.success(f"Welcome, {user_name}!")
            st.rerun()
else:
    user_info = data_manager.get_user(st.session_state.user_id)
    st.sidebar.success(f"Welcome back, {user_info['name']}!")
    if st.sidebar.button("Switch User"):
        st.session_state.user_id = None
        st.rerun()

# Main content based on selected page
if st.session_state.user_id is None:
    st.title("🌱 Welcome to EcoTracker")
    st.markdown("""
    ### Your AI-Powered Carbon Footprint Companion
    
    EcoTracker helps you monitor, predict, and reduce your carbon footprint using advanced AI and machine learning.
    
    **Features:**
    - 📊 Real-time carbon footprint tracking
    - 🤖 AI-powered predictions and insights
    - 📈 Advanced analytics and visualizations
    - 🎯 Goal setting and progress tracking
    - 💡 Personalized recommendations
    
    Please create a user profile in the sidebar to get started!
    """)

elif page == "Dashboard":
    st.title("📊 Carbon Footprint Dashboard")
    
    # Get recent data
    recent_data = data_manager.get_footprint_history(st.session_state.user_id, 30)
    
    if len(recent_data) > 0:
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_daily = recent_data['total_emissions'].mean()
            st.metric("Avg Daily Emissions", f"{avg_daily:.1f} kg CO₂")
        
        with col2:
            monthly_total = recent_data['total_emissions'].sum()
            st.metric("Monthly Total", f"{monthly_total:.1f} kg CO₂")
        
        with col3:
            trend = "📈" if recent_data['total_emissions'].iloc[-1] > recent_data['total_emissions'].iloc[0] else "📉"
            st.metric("Trend", trend)
        
        with col4:
            days_logged = len(recent_data)
            st.metric("Days Logged", days_logged)
        
        # Emissions over time chart
        st.subheader("Emissions Over Time")
        fig = px.line(recent_data, x='date', y='total_emissions', 
                     title="Daily Carbon Footprint")
        fig.update_layout(xaxis_title="Date", yaxis_title="CO₂ Emissions (kg)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Category breakdown
        st.subheader("Emissions by Category")
        categories = ['transportation_emissions', 'energy_emissions', 
                     'food_emissions', 'waste_emissions']
        category_totals = recent_data[categories].sum()
        
        fig_pie = px.pie(values=category_totals.values, 
                        names=['Transportation', 'Energy', 'Food', 'Waste'],
                        title="Emissions Breakdown")
        st.plotly_chart(fig_pie, use_container_width=True)
        
    else:
        st.info("No data available yet. Start by logging your daily activities!")

elif page == "Daily Input":
    st.title("📝 Daily Carbon Footprint Input")
    
    # Date selection
    selected_date = st.date_input("Select Date", datetime.now())
    
    # Transportation section
    st.subheader("🚗 Transportation")
    col1, col2 = st.columns(2)
    
    with col1:
        car_miles = st.number_input("Car Miles Driven", min_value=0.0, value=0.0)
        car_type = st.selectbox("Vehicle Type", 
                               ["car_gasoline", "car_diesel", "car_electric"])
        
    with col2:
        public_transport = st.number_input("Public Transport Miles", min_value=0.0, value=0.0)
        flights = st.number_input("Flight Miles", min_value=0.0, value=0.0)
    
    # Energy section
    st.subheader("⚡ Energy")
    col1, col2 = st.columns(2)
    
    with col1:
        electricity = st.number_input("Electricity Usage (kWh)", min_value=0.0, value=0.0)
        natural_gas = st.number_input("Natural Gas (therms)", min_value=0.0, value=0.0)
    
    with col2:
        heating_oil = st.number_input("Heating Oil (gallons)", min_value=0.0, value=0.0)
    
    # Food section
    st.subheader("🍽️ Food")
    col1, col2 = st.columns(2)
    
    with col1:
        beef_meals = st.number_input("Beef Meals", min_value=0, value=0)
        chicken_meals = st.number_input("Chicken Meals", min_value=0, value=0)
    
    with col2:
        dairy_servings = st.number_input("Dairy Servings", min_value=0, value=0)
        vegetable_servings = st.number_input("Vegetable Servings", min_value=0, value=0)
    
    # Waste section
    st.subheader("🗑️ Waste")
    waste_kg = st.number_input("Waste Generated (kg)", min_value=0.0, value=0.0)
    recycling_percent = st.slider("Recycling Percentage", 0, 100, 50)
    
    # Calculate footprint
    if st.button("Calculate Daily Footprint", type="primary"):
        # Prepare data for calculator
        user_data = {
            'transportation': {
                car_type: {'distance': car_miles, 'frequency': 1},
                'bus': {'distance': public_transport, 'frequency': 1},
                'plane_domestic': {'distance': flights, 'frequency': 1}
            },
            'energy': {
                'electricity': electricity,
                'natural_gas': natural_gas,
                'heating_oil': heating_oil
            },
            'food': {
                'beef': beef_meals * 0.25,  # Approximate kg per meal
                'chicken': chicken_meals * 0.2,
                'dairy': dairy_servings * 0.1,
                'vegetables': vegetable_servings * 0.05
            },
            'waste': {
                'landfill': waste_kg * (1 - recycling_percent/100),
                'recycling': waste_kg * (recycling_percent/100)
            }
        }
        
        # Calculate emissions
        footprint_data = calculator.calculate_total_footprint(user_data)
        
        # Save to database
        data_manager.save_daily_footprint(
            st.session_state.user_id, 
            selected_date.strftime('%Y-%m-%d'), 
            footprint_data
        )
        
        # Display results
        st.success("Daily footprint calculated and saved!")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Transportation", f"{footprint_data['transportation']:.1f} kg CO₂")
        with col2:
            st.metric("Energy", f"{footprint_data['energy']:.1f} kg CO₂")
        with col3:
            st.metric("Food", f"{footprint_data['food']:.1f} kg CO₂")
        with col4:
            st.metric("Waste", f"{footprint_data['waste']:.1f} kg CO₂")
        with col5:
            st.metric("Total", f"{footprint_data['total']:.1f} kg CO₂")

elif page == "AI Predictions":
    st.title("🤖 AI-Powered Predictions")
    
    st.subheader("Predict Your Carbon Footprint")
    
    # Input form for prediction
    with st.form("prediction_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            age = st.number_input("Age", min_value=18, max_value=100, value=30)
            income = st.number_input("Annual Income ($)", min_value=0, value=50000)
            household_size = st.number_input("Household Size", min_value=1, max_value=10, value=2)
            location_type = st.selectbox("Location", ["urban", "suburban", "rural"])
            
        with col2:
            car_miles_week = st.number_input("Car Miles per Week", min_value=0.0, value=100.0)
            flights_year = st.number_input("Flights per Year", min_value=0, value=2)
            electricity_monthly = st.number_input("Monthly Electricity (kWh)", min_value=0.0, value=900.0)
            home_size = st.number_input("Home Size (sq ft)", min_value=0, value=2000)
        
        predict_button = st.form_submit_button("Predict Annual Footprint")
    
    if predict_button:
        # Prepare prediction data
        prediction_data = {
            'age': age,
            'income': income,
            'household_size': household_size,
            'location_type': location_type,
            'car_miles_per_week': car_miles_week,
            'public_transport_usage': 2,  # Default
            'flights_per_year': flights_year,
            'vehicle_type': 'gasoline',  # Default
            'electricity_kwh_monthly': electricity_monthly,
            'natural_gas_therms_monthly': 50,  # Default
            'home_size_sqft': home_size,
            'renewable_energy': 0,  # Default
            'meat_meals_per_week': 10,  # Default
            'local_food_percentage': 30,  # Default
            'organic_food_percentage': 20,  # Default
            'waste_kg_per_week': 15,  # Default
            'recycling_percentage': 50,  # Default
            'composting': 0  # Default
        }
        
        # Make prediction
        predicted_footprint = predictor.predict_footprint(prediction_data)
        
        # Display prediction
        st.success(f"Predicted Annual Carbon Footprint: **{predicted_footprint:.0f} kg CO₂**")
        
        # Compare with averages
        us_average = 16000  # kg CO2 per year
        global_average = 4800
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Your Prediction", f"{predicted_footprint:.0f} kg CO₂")
        with col2:
            st.metric("US Average", f"{us_average} kg CO₂")
        with col3:
            st.metric("Global Average", f"{global_average} kg CO₂")
        
        # Feature importance
        st.subheader("What Impacts Your Footprint Most?")
        importance = predictor.get_feature_importance()
        if importance:
            importance_df = pd.DataFrame(list(importance.items()), 
                                       columns=['Factor', 'Importance'])
            fig = px.bar(importance_df.head(10), x='Importance', y='Factor',
                        orientation='h', title="Top Factors Affecting Your Carbon Footprint")
            st.plotly_chart(fig, use_container_width=True)

elif page == "Analytics":
    st.title("📈 Advanced Analytics")
    
    # Get historical data
    history_data = data_manager.get_footprint_history(st.session_state.user_id, 90)
    
    if len(history_data) > 0:
        # Trend analysis
        st.subheader("Trend Analysis")
        
        # Calculate moving averages
        history_data['7_day_avg'] = history_data['total_emissions'].rolling(window=7).mean()
        history_data['30_day_avg'] = history_data['total_emissions'].rolling(window=30).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=history_data['date'], y=history_data['total_emissions'],
                                mode='lines', name='Daily Emissions', line=dict(color='lightblue')))
        fig.add_trace(go.Scatter(x=history_data['date'], y=history_data['7_day_avg'],
                                mode='lines', name='7-Day Average', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=history_data['date'], y=history_data['30_day_avg'],
                                mode='lines', name='30-Day Average', line=dict(color='darkblue')))
        
        fig.update_layout(title="Emissions Trends", xaxis_title="Date", 
                         yaxis_title="CO₂ Emissions (kg)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Category analysis
        st.subheader("Category Performance")
        
        categories = ['transportation_emissions', 'energy_emissions', 
                     'food_emissions', 'waste_emissions']
        category_names = ['Transportation', 'Energy', 'Food', 'Waste']
        
        fig = go.Figure()
        for i, (cat, name) in enumerate(zip(categories, category_names)):
            fig.add_trace(go.Scatter(x=history_data['date'], y=history_data[cat],
                                   mode='lines', name=name, stackgroup='one'))
        
        fig.update_layout(title="Emissions by Category Over Time", 
                         xaxis_title="Date", yaxis_title="CO₂ Emissions (kg)")
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        st.subheader("Statistics Summary")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Best Day", f"{history_data['total_emissions'].min():.1f} kg CO₂")
        with col2:
            st.metric("Worst Day", f"{history_data['total_emissions'].max():.1f} kg CO₂")
        with col3:
            st.metric("Average", f"{history_data['total_emissions'].mean():.1f} kg CO₂")
        with col4:
            st.metric("Std Deviation", f"{history_data['total_emissions'].std():.1f} kg CO₂")
        
    else:
        st.info("Not enough data for analytics. Start logging your daily activities!")

elif page == "Goals":
    st.title("🎯 Carbon Reduction Goals")
    
    # Create new goal
    st.subheader("Set New Goal")
    with st.form("new_goal"):
        goal_type = st.selectbox("Goal Type", 
                                ["Daily Emissions", "Weekly Emissions", "Monthly Emissions"])
        target_value = st.number_input("Target Value (kg CO₂)", min_value=0.0, value=10.0)
        target_date = st.date_input("Target Date")
        
        if st.form_submit_button("Create Goal"):
            goal_id = data_manager.create_goal(
                st.session_state.user_id, goal_type, target_value, 
                target_date.strftime('%Y-%m-%d')
            )
            st.success("Goal created successfully!")
    
    # Display existing goals
    st.subheader("Your Goals")
    goals = data_manager.get_user_goals(st.session_state.user_id)
    
    if len(goals) > 0:
        for _, goal in goals.iterrows():
            progress = (goal['current_value'] / goal['target_value']) * 100 if goal['target_value'] > 0 else 0
            
            st.write(f"**{goal['goal_type']}**: {goal['current_value']:.1f} / {goal['target_value']:.1f} kg CO₂")
            st.progress(min(progress / 100, 1.0))
            
            if goal['target_date']:
                days_left = (pd.to_datetime(goal['target_date']) - pd.Timestamp.now()).days
                st.write(f"Days remaining: {days_left}")
            
            st.write("---")
    else:
        st.info("No goals set yet. Create your first goal above!")

elif page == "Recommendations":
    st.title("💡 AI-Powered Recommendations")
    
    # Get recent footprint data
    recent_data = data_manager.get_footprint_history(st.session_state.user_id, 7)
    
    if len(recent_data) > 0:
        # Calculate average footprint
        avg_footprint = {
            'transportation': recent_data['transportation_emissions'].mean(),
            'energy': recent_data['energy_emissions'].mean(),
            'food': recent_data['food_emissions'].mean(),
            'waste': recent_data['waste_emissions'].mean(),
            'total': recent_data['total_emissions'].mean()
        }
        
        # Get recommendations
        recommendations = calculator.get_recommendations(avg_footprint)
        
        st.subheader("Personalized Recommendations")
        
        for i, rec in enumerate(recommendations, 1):
            st.write(f"**{i}.** {rec}")
        
        # Impact estimation
        st.subheader("Potential Impact")
        
        impact_estimates = {
            "Switch to electric vehicle": -2000,
            "Reduce meat consumption by 50%": -500,
            "Use renewable energy": -1500,
            "Increase recycling to 80%": -200,
            "Work from home 2 days/week": -800
        }
        
        for action, impact in impact_estimates.items():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(action)
            with col2:
                st.write(f"{impact:+d} kg CO₂/year")
        
        # Future predictions
        st.subheader("Future Projections")
        
        if len(recent_data) >= 7:
            historical_emissions = recent_data['total_emissions'].tolist()
            future_trend = predictor.predict_future_trend(historical_emissions, 30)
            
            # Create projection chart
            dates_historical = recent_data['date'].tolist()
            dates_future = [dates_historical[-1] + timedelta(days=i) for i in range(1, 31)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=dates_historical, y=historical_emissions,
                                   mode='lines+markers', name='Historical'))
            fig.add_trace(go.Scatter(x=dates_future, y=future_trend,
                                   mode='lines', name='Predicted', line=dict(dash='dash')))
            
            fig.update_layout(title="30-Day Emissions Forecast",
                             xaxis_title="Date", yaxis_title="CO₂ Emissions (kg)")
            st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info("Start logging your daily activities to get personalized recommendations!")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("🌱 **EcoTracker** - Making sustainability measurable")
st.sidebar.markdown("Powered by AI & Machine Learning")
