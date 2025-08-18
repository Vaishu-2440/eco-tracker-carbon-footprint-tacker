import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta

class CarbonFootprintCalculator:
    """
    Core calculator for carbon footprint estimation across different categories
    """
    
    def __init__(self):
        # Emission factors (kg CO2 per unit)
        self.emission_factors = {
            'transportation': {
                'car_gasoline': 0.411,  # kg CO2 per mile
                'car_diesel': 0.364,
                'car_electric': 0.1,
                'bus': 0.089,
                'train': 0.041,
                'plane_domestic': 0.255,
                'plane_international': 0.195,
                'motorcycle': 0.197,
                'bicycle': 0.0,
                'walking': 0.0
            },
            'energy': {
                'electricity': 0.92,  # kg CO2 per kWh (US average)
                'natural_gas': 5.3,   # kg CO2 per therm
                'heating_oil': 10.15, # kg CO2 per gallon
                'propane': 5.68,      # kg CO2 per gallon
                'coal': 2.23          # kg CO2 per pound
            },
            'food': {
                'beef': 27.0,         # kg CO2 per kg
                'lamb': 39.2,
                'pork': 12.1,
                'chicken': 6.9,
                'fish': 6.1,
                'dairy': 3.2,
                'eggs': 4.8,
                'vegetables': 2.0,
                'fruits': 1.1,
                'grains': 2.5,
                'processed_food': 5.8
            },
            'waste': {
                'landfill': 0.57,     # kg CO2 per kg waste
                'recycling': 0.0,
                'composting': 0.0,
                'incineration': 0.7
            }
        }
    
    def calculate_transportation_footprint(self, transport_data: Dict) -> float:
        """Calculate carbon footprint from transportation"""
        total_emissions = 0.0
        
        for mode, details in transport_data.items():
            if mode in self.emission_factors['transportation']:
                distance = details.get('distance', 0)
                frequency = details.get('frequency', 1)
                total_emissions += (
                    distance * frequency * 
                    self.emission_factors['transportation'][mode]
                )
        
        return total_emissions
    
    def calculate_energy_footprint(self, energy_data: Dict) -> float:
        """Calculate carbon footprint from energy consumption"""
        total_emissions = 0.0
        
        for source, consumption in energy_data.items():
            if source in self.emission_factors['energy']:
                total_emissions += (
                    consumption * self.emission_factors['energy'][source]
                )
        
        return total_emissions
    
    def calculate_food_footprint(self, food_data: Dict) -> float:
        """Calculate carbon footprint from food consumption"""
        total_emissions = 0.0
        
        for food_type, amount in food_data.items():
            if food_type in self.emission_factors['food']:
                total_emissions += (
                    amount * self.emission_factors['food'][food_type]
                )
        
        return total_emissions
    
    def calculate_waste_footprint(self, waste_data: Dict) -> float:
        """Calculate carbon footprint from waste generation"""
        total_emissions = 0.0
        
        for disposal_method, amount in waste_data.items():
            if disposal_method in self.emission_factors['waste']:
                total_emissions += (
                    amount * self.emission_factors['waste'][disposal_method]
                )
        
        return total_emissions
    
    def calculate_total_footprint(self, user_data: Dict) -> Dict:
        """Calculate total carbon footprint across all categories"""
        footprint_breakdown = {}
        
        if 'transportation' in user_data:
            footprint_breakdown['transportation'] = self.calculate_transportation_footprint(
                user_data['transportation']
            )
        
        if 'energy' in user_data:
            footprint_breakdown['energy'] = self.calculate_energy_footprint(
                user_data['energy']
            )
        
        if 'food' in user_data:
            footprint_breakdown['food'] = self.calculate_food_footprint(
                user_data['food']
            )
        
        if 'waste' in user_data:
            footprint_breakdown['waste'] = self.calculate_waste_footprint(
                user_data['waste']
            )
        
        footprint_breakdown['total'] = sum(footprint_breakdown.values())
        
        return footprint_breakdown
    
    def get_recommendations(self, footprint_data: Dict) -> List[str]:
        """Generate AI-powered recommendations based on footprint analysis"""
        recommendations = []
        
        # Transportation recommendations
        if footprint_data.get('transportation', 0) > 100:  # High transport emissions
            recommendations.extend([
                "Consider using public transportation or carpooling",
                "Switch to an electric or hybrid vehicle",
                "Work from home when possible to reduce commuting",
                "Combine multiple errands into one trip"
            ])
        
        # Energy recommendations
        if footprint_data.get('energy', 0) > 200:  # High energy emissions
            recommendations.extend([
                "Switch to renewable energy sources",
                "Improve home insulation to reduce heating/cooling needs",
                "Use energy-efficient appliances",
                "Install LED lighting throughout your home"
            ])
        
        # Food recommendations
        if footprint_data.get('food', 0) > 150:  # High food emissions
            recommendations.extend([
                "Reduce meat consumption, especially beef and lamb",
                "Buy local and seasonal produce",
                "Minimize food waste through meal planning",
                "Consider plant-based alternatives"
            ])
        
        # Waste recommendations
        if footprint_data.get('waste', 0) > 50:  # High waste emissions
            recommendations.extend([
                "Increase recycling and composting",
                "Reduce single-use items",
                "Buy products with minimal packaging",
                "Donate or sell items instead of throwing them away"
            ])
        
        return recommendations[:5]  # Return top 5 recommendations
