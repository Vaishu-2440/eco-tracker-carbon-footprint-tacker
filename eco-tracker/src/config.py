"""
Configuration settings for the EcoTracker application
"""

import os
from typing import Dict

class Config:
    """Application configuration"""
    
    # Database settings
    DATABASE_PATH = "data/eco_tracker.db"
    
    # Model settings
    MODEL_DIR = "models"
    DEFAULT_MODEL = "xgboost"
    
    # Emission factors (kg CO2 per unit) - Updated with latest IPCC data
    EMISSION_FACTORS = {
        'transportation': {
            'car_gasoline': 0.411,      # kg CO2 per mile
            'car_diesel': 0.364,
            'car_electric': 0.1,        # Varies by grid mix
            'car_hybrid': 0.25,
            'bus': 0.089,
            'train': 0.041,
            'subway': 0.035,
            'plane_domestic': 0.255,
            'plane_international': 0.195,
            'motorcycle': 0.197,
            'bicycle': 0.0,
            'walking': 0.0,
            'scooter_electric': 0.05
        },
        'energy': {
            'electricity_us_avg': 0.92,    # kg CO2 per kWh
            'electricity_coal': 2.23,
            'electricity_natural_gas': 0.91,
            'electricity_renewable': 0.02,
            'natural_gas': 5.3,            # kg CO2 per therm
            'heating_oil': 10.15,          # kg CO2 per gallon
            'propane': 5.68,               # kg CO2 per gallon
            'wood': 1.87                   # kg CO2 per kg
        },
        'food': {
            'beef': 27.0,                  # kg CO2 per kg
            'lamb': 39.2,
            'pork': 12.1,
            'chicken': 6.9,
            'turkey': 10.9,
            'fish_farmed': 6.1,
            'fish_wild': 2.9,
            'dairy_milk': 3.2,
            'cheese': 13.5,
            'eggs': 4.8,
            'vegetables_local': 2.0,
            'vegetables_imported': 4.0,
            'fruits_local': 1.1,
            'fruits_imported': 2.5,
            'grains': 2.5,
            'nuts': 2.3,
            'processed_food': 5.8,
            'beverages': 1.4
        },
        'waste': {
            'landfill': 0.57,             # kg CO2 per kg waste
            'recycling': 0.0,
            'composting': 0.0,
            'incineration': 0.7,
            'electronic_waste': 2.1
        }
    }
    
    # Benchmarks (kg CO2 per year)
    BENCHMARKS = {
        'global_average': 4800,
        'us_average': 16000,
        'eu_average': 8500,
        'canada_average': 15600,
        'australia_average': 17100,
        'paris_target_2030': 2300,
        'paris_target_2050': 1000
    }
    
    # Recommendation thresholds (daily kg CO2)
    RECOMMENDATION_THRESHOLDS = {
        'transportation': {'high': 15, 'medium': 8},
        'energy': {'high': 25, 'medium': 12},
        'food': {'high': 12, 'medium': 6},
        'waste': {'high': 3, 'medium': 1.5}
    }
    
    # UI Configuration
    UI_CONFIG = {
        'page_title': "EcoTracker - Carbon Footprint Monitor",
        'page_icon': "🌱",
        'layout': "wide",
        'theme': {
            'primary_color': "#2E8B57",
            'background_color': "#F0F8FF",
            'secondary_background_color': "#E6F3FF",
            'text_color': "#1E1E1E"
        }
    }
    
    # API Configuration (for future external integrations)
    API_CONFIG = {
        'carbon_interface_api': {
            'base_url': "https://www.carboninterface.com/api/v1/",
            'timeout': 30
        },
        'electricity_maps_api': {
            'base_url': "https://api.electricitymap.org/v3/",
            'timeout': 30
        }
    }
    
    @staticmethod
    def get_emission_factor(category: str, activity_type: str) -> float:
        """Get emission factor for specific activity"""
        return Config.EMISSION_FACTORS.get(category, {}).get(activity_type, 0.0)
    
    @staticmethod
    def get_benchmark(benchmark_type: str) -> float:
        """Get benchmark value"""
        return Config.BENCHMARKS.get(benchmark_type, 0.0)
    
    @staticmethod
    def get_threshold(category: str, level: str) -> float:
        """Get recommendation threshold"""
        return Config.RECOMMENDATION_THRESHOLDS.get(category, {}).get(level, 0.0)
