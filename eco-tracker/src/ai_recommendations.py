import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import json

class AIRecommendationEngine:
    """
    Advanced AI-powered recommendation system for carbon footprint reduction
    """
    
    def __init__(self):
        self.recommendation_database = self._load_recommendation_database()
        self.impact_estimates = self._load_impact_estimates()
        
    def _load_recommendation_database(self) -> Dict:
        """Load comprehensive recommendation database"""
        return {
            'transportation': {
                'high_emissions': [
                    "Switch to an electric or hybrid vehicle - can reduce emissions by 40-60%",
                    "Use public transportation for daily commutes",
                    "Implement carpooling or ride-sharing for regular trips",
                    "Work from home 2-3 days per week if possible",
                    "Combine multiple errands into single trips",
                    "Consider cycling or walking for short distances (<3 miles)",
                    "Plan vacations closer to home to reduce flight emissions",
                    "Use video conferencing instead of business travel"
                ],
                'medium_emissions': [
                    "Maintain your vehicle properly for better fuel efficiency",
                    "Plan routes efficiently to minimize driving time",
                    "Use eco-driving techniques (smooth acceleration, steady speeds)",
                    "Consider upgrading to a more fuel-efficient vehicle",
                    "Use public transport for longer trips"
                ],
                'low_emissions': [
                    "Great job! Your transportation emissions are low",
                    "Continue using sustainable transport options",
                    "Share your transportation habits with friends and family"
                ]
            },
            'energy': {
                'high_emissions': [
                    "Switch to renewable energy sources (solar, wind)",
                    "Improve home insulation to reduce heating/cooling needs",
                    "Upgrade to energy-efficient appliances (ENERGY STAR rated)",
                    "Install a programmable thermostat",
                    "Replace incandescent bulbs with LED lighting",
                    "Unplug electronics when not in use",
                    "Use cold water for washing clothes when possible",
                    "Consider a heat pump for heating and cooling"
                ],
                'medium_emissions': [
                    "Set thermostat 2-3 degrees lower in winter, higher in summer",
                    "Use natural light during the day",
                    "Air-dry clothes instead of using the dryer",
                    "Seal air leaks around windows and doors"
                ],
                'low_emissions': [
                    "Excellent energy management!",
                    "Continue your energy-efficient practices",
                    "Consider sharing tips with neighbors"
                ]
            },
            'food': {
                'high_emissions': [
                    "Reduce red meat consumption (beef, lamb) by 50%",
                    "Try 'Meatless Monday' or plant-based meals 2-3 times per week",
                    "Buy local and seasonal produce when possible",
                    "Reduce food waste through meal planning",
                    "Grow your own herbs and vegetables",
                    "Choose organic and sustainably produced foods",
                    "Reduce dairy consumption or try plant-based alternatives",
                    "Avoid heavily processed and packaged foods"
                ],
                'medium_emissions': [
                    "Plan meals in advance to reduce waste",
                    "Choose chicken or fish over red meat",
                    "Buy from local farmers markets",
                    "Compost food scraps"
                ],
                'low_emissions': [
                    "Your food choices are climate-friendly!",
                    "Keep up the sustainable eating habits",
                    "Consider sharing recipes with others"
                ]
            },
            'waste': {
                'high_emissions': [
                    "Increase recycling rate to 80% or higher",
                    "Start composting organic waste",
                    "Reduce single-use items (bags, bottles, containers)",
                    "Buy products with minimal packaging",
                    "Donate or sell items instead of throwing them away",
                    "Choose reusable alternatives (water bottles, shopping bags)",
                    "Repair items instead of replacing them",
                    "Buy second-hand when possible"
                ],
                'medium_emissions': [
                    "Improve sorting for better recycling",
                    "Reduce packaging waste by buying in bulk",
                    "Use both sides of paper",
                    "Choose products made from recycled materials"
                ],
                'low_emissions': [
                    "Excellent waste management!",
                    "Your waste practices are very sustainable",
                    "Help others learn about proper waste disposal"
                ]
            }
        }
    
    def _load_impact_estimates(self) -> Dict:
        """Load impact estimates for different actions"""
        return {
            'transportation': {
                'switch_to_electric': -2000,  # kg CO2/year
                'work_from_home_2days': -800,
                'use_public_transport': -1200,
                'carpool_regularly': -600,
                'eco_driving': -300,
                'bike_short_trips': -400
            },
            'energy': {
                'renewable_energy': -1500,
                'led_lighting': -200,
                'efficient_appliances': -500,
                'better_insulation': -800,
                'programmable_thermostat': -300,
                'unplug_devices': -150
            },
            'food': {
                'reduce_meat_50percent': -500,
                'local_food': -200,
                'reduce_food_waste': -300,
                'plant_based_2days': -400,
                'organic_food': -100
            },
            'waste': {
                'increase_recycling': -200,
                'composting': -150,
                'reduce_single_use': -100,
                'buy_second_hand': -80,
                'repair_vs_replace': -120
            }
        }
    
    def analyze_user_pattern(self, footprint_history: pd.DataFrame) -> Dict:
        """Analyze user patterns to identify improvement opportunities"""
        if len(footprint_history) == 0:
            return {'patterns': [], 'opportunities': []}
        
        patterns = []
        opportunities = []
        
        # Calculate averages
        avg_transport = footprint_history['transportation_emissions'].mean()
        avg_energy = footprint_history['energy_emissions'].mean()
        avg_food = footprint_history['food_emissions'].mean()
        avg_waste = footprint_history['waste_emissions'].mean()
        
        # Identify highest emission category
        category_avgs = {
            'transportation': avg_transport,
            'energy': avg_energy,
            'food': avg_food,
            'waste': avg_waste
        }
        
        highest_category = max(category_avgs, key=category_avgs.get)
        patterns.append(f"Your highest emissions come from {highest_category}")
        
        # Identify trends
        if len(footprint_history) >= 7:
            recent_avg = footprint_history['total_emissions'].tail(7).mean()
            older_avg = footprint_history['total_emissions'].head(7).mean()
            
            if recent_avg > older_avg * 1.1:
                patterns.append("Your emissions have been increasing recently")
                opportunities.append("Focus on reducing daily activities that contribute most to emissions")
            elif recent_avg < older_avg * 0.9:
                patterns.append("Great! Your emissions have been decreasing")
            else:
                patterns.append("Your emissions have been relatively stable")
        
        # Day of week patterns
        if len(footprint_history) >= 14:
            footprint_history['day_of_week'] = pd.to_datetime(footprint_history['date']).dt.day_name()
            daily_avg = footprint_history.groupby('day_of_week')['total_emissions'].mean()
            
            highest_day = daily_avg.idxmax()
            lowest_day = daily_avg.idxmin()
            
            patterns.append(f"Your highest emission day is typically {highest_day}")
            patterns.append(f"Your lowest emission day is typically {lowest_day}")
            
            if daily_avg[highest_day] > daily_avg[lowest_day] * 1.5:
                opportunities.append(f"Try to replicate your {lowest_day} habits on {highest_day}")
        
        return {'patterns': patterns, 'opportunities': opportunities}
    
    def get_personalized_recommendations(self, user_footprint: Dict, 
                                       user_patterns: Dict, 
                                       user_goals: List[Dict] = None) -> List[Dict]:
        """Generate personalized recommendations based on user data and AI analysis"""
        recommendations = []
        
        # Categorize emission levels
        thresholds = {
            'transportation': {'high': 100, 'medium': 50},
            'energy': {'high': 200, 'medium': 100},
            'food': {'high': 150, 'medium': 75},
            'waste': {'high': 50, 'medium': 25}
        }
        
        for category, emissions in user_footprint.items():
            if category == 'total':
                continue
                
            # Determine emission level
            if emissions > thresholds[category]['high']:
                level = 'high_emissions'
            elif emissions > thresholds[category]['medium']:
                level = 'medium_emissions'
            else:
                level = 'low_emissions'
            
            # Get category-specific recommendations
            category_recs = self.recommendation_database[category][level]
            
            # Add top recommendations with impact estimates
            for rec in category_recs[:2]:  # Top 2 per category
                # Extract action key for impact estimation
                action_key = self._extract_action_key(rec, category)
                impact = self.impact_estimates[category].get(action_key, 0)
                
                recommendations.append({
                    'category': category.title(),
                    'recommendation': rec,
                    'impact_estimate': impact,
                    'priority': self._calculate_priority(emissions, impact),
                    'difficulty': self._estimate_difficulty(rec)
                })
        
        # Sort by priority and impact
        recommendations.sort(key=lambda x: (x['priority'], abs(x['impact_estimate'])), reverse=True)
        
        return recommendations[:8]  # Return top 8 recommendations
    
    def _extract_action_key(self, recommendation: str, category: str) -> str:
        """Extract action key from recommendation text for impact lookup"""
        action_mapping = {
            'transportation': {
                'electric': 'switch_to_electric',
                'work from home': 'work_from_home_2days',
                'public': 'use_public_transport',
                'carpool': 'carpool_regularly',
                'eco-driving': 'eco_driving',
                'cycling': 'bike_short_trips'
            },
            'energy': {
                'renewable': 'renewable_energy',
                'LED': 'led_lighting',
                'appliances': 'efficient_appliances',
                'insulation': 'better_insulation',
                'thermostat': 'programmable_thermostat',
                'unplug': 'unplug_devices'
            },
            'food': {
                'meat': 'reduce_meat_50percent',
                'local': 'local_food',
                'waste': 'reduce_food_waste',
                'plant-based': 'plant_based_2days',
                'organic': 'organic_food'
            },
            'waste': {
                'recycling': 'increase_recycling',
                'composting': 'composting',
                'single-use': 'reduce_single_use',
                'second-hand': 'buy_second_hand',
                'repair': 'repair_vs_replace'
            }
        }
        
        rec_lower = recommendation.lower()
        for keyword, action in action_mapping[category].items():
            if keyword in rec_lower:
                return action
        
        return list(action_mapping[category].values())[0]  # Default to first action
    
    def _calculate_priority(self, current_emissions: float, impact: float) -> int:
        """Calculate recommendation priority (1-10 scale)"""
        # Higher priority for high emissions and high impact
        emission_score = min(current_emissions / 100, 5)  # Scale to 0-5
        impact_score = min(abs(impact) / 500, 5)  # Scale to 0-5
        
        return int(emission_score + impact_score)
    
    def _estimate_difficulty(self, recommendation: str) -> str:
        """Estimate implementation difficulty"""
        rec_lower = recommendation.lower()
        
        high_difficulty_keywords = ['switch', 'install', 'upgrade', 'renewable']
        medium_difficulty_keywords = ['reduce', 'increase', 'improve', 'plan']
        
        if any(keyword in rec_lower for keyword in high_difficulty_keywords):
            return 'High'
        elif any(keyword in rec_lower for keyword in medium_difficulty_keywords):
            return 'Medium'
        else:
            return 'Low'
    
    def generate_action_plan(self, recommendations: List[Dict], 
                           timeframe_weeks: int = 12) -> Dict:
        """Generate a structured action plan from recommendations"""
        # Sort recommendations by difficulty and impact
        easy_wins = [r for r in recommendations if r['difficulty'] == 'Low']
        medium_actions = [r for r in recommendations if r['difficulty'] == 'Medium']
        major_changes = [r for r in recommendations if r['difficulty'] == 'High']
        
        action_plan = {
            'weeks_1_2': {
                'focus': 'Quick Wins',
                'actions': easy_wins[:3],
                'expected_reduction': sum(abs(r['impact_estimate']) for r in easy_wins[:3])
            },
            'weeks_3_6': {
                'focus': 'Habit Changes',
                'actions': medium_actions[:3],
                'expected_reduction': sum(abs(r['impact_estimate']) for r in medium_actions[:3])
            },
            'weeks_7_12': {
                'focus': 'Major Improvements',
                'actions': major_changes[:2],
                'expected_reduction': sum(abs(r['impact_estimate']) for r in major_changes[:2])
            }
        }
        
        total_reduction = sum(phase['expected_reduction'] for phase in action_plan.values())
        action_plan['total_potential_reduction'] = total_reduction
        
        return action_plan
    
    def get_seasonal_recommendations(self, current_month: int) -> List[str]:
        """Get season-specific recommendations"""
        seasonal_recs = {
            'winter': [  # Dec, Jan, Feb
                "Optimize heating efficiency - lower thermostat by 2°F",
                "Use draft stoppers and weatherstripping",
                "Take advantage of natural sunlight for heating",
                "Wear layers instead of increasing heat"
            ],
            'spring': [  # Mar, Apr, May
                "Start a garden to grow your own vegetables",
                "Begin cycling or walking as weather improves",
                "Clean and maintain HVAC systems",
                "Plan energy-efficient home improvements"
            ],
            'summer': [  # Jun, Jul, Aug
                "Use fans instead of air conditioning when possible",
                "Plan local vacations to reduce travel emissions",
                "Harvest rainwater for garden irrigation",
                "Use natural ventilation during cooler hours"
            ],
            'fall': [  # Sep, Oct, Nov
                "Prepare home for winter efficiency",
                "Preserve seasonal foods to reduce winter transport emissions",
                "Switch to renewable energy before peak heating season",
                "Insulate pipes and water heater"
            ]
        }
        
        if current_month in [12, 1, 2]:
            return seasonal_recs['winter']
        elif current_month in [3, 4, 5]:
            return seasonal_recs['spring']
        elif current_month in [6, 7, 8]:
            return seasonal_recs['summer']
        else:
            return seasonal_recs['fall']
    
    def calculate_roi_recommendations(self, recommendations: List[Dict], 
                                    annual_income: float = 50000) -> List[Dict]:
        """Calculate ROI for recommendations that involve financial investment"""
        cost_estimates = {
            'switch_to_electric': 25000,
            'renewable_energy': 15000,
            'efficient_appliances': 2000,
            'better_insulation': 5000,
            'programmable_thermostat': 200,
            'led_lighting': 300
        }
        
        # Carbon price estimate ($/ton CO2)
        carbon_price = 50
        
        for rec in recommendations:
            action_key = self._extract_action_key(rec['recommendation'], rec['category'].lower())
            
            if action_key in cost_estimates:
                upfront_cost = cost_estimates[action_key]
                annual_savings = abs(rec['impact_estimate']) * (carbon_price / 1000)  # Convert kg to tons
                
                if annual_savings > 0:
                    payback_years = upfront_cost / annual_savings
                    rec['upfront_cost'] = upfront_cost
                    rec['annual_savings'] = annual_savings
                    rec['payback_years'] = payback_years
                    rec['roi_5year'] = (annual_savings * 5 - upfront_cost) / upfront_cost * 100
        
        return recommendations
    
    def get_community_challenges(self) -> List[Dict]:
        """Get community-based challenges to encourage engagement"""
        challenges = [
            {
                'name': 'Car-Free Week',
                'description': 'Use only public transport, cycling, or walking for one week',
                'duration': '7 days',
                'estimated_impact': -50,  # kg CO2
                'difficulty': 'Medium'
            },
            {
                'name': 'Plant-Based Challenge',
                'description': 'Eat only plant-based meals for two weeks',
                'duration': '14 days',
                'estimated_impact': -30,
                'difficulty': 'Medium'
            },
            {
                'name': 'Zero Waste Weekend',
                'description': 'Produce no landfill waste for an entire weekend',
                'duration': '2 days',
                'estimated_impact': -5,
                'difficulty': 'High'
            },
            {
                'name': 'Energy Saver Month',
                'description': 'Reduce energy consumption by 20% for one month',
                'duration': '30 days',
                'estimated_impact': -100,
                'difficulty': 'Medium'
            },
            {
                'name': 'Local Food Challenge',
                'description': 'Eat only locally sourced food for one week',
                'duration': '7 days',
                'estimated_impact': -15,
                'difficulty': 'Low'
            }
        ]
        
        return challenges
    
    def generate_weekly_tips(self, user_footprint: Dict, week_number: int) -> List[str]:
        """Generate weekly tips based on user data and week of year"""
        tips = []
        
        # Base tips on highest emission category
        highest_category = max(
            [(k, v) for k, v in user_footprint.items() if k != 'total'],
            key=lambda x: x[1]
        )[0]
        
        weekly_tips_db = {
            'transportation': [
                "Try walking or biking for trips under 2 miles",
                "Plan your errands to minimize driving",
                "Check your tire pressure - properly inflated tires improve fuel efficiency",
                "Consider carpooling with colleagues or neighbors"
            ],
            'energy': [
                "Unplug chargers and electronics when not in use",
                "Use cold water for washing clothes",
                "Open curtains during sunny days for natural heating",
                "Set your water heater to 120°F (49°C)"
            ],
            'food': [
                "Try one new plant-based recipe this week",
                "Buy only what you need to reduce food waste",
                "Choose seasonal fruits and vegetables",
                "Start a small herb garden on your windowsill"
            ],
            'waste': [
                "Bring reusable bags when shopping",
                "Use both sides of paper for notes",
                "Donate clothes instead of throwing them away",
                "Start separating compostable materials"
            ]
        }
        
        # Select tips based on week and category
        category_tips = weekly_tips_db[highest_category]
        tip_index = week_number % len(category_tips)
        tips.append(category_tips[tip_index])
        
        # Add seasonal tip
        current_month = datetime.now().month
        seasonal_tips = self.get_seasonal_recommendations(current_month)
        tips.append(seasonal_tips[week_number % len(seasonal_tips)])
        
        return tips
    
    def benchmark_against_peers(self, user_footprint: Dict, 
                              user_demographics: Dict = None) -> Dict:
        """Benchmark user against similar demographic groups"""
        # Default benchmarks (kg CO2/year)
        benchmarks = {
            'global_average': 4800,
            'us_average': 16000,
            'eu_average': 8500,
            'target_2030': 2300  # Paris Agreement target
        }
        
        user_annual = user_footprint.get('total', 0) * 365
        
        comparisons = {}
        for benchmark_name, benchmark_value in benchmarks.items():
            difference = user_annual - benchmark_value
            percentage = (difference / benchmark_value) * 100 if benchmark_value > 0 else 0
            
            comparisons[benchmark_name] = {
                'value': benchmark_value,
                'difference': difference,
                'percentage': percentage,
                'status': 'above' if difference > 0 else 'below'
            }
        
        return comparisons
