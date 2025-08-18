#!/usr/bin/env python3
"""
Test script to validate EcoTracker functionality
"""

import sys
import os
import unittest
from datetime import datetime

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from carbon_calculator import CarbonFootprintCalculator
from ml_models import CarbonFootprintPredictor
from data_manager import DataManager
from utils import EcoTrackerUtils
from config import Config

class TestEcoTracker(unittest.TestCase):
    """Test suite for EcoTracker components"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.calculator = CarbonFootprintCalculator()
        self.predictor = CarbonFootprintPredictor()
        self.data_manager = DataManager("data/test_eco_tracker.db")
        
    def test_carbon_calculator(self):
        """Test carbon footprint calculations"""
        test_data = {
            'transportation': {
                'car_gasoline': {'distance': 25, 'frequency': 1}
            },
            'energy': {
                'electricity': 30
            },
            'food': {
                'beef': 0.2,
                'vegetables': 0.5
            },
            'waste': {
                'landfill': 1.5
            }
        }
        
        result = self.calculator.calculate_total_footprint(test_data)
        
        # Check that all categories are calculated
        self.assertIn('transportation', result)
        self.assertIn('energy', result)
        self.assertIn('food', result)
        self.assertIn('waste', result)
        self.assertIn('total', result)
        
        # Check that total is sum of parts
        expected_total = (result['transportation'] + result['energy'] + 
                         result['food'] + result['waste'])
        self.assertAlmostEqual(result['total'], expected_total, places=2)
        
        print("Carbon calculator test passed")
    
    def test_ml_models(self):
        """Test ML model functionality"""
        # Generate test data
        test_data = self.predictor.generate_synthetic_data(100)
        self.assertEqual(len(test_data), 100)
        
        # Test training
        results = self.predictor.train_models(test_data)
        self.assertGreater(len(results), 0)
        
        # Test prediction
        sample_input = {
            'age': 30,
            'income': 50000,
            'household_size': 2,
            'location_type': 'urban',
            'car_miles_per_week': 100,
            'public_transport_usage': 2,
            'flights_per_year': 2,
            'vehicle_type': 'gasoline',
            'electricity_kwh_monthly': 900,
            'natural_gas_therms_monthly': 50,
            'home_size_sqft': 2000,
            'renewable_energy': 0,
            'meat_meals_per_week': 10,
            'local_food_percentage': 30,
            'organic_food_percentage': 20,
            'waste_kg_per_week': 15,
            'recycling_percentage': 50,
            'composting': 0
        }
        
        prediction = self.predictor.predict_footprint(sample_input)
        self.assertGreater(prediction, 0)
        
        print("ML models test passed")
    
    def test_data_manager(self):
        """Test data management functionality"""
        # Test user creation (handle existing user)
        import random
        test_email = f"test{random.randint(1000,9999)}@example.com"
        try:
            user_id = self.data_manager.create_user("Test User", test_email)
        except:
            # Use existing user for testing
            user_id = 1
        self.assertIsNotNone(user_id)
        
        # Test user retrieval
        user = self.data_manager.get_user(user_id)
        self.assertIsNotNone(user)
        
        # Test footprint saving
        test_footprint = {
            'transportation': 10.5,
            'energy': 15.2,
            'food': 8.3,
            'waste': 2.1,
            'total': 36.1
        }
        
        self.data_manager.save_daily_footprint(
            user_id, 
            datetime.now().strftime('%Y-%m-%d'), 
            test_footprint
        )
        
        # Test footprint retrieval
        history = self.data_manager.get_footprint_history(user_id, 1)
        self.assertEqual(len(history), 1)
        
        print("Data manager test passed")
    
    def test_utils(self):
        """Test utility functions"""
        # Test input validation
        valid_data = EcoTrackerUtils.generate_sample_data()
        is_valid, errors = EcoTrackerUtils.validate_user_input(valid_data)
        self.assertTrue(is_valid)
        
        # Test unit conversion
        miles_to_km = EcoTrackerUtils.convert_units(10, 'miles', 'km')
        self.assertAlmostEqual(miles_to_km, 16.0934, places=2)
        
        # Test sustainability score
        test_footprint = {'total': 15}
        score, grade = EcoTrackerUtils.get_sustainability_score(test_footprint)
        self.assertGreaterEqual(score, 0)
        self.assertLessEqual(score, 100)
        
        print("Utils test passed")
    
    def test_config(self):
        """Test configuration settings"""
        # Test emission factor retrieval
        car_factor = Config.get_emission_factor('transportation', 'car_gasoline')
        self.assertEqual(car_factor, 0.411)
        
        # Test benchmark retrieval
        us_avg = Config.get_benchmark('us_average')
        self.assertEqual(us_avg, 16000)
        
        # Test threshold retrieval
        transport_high = Config.get_threshold('transportation', 'high')
        self.assertEqual(transport_high, 15)
        
        print("Config test passed")

def run_tests():
    """Run all tests"""
    print("Running EcoTracker Test Suite...")
    print("=" * 50)
    
    # Create test database directory
    os.makedirs("data", exist_ok=True)
    
    # Run tests
    unittest.main(verbosity=2, exit=False)
    
    print("=" * 50)
    print("All tests completed!")

if __name__ == "__main__":
    run_tests()
