import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_manager import DataManager
from visualizations import CarbonFootprintVisualizer
from utils import EcoTrackerUtils

st.set_page_config(page_title="Analytics", page_icon="📈", layout="wide")

# Initialize components
data_manager = DataManager()
visualizer = CarbonFootprintVisualizer()

st.title("📈 Advanced Carbon Footprint Analytics")

# Check if user is logged in
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.warning("Please create a user profile first from the main app!")
    st.stop()

# Time period selection
st.subheader("⏰ Analysis Period")
col1, col2, col3 = st.columns(3)

with col1:
    analysis_period = st.selectbox("Select Period", 
                                  ["Last 7 days", "Last 30 days", "Last 90 days", "Last year"])

with col2:
    start_date = st.date_input("Custom Start Date", datetime.now() - timedelta(days=30))

with col3:
    end_date = st.date_input("Custom End Date", datetime.now())

# Convert period to days
period_mapping = {
    "Last 7 days": 7,
    "Last 30 days": 30,
    "Last 90 days": 90,
    "Last year": 365
}

days = period_mapping.get(analysis_period, 30)
history_data = data_manager.get_footprint_history(st.session_state.user_id, days)

if len(history_data) > 0:
    # Filter by custom date range if specified
    if start_date and end_date:
        history_data = history_data[
            (pd.to_datetime(history_data['date']) >= pd.to_datetime(start_date)) &
            (pd.to_datetime(history_data['date']) <= pd.to_datetime(end_date))
        ]
    
    if len(history_data) == 0:
        st.warning("No data available for the selected date range.")
        st.stop()
    
    # Summary statistics
    st.subheader("📊 Summary Statistics")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_emissions = history_data['total_emissions'].sum()
        st.metric("Total Emissions", f"{total_emissions:.1f} kg CO₂")
    
    with col2:
        avg_emissions = history_data['total_emissions'].mean()
        st.metric("Average Daily", f"{avg_emissions:.1f} kg CO₂")
    
    with col3:
        min_emissions = history_data['total_emissions'].min()
        st.metric("Best Day", f"{min_emissions:.1f} kg CO₂")
    
    with col4:
        max_emissions = history_data['total_emissions'].max()
        st.metric("Highest Day", f"{max_emissions:.1f} kg CO₂")
    
    with col5:
        std_emissions = history_data['total_emissions'].std()
        st.metric("Variability", f"{std_emissions:.1f} kg CO₂")
    
    # Advanced visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🔍 Patterns", "📊 Distributions", "🎯 Benchmarks"])
    
    with tab1:
        st.subheader("Emission Trends Analysis")
        
        # Moving averages
        history_data['7_day_avg'] = history_data['total_emissions'].rolling(window=7, min_periods=1).mean()
        history_data['14_day_avg'] = history_data['total_emissions'].rolling(window=14, min_periods=1).mean()
        
        fig_trends = go.Figure()
        
        fig_trends.add_trace(go.Scatter(
            x=history_data['date'], y=history_data['total_emissions'],
            mode='lines', name='Daily Emissions', 
            line=dict(color='lightblue', width=1)
        ))
        
        fig_trends.add_trace(go.Scatter(
            x=history_data['date'], y=history_data['7_day_avg'],
            mode='lines', name='7-Day Average',
            line=dict(color='blue', width=2)
        ))
        
        fig_trends.add_trace(go.Scatter(
            x=history_data['date'], y=history_data['14_day_avg'],
            mode='lines', name='14-Day Average',
            line=dict(color='darkblue', width=3)
        ))
        
        fig_trends.update_layout(
            title="Emissions Trends with Moving Averages",
            xaxis_title="Date",
            yaxis_title="CO₂ Emissions (kg)"
        )
        st.plotly_chart(fig_trends, use_container_width=True)
        
        # Category trends
        st.subheader("Category Trends")
        categories = ['transportation_emissions', 'energy_emissions', 
                     'food_emissions', 'waste_emissions']
        category_names = ['Transportation', 'Energy', 'Food', 'Waste']
        
        fig_category_trends = go.Figure()
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        
        for cat, name, color in zip(categories, category_names, colors):
            fig_category_trends.add_trace(go.Scatter(
                x=history_data['date'], y=history_data[cat],
                mode='lines', name=name, line=dict(color=color)
            ))
        
        fig_category_trends.update_layout(
            title="Emissions by Category Over Time",
            xaxis_title="Date",
            yaxis_title="CO₂ Emissions (kg)"
        )
        st.plotly_chart(fig_category_trends, use_container_width=True)
    
    with tab2:
        st.subheader("Pattern Analysis")
        
        # Day of week patterns
        if len(history_data) >= 7:
            history_data['day_of_week'] = pd.to_datetime(history_data['date']).dt.day_name()
            daily_patterns = history_data.groupby('day_of_week')['total_emissions'].agg(['mean', 'std']).reindex([
                'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
            ])
            
            fig_daily = go.Figure()
            fig_daily.add_trace(go.Bar(
                x=daily_patterns.index,
                y=daily_patterns['mean'],
                error_y=dict(type='data', array=daily_patterns['std']),
                name='Average Emissions',
                marker_color='skyblue'
            ))
            
            fig_daily.update_layout(
                title="Average Emissions by Day of Week",
                xaxis_title="Day",
                yaxis_title="CO₂ Emissions (kg)"
            )
            st.plotly_chart(fig_daily, use_container_width=True)
        
        # Monthly patterns
        if len(history_data) >= 30:
            history_data['month'] = pd.to_datetime(history_data['date']).dt.month
            monthly_patterns = history_data.groupby('month')['total_emissions'].mean()
            
            month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
            
            fig_monthly = px.line(
                x=[month_names[m-1] for m in monthly_patterns.index],
                y=monthly_patterns.values,
                title="Monthly Emission Patterns",
                markers=True
            )
            fig_monthly.update_layout(xaxis_title="Month", yaxis_title="Average CO₂ Emissions (kg)")
            st.plotly_chart(fig_monthly, use_container_width=True)
    
    with tab3:
        st.subheader("Distribution Analysis")
        
        # Emission distribution histogram
        fig_hist = px.histogram(
            history_data, x='total_emissions',
            title="Distribution of Daily Emissions",
            nbins=20
        )
        fig_hist.update_layout(xaxis_title="CO₂ Emissions (kg)", yaxis_title="Frequency")
        st.plotly_chart(fig_hist, use_container_width=True)
        
        # Box plots by category
        categories_data = []
        for cat in ['transportation_emissions', 'energy_emissions', 'food_emissions', 'waste_emissions']:
            for value in history_data[cat]:
                categories_data.append({
                    'Category': cat.replace('_emissions', '').title(),
                    'Emissions': value
                })
        
        if categories_data:
            df_categories = pd.DataFrame(categories_data)
            fig_box = px.box(df_categories, x='Category', y='Emissions',
                           title="Emission Distribution by Category")
            st.plotly_chart(fig_box, use_container_width=True)
    
    with tab4:
        st.subheader("Benchmark Comparison")
        
        # Calculate user averages
        user_avg_daily = history_data['total_emissions'].mean()
        user_avg_annual = user_avg_daily * 365
        
        # Benchmark data
        benchmarks = {
            'Your Average': user_avg_annual,
            'US Average': 16000,
            'EU Average': 8500,
            'Global Average': 4800,
            'Paris 2030 Target': 2300
        }
        
        # Benchmark comparison chart
        fig_bench = px.bar(
            x=list(benchmarks.keys()),
            y=list(benchmarks.values()),
            title="Annual Footprint vs Global Benchmarks",
            color=list(benchmarks.values()),
            color_continuous_scale='RdYlGn_r'
        )
        st.plotly_chart(fig_bench, use_container_width=True)
        
        # Progress toward targets
        st.subheader("🎯 Progress Toward Climate Targets")
        
        paris_target = 2300
        progress_to_paris = (paris_target / user_avg_annual) * 100 if user_avg_annual > 0 else 0
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Progress to Paris Target", f"{min(progress_to_paris, 100):.1f}%")
        with col2:
            reduction_needed = max(0, user_avg_annual - paris_target)
            st.metric("Reduction Needed", f"{reduction_needed:.0f} kg CO₂/year")
    
    # Insights and recommendations
    st.subheader("🧠 AI Insights")
    
    insights = []
    
    # Trend analysis
    if len(history_data) >= 14:
        recent_avg = history_data['total_emissions'].tail(7).mean()
        older_avg = history_data['total_emissions'].head(7).mean()
        
        if recent_avg > older_avg * 1.1:
            insights.append("📈 Your emissions have increased recently. Consider reviewing your recent activities.")
        elif recent_avg < older_avg * 0.9:
            insights.append("📉 Great progress! Your emissions are decreasing.")
        else:
            insights.append("📊 Your emissions are stable. Look for optimization opportunities.")
    
    # Category analysis
    category_avgs = {
        'Transportation': history_data['transportation_emissions'].mean(),
        'Energy': history_data['energy_emissions'].mean(),
        'Food': history_data['food_emissions'].mean(),
        'Waste': history_data['waste_emissions'].mean()
    }
    
    highest_category = max(category_avgs, key=category_avgs.get)
    insights.append(f"🎯 Your highest emission category is {highest_category}. Focus reduction efforts here.")
    
    # Variability analysis
    cv = history_data['total_emissions'].std() / history_data['total_emissions'].mean()
    if cv > 0.3:
        insights.append("📊 Your emissions vary significantly day-to-day. Consider establishing more consistent routines.")
    else:
        insights.append("📊 Your emissions are consistent, which makes prediction and planning easier.")
    
    for insight in insights:
        st.info(insight)

