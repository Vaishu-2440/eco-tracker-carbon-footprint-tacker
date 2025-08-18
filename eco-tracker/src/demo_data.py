"""
Demo data generator for EcoTracker application
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from data_manager import DataManager
from carbon_calculator import CarbonFootprintCalculator

class DemoDataGenerator:
    """Generate realistic demo data for testing and demonstration"""
    
    def __init__(self):
        self.calculator = CarbonFootprintCalculator()
        
    def generate_demo_user_data(self, days: int = 30) -> pd.DataFrame:
        """Generate demo data for a realistic user over specified days"""
        np.random.seed(42)
        random.seed(42)
        
        demo_data = []
        start_date = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            day_of_week = current_date.weekday()  # 0=Monday, 6=Sunday
            
            # Create realistic patterns based on day of week
            is_weekend = day_of_week >= 5
            is_workday = not is_weekend
            
            # Transportation patterns
            if is_workday:
                car_miles = np.random.normal(30, 8)  # Commute
                public_transport = np.random.normal(5, 2)
                flights = 0
            else:
                car_miles = np.random.normal(15, 10)  # Weekend errands
                public_transport = np.random.normal(2, 1)
                flights = np.random.poisson(0.1) * 500  # Occasional flights
            
            # Energy patterns (higher in winter/summer)
            month = current_date.month
            if month in [12, 1, 2, 6, 7, 8]:  # Winter/Summer
                electricity = np.random.normal(35, 8)
                natural_gas = np.random.normal(3, 1)
            else:
                electricity = np.random.normal(25, 5)
                natural_gas = np.random.normal(1.5, 0.5)
            
            # Food patterns (more meat on weekends)
            if is_weekend:
                beef_meals = np.random.poisson(0.5)
                chicken_meals = np.random.poisson(1)
            else:
                beef_meals = np.random.poisson(0.2)
                chicken_meals = np.random.poisson(0.8)
            
            vegetable_servings = np.random.poisson(4)
            dairy_servings = np.random.poisson(2)
            
            # Waste patterns
            waste_kg = np.random.normal(2, 0.5)
            recycling_rate = np.random.uniform(40, 80)
            
            # Calculate emissions
            user_data = {
                'transportation': {
                    'car_gasoline': {'distance': max(0, car_miles), 'frequency': 1},
                    'bus': {'distance': max(0, public_transport), 'frequency': 1},
                    'plane_domestic': {'distance': max(0, flights), 'frequency': 1}
                },
                'energy': {
                    'electricity': max(0, electricity),
                    'natural_gas': max(0, natural_gas)
                },
                'food': {
                    'beef': beef_meals * 0.25,
                    'chicken': chicken_meals * 0.2,
                    'vegetables': vegetable_servings * 0.1,
                    'dairy': dairy_servings * 0.1
                },
                'waste': {
                    'landfill': waste_kg * (1 - recycling_rate/100),
                    'recycling': waste_kg * (recycling_rate/100)
                }
            }
            
            footprint = self.calculator.calculate_total_footprint(user_data)
            
            demo_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'day_of_week': current_date.strftime('%A'),
                'transportation_emissions': footprint['transportation'],
                'energy_emissions': footprint['energy'],
                'food_emissions': footprint['food'],
                'waste_emissions': footprint['waste'],
                'total_emissions': footprint['total'],
                'car_miles': max(0, car_miles),
                'electricity_kwh': max(0, electricity),
                'meat_meals': beef_meals + chicken_meals,
                'waste_kg': waste_kg,
                'recycling_rate': recycling_rate
            })
        
        return pd.DataFrame(demo_data)
    
    def populate_demo_database(self, user_name: str = "Demo User", days: int = 60):
        """Populate database with demo data"""
        data_manager = DataManager()
        
        # Create demo user
        user_id = data_manager.create_user(user_name, "demo@ecotracker.com")
        
        # Generate demo data
        demo_df = self.generate_demo_user_data(days)
        
        # Save to database
        for _, row in demo_df.iterrows():
            footprint_data = {
                'transportation': row['transportation_emissions'],
                'energy': row['energy_emissions'],
                'food': row['food_emissions'],
                'waste': row['waste_emissions'],
                'total': row['total_emissions']
            }
            
            data_manager.save_daily_footprint(user_id, row['date'], footprint_data)
            
            # Save individual activities
            activities = [
                ('transportation', 'car_travel', row['car_miles'], 'miles', row['transportation_emissions']),
                ('energy', 'electricity', row['electricity_kwh'], 'kWh', row['energy_emissions']),
                ('food', 'meals', row['meat_meals'], 'servings', row['food_emissions']),
                ('waste', 'total_waste', row['waste_kg'], 'kg', row['waste_emissions'])
            ]
            
            for category, activity_type, amount, unit, emissions in activities:
                if amount > 0:
                    data_manager.save_activity(user_id, row['date'], category, activity_type, amount, unit, emissions)
        
        # Create demo goals
        goals = [
            ('Daily Emissions Reduction', 25.0, (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')),
            ('Monthly Emissions Limit', 800.0, (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')),
            ('Annual Footprint Goal', 8000.0, (datetime.now() + timedelta(days=365)).strftime('%Y-%m-%d'))
        ]
        
        for goal_type, target, target_date in goals:
            data_manager.create_goal(user_id, goal_type, target, target_date)
        
        print(f"✅ Demo data created for user ID: {user_id}")
        print(f"📊 Generated {len(demo_df)} days of data")
        print(f"🎯 Created {len(goals)} demo goals")
        
        return user_id

def main():
    """Run demo data generation"""
    print("🎭 Generating EcoTracker Demo Data...")
    
    generator = DemoDataGenerator()
    user_id = generator.populate_demo_database("Demo User", 60)
    
    print(f"\n🎉 Demo setup complete!")
    print(f"👤 Demo User ID: {user_id}")
    print(f"🚀 Run 'streamlit run app.py' to see the demo data in action")

if __name__ == "__main__":
    main()
