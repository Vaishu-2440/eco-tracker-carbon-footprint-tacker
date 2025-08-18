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

st.set_page_config(page_title="Goals", page_icon="🎯", layout="wide")

data_manager = DataManager()

st.title("🎯 Carbon Reduction Goals")

# Check if user is logged in
if 'user_id' not in st.session_state or st.session_state.user_id is None:
    st.warning("Please create a user profile first from the main app!")
    st.stop()

user_id = st.session_state.user_id

# Create new goal section
st.subheader("➕ Create New Goal")

with st.form("new_goal_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        goal_type = st.selectbox("Goal Type", [
            "Daily Emissions Reduction",
            "Weekly Emissions Target", 
            "Monthly Emissions Limit",
            "Annual Footprint Goal",
            "Category-Specific Reduction"
        ])
    
    with col2:
        target_value = st.number_input("Target Value (kg CO₂)", min_value=0.1, value=10.0, step=0.1)
        target_date = st.date_input("Target Date", datetime.now() + timedelta(days=30))
    
    with col3:
        goal_description = st.text_area("Goal Description (optional)", 
                                       placeholder="Describe your goal...")
    
    create_goal = st.form_submit_button("🎯 Create Goal", type="primary")
    
    if create_goal:
        goal_id = data_manager.create_goal(
            user_id, goal_type, target_value, target_date.strftime('%Y-%m-%d')
        )
        st.success(f"✅ Goal created successfully! (ID: {goal_id})")
        st.rerun()

# Display existing goals
st.subheader("📋 Your Active Goals")

goals = data_manager.get_user_goals(user_id)

if len(goals) > 0:
    # Get recent data for progress calculation
    recent_data = data_manager.get_footprint_history(user_id, 30)
    
    for _, goal in goals.iterrows():
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.write(f"**{goal['goal_type']}**")
                if goal_description := goal.get('description'):
                    st.write(goal_description)
            
            with col2:
                # Calculate current progress
                if len(recent_data) > 0:
                    if "Daily" in goal['goal_type']:
                        current_value = recent_data['total_emissions'].tail(7).mean()
                    elif "Weekly" in goal['goal_type']:
                        current_value = recent_data['total_emissions'].tail(7).sum()
                    elif "Monthly" in goal['goal_type']:
                        current_value = recent_data['total_emissions'].sum()
                    else:
                        current_value = recent_data['total_emissions'].mean() * 365
                    
                    # Update goal progress
                    data_manager.update_goal_progress(goal['id'], current_value)
                else:
                    current_value = 0
                
                progress_percent = min((current_value / goal['target_value']) * 100, 100) if goal['target_value'] > 0 else 0
                
                # For reduction goals, invert the progress calculation
                if "Reduction" in goal['goal_type'] or "Limit" in goal['goal_type']:
                    if current_value <= goal['target_value']:
                        progress_percent = 100
                        status_color = "green"
                    else:
                        progress_percent = (goal['target_value'] / current_value) * 100
                        status_color = "red" if progress_percent < 50 else "orange"
                else:
                    status_color = "green" if progress_percent >= 100 else "orange" if progress_percent >= 70 else "red"
                
                st.metric("Current", f"{current_value:.1f} kg CO₂")
                st.metric("Target", f"{goal['target_value']:.1f} kg CO₂")
            
            with col3:
                # Progress bar
                st.write("**Progress**")
                progress_bar = st.progress(min(progress_percent / 100, 1.0))
                st.write(f"{progress_percent:.1f}%")
                
                # Days remaining
                if goal['target_date']:
                    days_left = (pd.to_datetime(goal['target_date']) - pd.Timestamp.now()).days
                    if days_left > 0:
                        st.write(f"⏰ {days_left} days left")
                    else:
                        st.write("⏰ Goal deadline passed")
            
            # Goal status indicator
            if progress_percent >= 100:
                st.success("🎉 Goal achieved!")
            elif progress_percent >= 70:
                st.warning("⚠️ Close to target")
            else:
                st.error("❌ Needs attention")
            
            st.markdown("---")

else:
    st.info("🎯 No goals set yet. Create your first goal above!")

# Goal suggestions
st.subheader("💡 Suggested Goals")

if len(recent_data) > 0:
    current_avg = recent_data['total_emissions'].mean()
    
    suggested_goals = [
        {
            "type": "Daily Emissions Reduction",
            "target": current_avg * 0.9,
            "description": f"Reduce daily emissions by 10% (from {current_avg:.1f} to {current_avg * 0.9:.1f} kg CO₂)"
        },
        {
            "type": "Weekly Emissions Target",
            "target": current_avg * 7 * 0.85,
            "description": f"Keep weekly emissions under {current_avg * 7 * 0.85:.1f} kg CO₂"
        },
        {
            "type": "Annual Footprint Goal",
            "target": 8000,  # Below US average
            "description": "Achieve below-average annual footprint (8000 kg CO₂/year)"
        }
    ]
    
    for suggestion in suggested_goals:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{suggestion['type']}**")
            st.write(suggestion['description'])
        with col2:
            if st.button(f"Add Goal", key=f"add_{suggestion['type']}"):
                goal_id = data_manager.create_goal(
                    user_id, 
                    suggestion['type'], 
                    suggestion['target'],
                    (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
                )
                st.success("Goal added!")
                st.rerun()

# Goal achievement statistics
st.subheader("🏆 Achievement Statistics")

if len(goals) > 0:
    achieved_goals = len(goals[goals['current_value'] <= goals['target_value']])
    total_goals = len(goals)
    achievement_rate = (achieved_goals / total_goals) * 100 if total_goals > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Goals Achieved", f"{achieved_goals}/{total_goals}")
    with col2:
        st.metric("Achievement Rate", f"{achievement_rate:.1f}%")
    with col3:
        avg_progress = goals.apply(
            lambda row: min((row['current_value'] / row['target_value']) * 100, 100) if row['target_value'] > 0 else 0,
            axis=1
        ).mean()
        st.metric("Average Progress", f"{avg_progress:.1f}%")

# Tips for goal setting
with st.expander("💡 Goal Setting Tips"):
    st.markdown("""
    **SMART Goals for Carbon Reduction:**
    
    - **Specific**: Target exact emission categories or activities
    - **Measurable**: Use concrete numbers (kg CO₂, percentages)
    - **Achievable**: Set realistic targets based on your current footprint
    - **Relevant**: Focus on your highest emission categories
    - **Time-bound**: Set clear deadlines
    
    **Example Goals:**
    - Reduce daily car travel by 20% within 2 months
    - Achieve 80% recycling rate by end of year
    - Limit monthly electricity to 800 kWh
    - Take only 1 flight this year instead of 3
    """)
