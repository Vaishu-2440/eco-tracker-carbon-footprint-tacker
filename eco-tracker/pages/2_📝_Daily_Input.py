import streamlit as st
import pandas as pd
from datetime import datetime
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from carbon_calculator import CarbonFootprintCalculator
from data_manager import DataManager
from utils import EcoTrackerUtils

st.set_page_config(page_title="Daily Input", page_icon="📝", layout="wide")

# Initialize components
calculator = CarbonFootprintCalculator()
data_manager = DataManager()

st.title("📝 Daily Carbon Footprint Input")

# Check if user is logged in
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.warning("Please create a user profile first from the main app!")
    st.stop()

# Date selection
selected_date = st.date_input("📅 Select Date", datetime.now())

# Create tabs for different categories
tab1, tab2, tab3, tab4 = st.tabs(["🚗 Transportation", "⚡ Energy", "🍽️ Food", "🗑️ Waste"])

# Initialize session state for form data
if 'form_data' not in st.session_state:
    st.session_state.form_data = {}

with tab1:
    st.subheader("🚗 Transportation Activities")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🚙 Personal Vehicle**")
        car_miles = st.number_input("Miles Driven", min_value=0.0, value=0.0, key="car_miles")
        vehicle_type = st.selectbox("Vehicle Type", 
                                   ["car_gasoline", "car_diesel", "car_electric", "car_hybrid"],
                                   key="vehicle_type")
        fuel_efficiency = st.number_input("Fuel Efficiency (MPG)", min_value=1.0, value=25.0, key="mpg")
        
        st.write("**✈️ Air Travel**")
        flight_miles = st.number_input("Flight Miles", min_value=0.0, value=0.0, key="flight_miles")
        flight_type = st.selectbox("Flight Type", ["plane_domestic", "plane_international"], key="flight_type")
    
    with col2:
        st.write("**🚌 Public Transportation**")
        bus_miles = st.number_input("Bus Miles", min_value=0.0, value=0.0, key="bus_miles")
        train_miles = st.number_input("Train Miles", min_value=0.0, value=0.0, key="train_miles")
        subway_miles = st.number_input("Subway Miles", min_value=0.0, value=0.0, key="subway_miles")
        
        st.write("**🚴 Active Transportation**")
        bike_miles = st.number_input("Bicycle Miles", min_value=0.0, value=0.0, key="bike_miles")
        walk_miles = st.number_input("Walking Miles", min_value=0.0, value=0.0, key="walk_miles")

with tab2:
    st.subheader("⚡ Energy Consumption")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🏠 Home Energy**")
        electricity = st.number_input("Electricity (kWh)", min_value=0.0, value=0.0, key="electricity")
        natural_gas = st.number_input("Natural Gas (therms)", min_value=0.0, value=0.0, key="natural_gas")
        heating_oil = st.number_input("Heating Oil (gallons)", min_value=0.0, value=0.0, key="heating_oil")
        
        renewable_energy = st.checkbox("Using Renewable Energy", key="renewable")
        renewable_percent = st.slider("Renewable Energy %", 0, 100, 0, key="renewable_percent") if renewable_energy else 0
    
    with col2:
        st.write("**🏢 Other Energy**")
        propane = st.number_input("Propane (gallons)", min_value=0.0, value=0.0, key="propane")
        wood = st.number_input("Wood (kg)", min_value=0.0, value=0.0, key="wood")
        
        st.write("**🌡️ Climate Control**")
        heating_hours = st.number_input("Heating Hours", min_value=0.0, value=0.0, key="heating_hours")
        cooling_hours = st.number_input("AC Hours", min_value=0.0, value=0.0, key="cooling_hours")

with tab3:
    st.subheader("🍽️ Food Consumption")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🥩 Meat & Protein**")
        beef_servings = st.number_input("Beef Servings", min_value=0, value=0, key="beef")
        pork_servings = st.number_input("Pork Servings", min_value=0, value=0, key="pork")
        chicken_servings = st.number_input("Chicken Servings", min_value=0, value=0, key="chicken")
        fish_servings = st.number_input("Fish Servings", min_value=0, value=0, key="fish")
        
        st.write("**🥛 Dairy & Eggs**")
        dairy_servings = st.number_input("Dairy Servings", min_value=0, value=0, key="dairy")
        egg_servings = st.number_input("Egg Servings", min_value=0, value=0, key="eggs")
    
    with col2:
        st.write("**🥬 Plant-Based**")
        vegetable_servings = st.number_input("Vegetable Servings", min_value=0, value=0, key="vegetables")
        fruit_servings = st.number_input("Fruit Servings", min_value=0, value=0, key="fruits")
        grain_servings = st.number_input("Grain Servings", min_value=0, value=0, key="grains")
        
        st.write("**🌱 Food Choices**")
        local_food_percent = st.slider("Local Food %", 0, 100, 30, key="local_food")
        organic_percent = st.slider("Organic Food %", 0, 100, 20, key="organic_food")
        food_waste = st.number_input("Food Waste (kg)", min_value=0.0, value=0.0, key="food_waste")

with tab4:
    st.subheader("🗑️ Waste Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**🗑️ Waste Generation**")
        total_waste = st.number_input("Total Waste (kg)", min_value=0.0, value=0.0, key="total_waste")
        recycling_percent = st.slider("Recycling Rate %", 0, 100, 50, key="recycling_percent")
        composting_percent = st.slider("Composting Rate %", 0, 100, 20, key="composting_percent")
    
    with col2:
        st.write("**♻️ Waste Types**")
        plastic_waste = st.number_input("Plastic Waste (kg)", min_value=0.0, value=0.0, key="plastic_waste")
        paper_waste = st.number_input("Paper Waste (kg)", min_value=0.0, value=0.0, key="paper_waste")
        electronic_waste = st.number_input("E-Waste (kg)", min_value=0.0, value=0.0, key="ewaste")
        
        st.write("**🛍️ Consumption**")
        new_purchases = st.number_input("New Items Purchased", min_value=0, value=0, key="purchases")
        reused_items = st.number_input("Items Reused/Repaired", min_value=0, value=0, key="reused")

