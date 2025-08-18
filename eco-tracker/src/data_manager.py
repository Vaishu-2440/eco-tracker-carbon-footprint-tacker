import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import sqlite3

class DataManager:
    """
    Manages user data storage and retrieval for carbon footprint tracking
    """
    
    def __init__(self, db_path: str = "data/eco_tracker.db"):
        self.db_path = db_path
        self.ensure_db_exists()
    
    def ensure_db_exists(self):
        """Create database and tables if they don't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Daily footprint records
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS daily_footprints (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    date DATE NOT NULL,
                    transportation_emissions REAL DEFAULT 0,
                    energy_emissions REAL DEFAULT 0,
                    food_emissions REAL DEFAULT 0,
                    waste_emissions REAL DEFAULT 0,
                    total_emissions REAL DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Activity logs
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activities (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    date DATE NOT NULL,
                    category TEXT NOT NULL,
                    activity_type TEXT NOT NULL,
                    amount REAL NOT NULL,
                    unit TEXT NOT NULL,
                    emissions REAL NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Goals table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    goal_type TEXT NOT NULL,
                    target_value REAL NOT NULL,
                    current_value REAL DEFAULT 0,
                    target_date DATE,
                    status TEXT DEFAULT 'active',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            conn.commit()
    
    def create_user(self, name: str, email: str = None) -> int:
        """Create a new user and return user ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (name, email)
            )
            return cursor.lastrowid
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Get user information by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            
            if row:
                return {
                    'id': row[0],
                    'name': row[1],
                    'email': row[2],
                    'created_at': row[3]
                }
            return None
    
    def save_daily_footprint(self, user_id: int, date: str, footprint_data: Dict):
        """Save daily carbon footprint data"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check if record exists for this date
            cursor.execute(
                "SELECT id FROM daily_footprints WHERE user_id = ? AND date = ?",
                (user_id, date)
            )
            existing = cursor.fetchone()
            
            if existing:
                # Update existing record
                cursor.execute('''
                    UPDATE daily_footprints 
                    SET transportation_emissions = ?, energy_emissions = ?, 
                        food_emissions = ?, waste_emissions = ?, total_emissions = ?
                    WHERE user_id = ? AND date = ?
                ''', (
                    footprint_data.get('transportation', 0),
                    footprint_data.get('energy', 0),
                    footprint_data.get('food', 0),
                    footprint_data.get('waste', 0),
                    footprint_data.get('total', 0),
                    user_id, date
                ))
            else:
                # Insert new record
                cursor.execute('''
                    INSERT INTO daily_footprints 
                    (user_id, date, transportation_emissions, energy_emissions, 
                     food_emissions, waste_emissions, total_emissions)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    user_id, date,
                    footprint_data.get('transportation', 0),
                    footprint_data.get('energy', 0),
                    footprint_data.get('food', 0),
                    footprint_data.get('waste', 0),
                    footprint_data.get('total', 0)
                ))
    
    def get_footprint_history(self, user_id: int, days: int = 30) -> pd.DataFrame:
        """Get historical footprint data for a user"""
        with sqlite3.connect(self.db_path) as conn:
            query = '''
                SELECT date, transportation_emissions, energy_emissions, 
                       food_emissions, waste_emissions, total_emissions
                FROM daily_footprints 
                WHERE user_id = ? 
                ORDER BY date DESC 
                LIMIT ?
            '''
            
            df = pd.read_sql_query(query, conn, params=(user_id, days))
            df['date'] = pd.to_datetime(df['date'])
            return df.sort_values('date')
    
    def save_activity(self, user_id: int, date: str, category: str, 
                     activity_type: str, amount: float, unit: str, emissions: float):
        """Save individual activity record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO activities 
                (user_id, date, category, activity_type, amount, unit, emissions)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (user_id, date, category, activity_type, amount, unit, emissions))
    
    def get_activities(self, user_id: int, category: str = None, days: int = 30) -> pd.DataFrame:
        """Get activity history for a user"""
        with sqlite3.connect(self.db_path) as conn:
            if category:
                query = '''
                    SELECT * FROM activities 
                    WHERE user_id = ? AND category = ?
                    AND date >= date('now', '-{} days')
                    ORDER BY date DESC
                '''.format(days)
                params = (user_id, category)
            else:
                query = '''
                    SELECT * FROM activities 
                    WHERE user_id = ?
                    AND date >= date('now', '-{} days')
                    ORDER BY date DESC
                '''.format(days)
                params = (user_id,)
            
            return pd.read_sql_query(query, conn, params=params)
    
    def create_goal(self, user_id: int, goal_type: str, target_value: float, 
                   target_date: str = None) -> int:
        """Create a new goal for user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO goals (user_id, goal_type, target_value, target_date)
                VALUES (?, ?, ?, ?)
            ''', (user_id, goal_type, target_value, target_date))
            return cursor.lastrowid
    
    def update_goal_progress(self, goal_id: int, current_value: float):
        """Update progress on a goal"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE goals SET current_value = ? WHERE id = ?
            ''', (current_value, goal_id))
    
    def get_user_goals(self, user_id: int) -> pd.DataFrame:
        """Get all goals for a user"""
        with sqlite3.connect(self.db_path) as conn:
            query = '''
                SELECT * FROM goals 
                WHERE user_id = ? AND status = 'active'
                ORDER BY created_at DESC
            '''
            return pd.read_sql_query(query, conn, params=(user_id,))
    
    def get_monthly_summary(self, user_id: int, year: int, month: int) -> Dict:
        """Get monthly carbon footprint summary"""
        with sqlite3.connect(self.db_path) as conn:
            query = '''
                SELECT 
                    AVG(total_emissions) as avg_daily,
                    SUM(total_emissions) as total_monthly,
                    AVG(transportation_emissions) as avg_transport,
                    AVG(energy_emissions) as avg_energy,
                    AVG(food_emissions) as avg_food,
                    AVG(waste_emissions) as avg_waste,
                    COUNT(*) as days_logged
                FROM daily_footprints 
                WHERE user_id = ? 
                AND strftime('%Y', date) = ? 
                AND strftime('%m', date) = ?
            '''
            
            cursor = conn.cursor()
            cursor.execute(query, (user_id, str(year), f"{month:02d}"))
            row = cursor.fetchone()
            
            if row and row[0] is not None:
                return {
                    'avg_daily': round(row[0], 2),
                    'total_monthly': round(row[1], 2),
                    'avg_transport': round(row[2], 2),
                    'avg_energy': round(row[3], 2),
                    'avg_food': round(row[4], 2),
                    'avg_waste': round(row[5], 2),
                    'days_logged': row[6]
                }
            
            return {
                'avg_daily': 0, 'total_monthly': 0,
                'avg_transport': 0, 'avg_energy': 0,
                'avg_food': 0, 'avg_waste': 0,
                'days_logged': 0
            }
    
    def export_user_data(self, user_id: int, format: str = 'csv') -> str:
        """Export user data to file"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format.lower() == 'csv':
            # Export footprint data
            df_footprints = self.get_footprint_history(user_id, days=365)
            footprint_file = f"data/export_footprints_{user_id}_{timestamp}.csv"
            df_footprints.to_csv(footprint_file, index=False)
            
            # Export activities
            df_activities = self.get_activities(user_id, days=365)
            activities_file = f"data/export_activities_{user_id}_{timestamp}.csv"
            df_activities.to_csv(activities_file, index=False)
            
            return f"Data exported to {footprint_file} and {activities_file}"
        
        elif format.lower() == 'json':
            # Export as JSON
            data = {
                'user': self.get_user(user_id),
                'footprints': self.get_footprint_history(user_id, days=365).to_dict('records'),
                'activities': self.get_activities(user_id, days=365).to_dict('records'),
                'goals': self.get_user_goals(user_id).to_dict('records')
            }
            
            export_file = f"data/export_user_{user_id}_{timestamp}.json"
            with open(export_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            return f"Data exported to {export_file}"
        
        else:
            raise ValueError("Format must be 'csv' or 'json'")
