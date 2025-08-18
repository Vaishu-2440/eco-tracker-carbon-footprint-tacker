"""
Utility functions for the EcoTracker application
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional, Tuple

class EcoTrackerUtils:
    """Utility functions for carbon footprint calculations and data processing"""
    
    @staticmethod
    def validate_user_input(data: Dict) -> Tuple[bool, List[str]]:
        """Validate user input data"""
        errors = []
        
        # Check for negative values
        for category, values in data.items():
            if isinstance(values, dict):
                for key, value in values.items():
                    if isinstance(value, (int, float)) and value < 0:
                        errors.append(f"Negative value not allowed for {category}.{key}")
            elif isinstance(values, (int, float)) and values < 0:
                errors.append(f"Negative value not allowed for {category}")
        
        # Check for reasonable ranges
        if 'transportation' in data:
            car_miles = data['transportation'].get('car_gasoline', {}).get('distance', 0)
            if car_miles > 500:  # More than 500 miles per day seems unrealistic
                errors.append("Daily car miles seems unrealistically high (>500)")
        
        if 'energy' in data:
            electricity = data['energy'].get('electricity', 0)
            if electricity > 100:  # More than 100 kWh per day
                errors.append("Daily electricity usage seems very high (>100 kWh)")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def convert_units(value: float, from_unit: str, to_unit: str) -> float:
        """Convert between different units"""
        conversions = {
            # Distance conversions
            ('miles', 'km'): 1.60934,
            ('km', 'miles'): 0.621371,
            
            # Energy conversions
            ('kwh', 'mwh'): 0.001,
            ('mwh', 'kwh'): 1000,
            ('btu', 'kwh'): 0.000293071,
            ('kwh', 'btu'): 3412.14,
            
            # Weight conversions
            ('lbs', 'kg'): 0.453592,
            ('kg', 'lbs'): 2.20462,
            ('tons', 'kg'): 1000,
            ('kg', 'tons'): 0.001,
            
            # Volume conversions
            ('gallons', 'liters'): 3.78541,
            ('liters', 'gallons'): 0.264172
        }
        
        conversion_key = (from_unit.lower(), to_unit.lower())
        if conversion_key in conversions:
            return value * conversions[conversion_key]
        else:
            return value  # No conversion available
    
    @staticmethod
    def calculate_carbon_intensity(emissions: float, activity_amount: float) -> float:
        """Calculate carbon intensity (emissions per unit of activity)"""
        if activity_amount == 0:
            return 0
        return emissions / activity_amount
    
    @staticmethod
    def format_emissions(emissions: float) -> str:
        """Format emissions value for display"""
        if emissions >= 1000:
            return f"{emissions/1000:.2f} tons CO₂"
        else:
            return f"{emissions:.1f} kg CO₂"
    
    @staticmethod
    def calculate_percentage_change(old_value: float, new_value: float) -> float:
        """Calculate percentage change between two values"""
        if old_value == 0:
            return 0
        return ((new_value - old_value) / old_value) * 100
    
    @staticmethod
    def get_emission_category(daily_emissions: float) -> str:
        """Categorize daily emissions level"""
        if daily_emissions < 10:
            return "Low"
        elif daily_emissions < 25:
            return "Medium"
        elif daily_emissions < 50:
            return "High"
        else:
            return "Very High"
    
    @staticmethod
    def calculate_days_to_goal(current_rate: float, target_rate: float, 
                              current_total: float = 0) -> int:
        """Calculate days needed to reach emission goal"""
        if current_rate <= target_rate:
            return 0
        
        daily_reduction_needed = current_rate - target_rate
        if daily_reduction_needed <= 0:
            return float('inf')
        
        # Assume linear improvement
        return int(current_total / daily_reduction_needed)
    
    @staticmethod
    def generate_sample_data() -> Dict:
        """Generate sample user data for testing"""
        return {
            'transportation': {
                'car_gasoline': {'distance': 25, 'frequency': 1},
                'bus': {'distance': 5, 'frequency': 1}
            },
            'energy': {
                'electricity': 30,  # kWh
                'natural_gas': 2    # therms
            },
            'food': {
                'beef': 0.2,        # kg
                'chicken': 0.3,
                'vegetables': 0.5,
                'dairy': 0.4
            },
            'waste': {
                'landfill': 1.5,    # kg
                'recycling': 0.5
            }
        }
    
    @staticmethod
    def export_to_csv(data: pd.DataFrame, filename: str) -> str:
        """Export data to CSV file"""
        os.makedirs("exports", exist_ok=True)
        filepath = os.path.join("exports", filename)
        data.to_csv(filepath, index=False)
        return filepath
    
    @staticmethod
    def load_external_data(source: str) -> Optional[pd.DataFrame]:
        """Load data from external sources"""
        # Placeholder for future API integrations
        external_sources = {
            'electricity_grid': 'data/grid_emissions.csv',
            'transport_stats': 'data/transport_emissions.csv',
            'food_database': 'data/food_emissions.csv'
        }
        
        if source in external_sources:
            filepath = external_sources[source]
            if os.path.exists(filepath):
                return pd.read_csv(filepath)
        
        return None
    
    @staticmethod
    def get_country_specific_factors(country: str = "US") -> Dict:
        """Get country-specific emission factors"""
        country_factors = {
            'US': {
                'electricity_grid': 0.92,
                'transport_efficiency': 1.0,
                'waste_management': 1.0
            },
            'UK': {
                'electricity_grid': 0.45,
                'transport_efficiency': 0.8,
                'waste_management': 0.7
            },
            'Germany': {
                'electricity_grid': 0.55,
                'transport_efficiency': 0.7,
                'waste_management': 0.6
            },
            'Canada': {
                'electricity_grid': 0.35,
                'transport_efficiency': 1.1,
                'waste_management': 0.9
            }
        }
        
        return country_factors.get(country, country_factors['US'])
    
    @staticmethod
    def calculate_offset_cost(emissions_kg: float, offset_price_per_ton: float = 20) -> float:
        """Calculate cost to offset carbon emissions"""
        emissions_tons = emissions_kg / 1000
        return emissions_tons * offset_price_per_ton
    
    @staticmethod
    def get_sustainability_score(footprint_data: Dict) -> Tuple[int, str]:
        """Calculate sustainability score (0-100) and grade"""
        total_daily = footprint_data.get('total', 0)
        
        # Score based on daily emissions (lower is better)
        if total_daily <= 5:
            score = 95
            grade = "A+"
        elif total_daily <= 10:
            score = 85
            grade = "A"
        elif total_daily <= 20:
            score = 75
            grade = "B+"
        elif total_daily <= 30:
            score = 65
            grade = "B"
        elif total_daily <= 45:
            score = 55
            grade = "C+"
        elif total_daily <= 60:
            score = 45
            grade = "C"
        elif total_daily <= 80:
            score = 35
            grade = "D"
        else:
            score = 25
            grade = "F"
        
        return score, grade