# Calculate and save footprint
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    if st.button("🧮 Calculate & Save Daily Footprint", type="primary", use_container_width=True):
        # Prepare data for calculator
        user_data = {
            'transportation': {
                vehicle_type: {'distance': car_miles, 'frequency': 1},
                'bus': {'distance': bus_miles, 'frequency': 1},
                'train': {'distance': train_miles, 'frequency': 1},
                flight_type: {'distance': flight_miles, 'frequency': 1},
                'bicycle': {'distance': bike_miles, 'frequency': 1},
                'walking': {'distance': walk_miles, 'frequency': 1}
            },
            'energy': {
                'electricity': electricity * (1 - renewable_percent/100),
                'natural_gas': natural_gas,
                'heating_oil': heating_oil,
                'propane': propane
            },
            'food': {
                'beef': beef_servings * 0.25,  # Approximate kg per serving
                'pork': pork_servings * 0.2,
                'chicken': chicken_servings * 0.2,
                'fish': fish_servings * 0.15,
                'dairy': dairy_servings * 0.1,
                'eggs': egg_servings * 0.05,
                'vegetables': vegetable_servings * 0.1,
                'fruits': fruit_servings * 0.08,
                'grains': grain_servings * 0.05
            },
            'waste': {
                'landfill': total_waste * (1 - recycling_percent/100 - composting_percent/100),
                'recycling': total_waste * (recycling_percent/100),
                'composting': total_waste * (composting_percent/100)
            }
        }
        
        # Validate input
        is_valid, errors = EcoTrackerUtils.validate_user_input(user_data)
        
        if not is_valid:
            st.error("Input validation failed:")
            for error in errors:
                st.error(f"• {error}")
        else:
            # Calculate emissions
            footprint_data = calculator.calculate_total_footprint(user_data)
            
            # Save to database
            data_manager.save_daily_footprint(
                st.session_state.user_id,
                selected_date.strftime('%Y-%m-%d'),
                footprint_data
            )
            
            # Save individual activities
            activities_to_save = [
                ('transportation', 'car_travel', car_miles, 'miles', footprint_data.get('transportation', 0)),
                ('energy', 'electricity', electricity, 'kWh', electricity * 0.92),
                ('food', 'total_food', sum([beef_servings, chicken_servings, fish_servings]), 'servings', footprint_data.get('food', 0)),
                ('waste', 'total_waste', total_waste, 'kg', footprint_data.get('waste', 0))
            ]
            
            for category, activity_type, amount, unit, emissions in activities_to_save:
                if amount > 0:
                    data_manager.save_activity(
                        st.session_state.user_id,
                        selected_date.strftime('%Y-%m-%d'),
                        category, activity_type, amount, unit, emissions
                    )
            
            # Display results
            st.success("✅ Daily footprint calculated and saved!")
            
            # Show breakdown
            st.subheader("📊 Today's Footprint Breakdown")
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("🚗 Transportation", f"{footprint_data.get('transportation', 0):.1f} kg CO₂")
            with col2:
                st.metric("⚡ Energy", f"{footprint_data.get('energy', 0):.1f} kg CO₂")
            with col3:
                st.metric("🍽️ Food", f"{footprint_data.get('food', 0):.1f} kg CO₂")
            with col4:
                st.metric("🗑️ Waste", f"{footprint_data.get('waste', 0):.1f} kg CO₂")
            with col5:
                st.metric("🌍 **Total**", f"{footprint_data.get('total', 0):.1f} kg CO₂")
            
            # Show sustainability score
            score, grade = EcoTrackerUtils.get_sustainability_score(footprint_data)
            st.info(f"🏆 Today's Sustainability Score: **{score}/100 ({grade})**")
            
            # Quick recommendations
            recommendations = calculator.get_recommendations(footprint_data)
            if recommendations:
                st.subheader("💡 Quick Tips for Tomorrow")
                for i, rec in enumerate(recommendations[:3], 1):
                    st.write(f"{i}. {rec}")

# Quick input templates
st.sidebar.subheader("⚡ Quick Templates")

if st.sidebar.button("🏠 Work From Home Day"):
    st.session_state.update({
        'car_miles': 0,
        'bus_miles': 0,
        'train_miles': 0,
        'electricity': 35,  # Higher home usage
        'heating_hours': 8
    })
    st.rerun()

if st.sidebar.button("🚗 Commute Day"):
    st.session_state.update({
        'car_miles': 30,
        'electricity': 25,
        'bus_miles': 5
    })
    st.rerun()

if st.sidebar.button("✈️ Travel Day"):
    st.session_state.update({
        'flight_miles': 500,
        'car_miles': 50
    })
    st.rerun()

if st.sidebar.button("🌱 Eco Day"):
    st.session_state.update({
        'bike_miles': 10,
        'walk_miles': 3,
        'vegetable_servings': 8,
        'recycling_percent': 90,
        'composting_percent': 50
    })
    st.rerun()

# Clear form
if st.sidebar.button("🔄 Clear Form"):
    for key in list(st.session_state.keys()):
        if key not in ['user_id']:
            del st.session_state[key]
    st.rerun()
