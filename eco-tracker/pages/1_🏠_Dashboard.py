import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_manager import DataManager
from utils import EcoTrackerUtils

st.set_page_config(page_title="Dashboard", page_icon="🏠", layout="wide")

# Initialize data manager
data_manager = DataManager()

st.title("🏠 Dashboard Overview")

# Check if user is logged in
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.warning("Please create a user profile first from the main app!")
    st.stop()

# Get user data
user_id = st.session_state.user_id
recent_data = data_manager.get_footprint_history(user_id, 30)

if len(recent_data) > 0:
    # Key Performance Indicators
    st.subheader("📊 Key Metrics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        today_emissions = recent_data['total_emissions'].iloc[-1] if len(recent_data) > 0 else 0
        st.metric("Today's Emissions", f"{today_emissions:.1f} kg CO₂")
    
    with col2:
        avg_daily = recent_data['total_emissions'].mean()
        st.metric("30-Day Average", f"{avg_daily:.1f} kg CO₂")
    
    with col3:
        monthly_total = recent_data['total_emissions'].sum()
        st.metric("Monthly Total", f"{monthly_total:.1f} kg CO₂")
    
    with col4:
        # Calculate sustainability score
        avg_footprint = {'total': avg_daily}
        score, grade = EcoTrackerUtils.get_sustainability_score(avg_footprint)
        st.metric("Sustainability Score", f"{score}/100 ({grade})")
    
    with col5:
        # Trend indicator
        if len(recent_data) >= 7:
            recent_avg = recent_data['total_emissions'].tail(7).mean()
            older_avg = recent_data['total_emissions'].head(7).mean()
            trend = "📈" if recent_avg > older_avg else "📉"
            change = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
            st.metric("7-Day Trend", trend, f"{change:+.1f}%")
        else:
            st.metric("7-Day Trend", "📊", "Insufficient data")
    
    # Main charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Emissions timeline
        st.subheader("📈 Emissions Timeline")
        fig_timeline = px.line(recent_data, x='date', y='total_emissions',
                              title="Daily Carbon Footprint")
        fig_timeline.update_traces(line_color='#2E8B57')
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    with col2:
        # Category breakdown
        st.subheader("🥧 Category Breakdown")
        categories = ['transportation_emissions', 'energy_emissions', 
                     'food_emissions', 'waste_emissions']
        category_names = ['Transportation', 'Energy', 'Food', 'Waste']
        category_totals = recent_data[categories].sum()
        
        fig_pie = px.pie(values=category_totals.values, names=category_names,
                        title="Emissions by Category",
                        color_discrete_sequence=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4'])
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Weekly pattern analysis
    st.subheader("📅 Weekly Patterns")
    if len(recent_data) >= 7:
        recent_data['day_of_week'] = pd.to_datetime(recent_data['date']).dt.day_name()
        daily_avg = recent_data.groupby('day_of_week')['total_emissions'].mean().reindex([
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        ])
        
        fig_weekly = px.bar(x=daily_avg.index, y=daily_avg.values,
                           title="Average Emissions by Day of Week",
                           color=daily_avg.values,
                           color_continuous_scale='RdYlGn_r')
        fig_weekly.update_layout(xaxis_title="Day", yaxis_title="CO₂ Emissions (kg)")
        st.plotly_chart(fig_weekly, use_container_width=True)
    
    # Recent activities summary
    st.subheader("📋 Recent Activity Summary")
    activities = data_manager.get_activities(user_id, days=7)
    
    if len(activities) > 0:
        # Group by category
        activity_summary = activities.groupby('category').agg({
            'emissions': 'sum',
            'amount': 'sum'
        }).round(2)
        
        st.dataframe(activity_summary, use_container_width=True)
    else:
        st.info("No recent activities logged. Start tracking your daily activities!")
    
    # Quick stats
    st.subheader("📊 Quick Statistics")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        best_day = recent_data.loc[recent_data['total_emissions'].idxmin()]
        st.write(f"**Best Day:** {best_day['date'].strftime('%Y-%m-%d')}")
        st.write(f"Emissions: {best_day['total_emissions']:.1f} kg CO₂")
    
    with col2:
        worst_day = recent_data.loc[recent_data['total_emissions'].idxmax()]
        st.write(f"**Highest Day:** {worst_day['date'].strftime('%Y-%m-%d')}")
        st.write(f"Emissions: {worst_day['total_emissions']:.1f} kg CO₂")
    
    with col3:
        improvement = ((recent_data['total_emissions'].iloc[0] - recent_data['total_emissions'].iloc[-1]) 
                      / recent_data['total_emissions'].iloc[0] * 100) if len(recent_data) > 1 else 0
        st.write(f"**30-Day Change:** {improvement:+.1f}%")
        if improvement > 0:
            st.write("🎉 Great improvement!")
        elif improvement < -10:
            st.write("⚠️ Consider reviewing habits")
        else:
            st.write("📊 Stable emissions")

else:
    st.info("📝 No data available yet. Start by logging your daily activities in the Daily Input page!")
    
    # Show sample data structure
    st.subheader("💡 Getting Started")
    st.write("Here's what you can track:")
    
    sample_data = {
        "Transportation": ["Car miles", "Public transport", "Flights", "Cycling"],
        "Energy": ["Electricity usage", "Natural gas", "Heating oil", "Renewable energy"],
        "Food": ["Meat consumption", "Dairy products", "Local produce", "Food waste"],
        "Waste": ["Landfill waste", "Recycling", "Composting", "Electronic waste"]
    }
    
    for category, items in sample_data.items():
        st.write(f"**{category}:** {', '.join(items)}")

# Sidebar with quick actions
st.sidebar.subheader("🚀 Quick Actions")
if st.sidebar.button("📝 Log Today's Activities"):
    st.switch_page("pages/2_📝_Daily_Input.py")

if st.sidebar.button("🤖 Get AI Predictions"):
    st.switch_page("pages/3_🤖_AI_Predictions.py")

if st.sidebar.button("📈 View Analytics"):
    st.switch_page("pages/4_📈_Analytics.py")
