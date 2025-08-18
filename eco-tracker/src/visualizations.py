import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib.pyplot as plt

class CarbonFootprintVisualizer:
    """
    Advanced visualization components for carbon footprint data
    """
    
    def __init__(self):
        self.color_palette = {
            'transportation': '#FF6B6B',
            'energy': '#4ECDC4',
            'food': '#45B7D1',
            'waste': '#96CEB4',
            'total': '#2C3E50'
        }
    
    def create_emissions_timeline(self, df: pd.DataFrame) -> go.Figure:
        """Create an interactive timeline of emissions"""
        fig = go.Figure()
        
        # Add total emissions line
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['total_emissions'],
            mode='lines+markers',
            name='Total Emissions',
            line=dict(color=self.color_palette['total'], width=3),
            hovertemplate='<b>%{x}</b><br>Total: %{y:.1f} kg CO₂<extra></extra>'
        ))
        
        # Add category traces
        categories = ['transportation_emissions', 'energy_emissions', 
                     'food_emissions', 'waste_emissions']
        category_names = ['Transportation', 'Energy', 'Food', 'Waste']
        
        for cat, name in zip(categories, category_names):
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df[cat],
                mode='lines',
                name=name,
                line=dict(color=self.color_palette[name.lower()]),
                visible='legendonly',
                hovertemplate=f'<b>%{{x}}</b><br>{name}: %{{y:.1f}} kg CO₂<extra></extra>'
            ))
        
        fig.update_layout(
            title='Carbon Footprint Timeline',
            xaxis_title='Date',
            yaxis_title='CO₂ Emissions (kg)',
            hovermode='x unified',
            showlegend=True
        )
        
        return fig
    
    def create_category_breakdown_pie(self, df: pd.DataFrame) -> go.Figure:
        """Create pie chart for category breakdown"""
        categories = ['transportation_emissions', 'energy_emissions', 
                     'food_emissions', 'waste_emissions']
        category_names = ['Transportation', 'Energy', 'Food', 'Waste']
        
        totals = df[categories].sum()
        
        fig = go.Figure(data=[go.Pie(
            labels=category_names,
            values=totals.values,
            hole=0.3,
            marker_colors=[self.color_palette[name.lower()] for name in category_names],
            textinfo='label+percent',
            textposition='outside'
        )])
        
        fig.update_layout(
            title='Emissions by Category',
            showlegend=True
        )
        
        return fig
    
    def create_stacked_area_chart(self, df: pd.DataFrame) -> go.Figure:
        """Create stacked area chart showing category contributions over time"""
        fig = go.Figure()
        
        categories = ['transportation_emissions', 'energy_emissions', 
                     'food_emissions', 'waste_emissions']
        category_names = ['Transportation', 'Energy', 'Food', 'Waste']
        
        for cat, name in zip(categories, category_names):
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df[cat],
                mode='lines',
                stackgroup='one',
                name=name,
                line=dict(color=self.color_palette[name.lower()]),
                hovertemplate=f'<b>%{{x}}</b><br>{name}: %{{y:.1f}} kg CO₂<extra></extra>'
            ))
        
        fig.update_layout(
            title='Emissions Categories Over Time',
            xaxis_title='Date',
            yaxis_title='CO₂ Emissions (kg)',
            hovermode='x unified'
        )
        
        return fig
    
    def create_weekly_pattern_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """Create heatmap showing weekly emission patterns"""
        # Add day of week and week number
        df_copy = df.copy()
        df_copy['day_of_week'] = pd.to_datetime(df_copy['date']).dt.day_name()
        df_copy['week'] = pd.to_datetime(df_copy['date']).dt.isocalendar().week
        
        # Create pivot table
        pivot_data = df_copy.pivot_table(
            values='total_emissions',
            index='week',
            columns='day_of_week',
            aggfunc='mean'
        )
        
        # Reorder columns to start with Monday
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        pivot_data = pivot_data.reindex(columns=day_order)
        
        fig = go.Figure(data=go.Heatmap(
            z=pivot_data.values,
            x=pivot_data.columns,
            y=pivot_data.index,
            colorscale='RdYlBu_r',
            hovertemplate='<b>Week %{y}, %{x}</b><br>Emissions: %{z:.1f} kg CO₂<extra></extra>'
        ))
        
        fig.update_layout(
            title='Weekly Emission Patterns',
            xaxis_title='Day of Week',
            yaxis_title='Week Number'
        )
        
        return fig
    
    def create_comparison_radar_chart(self, user_data: dict, benchmarks: dict) -> go.Figure:
        """Create radar chart comparing user data to benchmarks"""
        categories = list(user_data.keys())
        
        fig = go.Figure()
        
        # User data
        fig.add_trace(go.Scatterpolar(
            r=list(user_data.values()),
            theta=categories,
            fill='toself',
            name='Your Footprint',
            line_color='rgb(255, 99, 71)'
        ))
        
        # Benchmark data
        fig.add_trace(go.Scatterpolar(
            r=list(benchmarks.values()),
            theta=categories,
            fill='toself',
            name='Average Footprint',
            line_color='rgb(70, 130, 180)'
        ))
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, max(max(user_data.values()), max(benchmarks.values()))]
                )
            ),
            showlegend=True,
            title='Footprint Comparison'
        )
        
        return fig
    
    def create_goal_progress_chart(self, goals_df: pd.DataFrame) -> go.Figure:
        """Create progress chart for goals"""
        fig = go.Figure()
        
        for _, goal in goals_df.iterrows():
            progress = min(goal['current_value'] / goal['target_value'], 1.0) if goal['target_value'] > 0 else 0
            
            fig.add_trace(go.Bar(
                x=[goal['goal_type']],
                y=[progress * 100],
                name=goal['goal_type'],
                text=f"{progress:.1%}",
                textposition='auto',
                marker_color='green' if progress >= 1.0 else 'orange' if progress >= 0.7 else 'red'
            ))
        
        fig.update_layout(
            title='Goal Progress',
            xaxis_title='Goals',
            yaxis_title='Progress (%)',
            yaxis=dict(range=[0, 100]),
            showlegend=False
        )
        
        return fig
    
    def create_prediction_confidence_chart(self, predictions: list, confidence_intervals: list) -> go.Figure:
        """Create chart showing predictions with confidence intervals"""
        dates = [datetime.now() + timedelta(days=i) for i in range(len(predictions))]
        
        fig = go.Figure()
        
        # Add confidence interval
        fig.add_trace(go.Scatter(
            x=dates + dates[::-1],
            y=confidence_intervals[1] + confidence_intervals[0][::-1],
            fill='toself',
            fillcolor='rgba(0,100,80,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            hoverinfo="skip",
            showlegend=False,
            name='Confidence Interval'
        ))
        
        # Add prediction line
        fig.add_trace(go.Scatter(
            x=dates,
            y=predictions,
            mode='lines+markers',
            name='Predicted Emissions',
            line=dict(color='rgb(31, 119, 180)'),
            hovertemplate='<b>%{x}</b><br>Predicted: %{y:.1f} kg CO₂<extra></extra>'
        ))
        
        fig.update_layout(
            title='Emission Predictions with Confidence Intervals',
            xaxis_title='Date',
            yaxis_title='CO₂ Emissions (kg)',
            hovermode='x'
        )
        
        return fig
    
    def create_impact_waterfall_chart(self, baseline: float, actions: dict) -> go.Figure:
        """Create waterfall chart showing impact of different actions"""
        x_labels = ['Baseline'] + list(actions.keys()) + ['Final']
        y_values = [baseline]
        
        running_total = baseline
        for impact in actions.values():
            running_total += impact
            y_values.append(running_total)
        
        # Create waterfall effect
        fig = go.Figure(go.Waterfall(
            name="Carbon Reduction",
            orientation="v",
            measure=["absolute"] + ["relative"] * len(actions) + ["total"],
            x=x_labels,
            textposition="outside",
            text=[f"{v:.0f}" for v in y_values],
            y=[baseline] + list(actions.values()) + [running_total],
            connector={"line": {"color": "rgb(63, 63, 63)"}},
        ))
        
        fig.update_layout(
            title="Carbon Reduction Impact Analysis",
            showlegend=False,
            yaxis_title="CO₂ Emissions (kg/year)"
        )
        
        return fig
    
    def create_seasonal_analysis(self, df: pd.DataFrame) -> go.Figure:
        """Create seasonal analysis chart"""
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['date'])
        df_copy['month'] = df_copy['date'].dt.month
        df_copy['season'] = df_copy['month'].map({
            12: 'Winter', 1: 'Winter', 2: 'Winter',
            3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer',
            9: 'Fall', 10: 'Fall', 11: 'Fall'
        })
        
        seasonal_data = df_copy.groupby('season')['total_emissions'].agg(['mean', 'std']).reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=seasonal_data['season'],
            y=seasonal_data['mean'],
            error_y=dict(type='data', array=seasonal_data['std']),
            name='Average Emissions',
            marker_color=['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
        ))
        
        fig.update_layout(
            title='Seasonal Emission Patterns',
            xaxis_title='Season',
            yaxis_title='Average CO₂ Emissions (kg)',
            showlegend=False
        )
        
        return fig