else:
    st.info("📝 No data available for analysis. Start by logging your daily activities!")
    
    # Show what analytics will be available
    st.subheader("📊 Available Analytics")
    st.write("Once you start logging data, you'll see:")
    
    analytics_features = [
        "📈 **Trend Analysis** - Moving averages and emission trends",
        "📅 **Pattern Recognition** - Daily and monthly patterns",
        "📊 **Statistical Analysis** - Distribution and variability metrics",
        "🎯 **Benchmark Comparisons** - How you compare to global averages",
        "🧠 **AI Insights** - Automated analysis and recommendations",
        "🔮 **Predictive Analytics** - Future emission forecasts"
    ]
    
    for feature in analytics_features:
        st.markdown(feature)

# Export functionality
st.sidebar.subheader("📤 Export Data")
if st.sidebar.button("Export to CSV"):
    if len(history_data) > 0:
        filename = f"carbon_footprint_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        filepath = EcoTrackerUtils.export_to_csv(history_data, filename)
        st.sidebar.success(f"Data exported to {filepath}")
    else:
        st.sidebar.warning("No data to export")

# Analysis settings
st.sidebar.subheader("⚙️ Analysis Settings")
show_moving_avg = st.sidebar.checkbox("Show Moving Averages", True)
show_confidence_bands = st.sidebar.checkbox("Show Confidence Bands", False)
normalize_data = st.sidebar.checkbox("Normalize by Household Size", False)
