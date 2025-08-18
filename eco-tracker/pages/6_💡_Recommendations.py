import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import sys
import os

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_manager import DataManager
from ai_recommendations import AIRecommendationEngine
from carbon_calculator import CarbonFootprintCalculator

st.set_page_config(page_title="Recommendations", page_icon="💡", layout="wide")

# Initialize components
data_manager = DataManager()
ai_engine = AIRecommendationEngine()
calculator = CarbonFootprintCalculator()

st.title("💡 AI-Powered Recommendations")

# Check if user is logged in
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.warning("Please create a user profile first from the main app!")
    st.stop()

user_id = st.session_state.user_id

# Get user data
recent_data = data_manager.get_footprint_history(user_id, 30)

if len(recent_data) > 0:
    # Calculate average footprint
    avg_footprint = {
        'transportation': recent_data['transportation_emissions'].mean(),
        'energy': recent_data['energy_emissions'].mean(),
        'food': recent_data['food_emissions'].mean(),
        'waste': recent_data['waste_emissions'].mean(),
        'total': recent_data['total_emissions'].mean()
    }
    
    # Analyze patterns
    user_patterns = ai_engine.analyze_user_pattern(recent_data)
    
    # Get personalized recommendations
    recommendations = ai_engine.get_personalized_recommendations(avg_footprint, user_patterns)
    
    # Display pattern analysis
    st.subheader("🔍 Your Emission Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**📊 Identified Patterns:**")
        for pattern in user_patterns['patterns']:
            st.info(f"• {pattern}")
    
    with col2:
        st.write("**🎯 Improvement Opportunities:**")
        for opportunity in user_patterns['opportunities']:
            st.warning(f"• {opportunity}")
    
    # Main recommendations
    st.subheader("🚀 Personalized Action Plan")
    
    if recommendations:
        # Create action plan
        action_plan = ai_engine.generate_action_plan(recommendations, 12)
        
        # Display action plan in tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🏃 Quick Wins (Weeks 1-2)", "🔄 Habit Changes (Weeks 3-6)", 
                                         "🏗️ Major Changes (Weeks 7-12)", "📊 Full Analysis"])
        
        with tab1:
            st.write("**Focus: Easy implementations with immediate impact**")
            quick_wins = action_plan['weeks_1_2']
            
            for i, action in enumerate(quick_wins['actions'], 1):
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{i}. {action['recommendation']}**")
                        st.write(f"*Category: {action['category']}*")
                    
                    with col2:
                        impact_color = "green" if action['impact_estimate'] < -100 else "orange"
                        st.metric("Impact", f"{action['impact_estimate']:+d} kg CO₂/year")
                    
                    with col3:
                        difficulty_color = {"Low": "green", "Medium": "orange", "High": "red"}[action['difficulty']]
                        st.write(f"**Difficulty:** {action['difficulty']}")
                        st.write(f"**Priority:** {action['priority']}/10")
            
            st.success(f"💚 Expected total reduction: {quick_wins['expected_reduction']:.0f} kg CO₂/year")
        
        with tab2:
            st.write("**Focus: Building sustainable habits**")
            habit_changes = action_plan['weeks_3_6']
            
            for i, action in enumerate(habit_changes['actions'], 1):
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{i}. {action['recommendation']}**")
                        st.write(f"*Category: {action['category']}*")
                    
                    with col2:
                        st.metric("Impact", f"{action['impact_estimate']:+d} kg CO₂/year")
                    
                    with col3:
                        st.write(f"**Difficulty:** {action['difficulty']}")
                        st.write(f"**Priority:** {action['priority']}/10")
            
            st.info(f"🔄 Expected total reduction: {habit_changes['expected_reduction']:.0f} kg CO₂/year")
        
        with tab3:
            st.write("**Focus: Significant lifestyle or infrastructure changes**")
            major_changes = action_plan['weeks_7_12']
            
            for i, action in enumerate(major_changes['actions'], 1):
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.write(f"**{i}. {action['recommendation']}**")
                        st.write(f"*Category: {action['category']}*")
                    
                    with col2:
                        st.metric("Impact", f"{action['impact_estimate']:+d} kg CO₂/year")
                    
                    with col3:
                        st.write(f"**Difficulty:** {action['difficulty']}")
                        st.write(f"**Priority:** {action['priority']}/10")
            
            st.warning(f"🏗️ Expected total reduction: {major_changes['expected_reduction']:.0f} kg CO₂/year")
        
        with tab4:
            st.write("**Complete Recommendation Analysis**")
            
            # Total potential impact
            total_reduction = action_plan['total_potential_reduction']
            current_annual = avg_footprint['total'] * 365
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Current Annual", f"{current_annual:.0f} kg CO₂")
            with col2:
                st.metric("Potential Reduction", f"{total_reduction:.0f} kg CO₂")
            with col3:
                final_footprint = current_annual - total_reduction
                st.metric("Potential Final", f"{final_footprint:.0f} kg CO₂")
            
            # Impact visualization
            fig_impact = go.Figure(go.Waterfall(
                name="Carbon Reduction Plan",
                orientation="v",
                measure=["absolute", "relative", "relative", "relative", "total"],
                x=["Current", "Quick Wins", "Habit Changes", "Major Changes", "Final"],
                textposition="outside",
                text=[f"{current_annual:.0f}", f"-{quick_wins['expected_reduction']:.0f}", 
                      f"-{habit_changes['expected_reduction']:.0f}", 
                      f"-{major_changes['expected_reduction']:.0f}", f"{final_footprint:.0f}"],
                y=[current_annual, -quick_wins['expected_reduction'], 
                   -habit_changes['expected_reduction'], -major_changes['expected_reduction'], 
                   final_footprint],
                connector={"line": {"color": "rgb(63, 63, 63)"}},
            ))
            
            fig_impact.update_layout(
                title="Carbon Reduction Impact Plan",
                yaxis_title="CO₂ Emissions (kg/year)"
            )
            st.plotly_chart(fig_impact, use_container_width=True)
    
    # Seasonal recommendations
    st.subheader("🌍 Seasonal Recommendations")
    current_month = datetime.now().month
    seasonal_recs = ai_engine.get_seasonal_recommendations(current_month)
    
    for i, rec in enumerate(seasonal_recs, 1):
        st.write(f"**{i}.** {rec}")
    
    # Community challenges
    st.subheader("🏆 Community Challenges")
    challenges = ai_engine.get_community_challenges()
    
    for challenge in challenges[:3]:
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{challenge['name']}**")
                st.write(challenge['description'])
            
            with col2:
                st.metric("Duration", challenge['duration'])
                st.metric("Impact", f"{challenge['estimated_impact']:+d} kg CO₂")
            
            with col3:
                difficulty_colors = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
                st.write(f"**Difficulty:** {difficulty_colors[challenge['difficulty']]} {challenge['difficulty']}")
                
                if st.button(f"Join Challenge", key=f"join_{challenge['name']}"):
                    st.success(f"🎉 Joined {challenge['name']}! Good luck!")
    
    # Benchmark comparison
    st.subheader("📊 How You Compare")
    benchmarks = ai_engine.benchmark_against_peers(avg_footprint)
    
    comparison_data = []
    for benchmark_name, data in benchmarks.items():
        comparison_data.append({
            'Benchmark': benchmark_name.replace('_', ' ').title(),
            'Value': data['value'],
            'Your Emissions': avg_footprint['total'] * 365,
            'Difference': data['difference'],
            'Status': '🔴 Above' if data['status'] == 'above' else '🟢 Below'
        })
    
    comparison_df = pd.DataFrame(comparison_data)
    st.dataframe(comparison_df, use_container_width=True)

else:
    st.info("📝 Start logging your daily activities to get personalized recommendations!")
    
    # Show general recommendations
    st.subheader("🌟 General Eco-Friendly Tips")
    
    general_tips = [
        "🚗 **Transportation**: Use public transport, bike, or walk when possible",
        "⚡ **Energy**: Switch to LED bulbs and unplug devices when not in use",
        "🍽️ **Food**: Reduce meat consumption and buy local produce",
        "♻️ **Waste**: Increase recycling and composting rates",
        "🏠 **Home**: Improve insulation and use programmable thermostats",
        "💚 **Lifestyle**: Choose quality items that last longer"
    ]
    
    for tip in general_tips:
        st.markdown(tip)

# Weekly tip
st.sidebar.subheader("💡 Weekly Tip")
current_week = datetime.now().isocalendar()[1]
weekly_tips = ai_engine.generate_weekly_tips(avg_footprint if len(recent_data) > 0 else {'total': 20}, current_week)

for tip in weekly_tips:
    st.sidebar.info(tip)
