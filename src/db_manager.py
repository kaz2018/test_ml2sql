import sqlite3
import pandas as pd
from typing import List, Dict, Any, Optional
from pathlib import Path

class DatabaseManager:
    def __init__(self, db_path: str = "database/sample.db"):
        self.db_path = db_path
        self.connection = None
        
    def __enter__(self):
        self.connect()
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        
    def connect(self):
        """Connect to SQLite database"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            
    def initialize_database(self):
        """Initialize database with schema and sample data"""
        try:
            # Create tables
            with open('database/schema.sql', 'r') as f:
                self.connection.executescript(f.read())
                
            # Check if data already exists
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM products")
            if cursor.fetchone()[0] == 0:
                # Insert sample data
                with open('database/sample_data.sql', 'r') as f:
                    self.connection.executescript(f.read())
                    
            self.connection.commit()
            print("Database initialized successfully")
            
        except Exception as e:
            print(f"Error initializing database: {e}")
            self.connection.rollback()
            
    def execute_query(self, query: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """Execute SQL query and return results"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            # Fetch results
            results = []
            for row in cursor.fetchall():
                results.append(dict(row))
                
            return results
            
        except Exception as e:
            print(f"Error executing query: {e}")
            return []
            
    def execute_query_df(self, query: str, params: Optional[tuple] = None) -> pd.DataFrame:
        """Execute SQL query and return results as DataFrame"""
        try:
            if params:
                return pd.read_sql_query(query, self.connection, params=params)
            else:
                return pd.read_sql_query(query, self.connection)
                
        except Exception as e:
            print(f"Error executing query: {e}")
            return pd.DataFrame()
            
    def get_table_info(self) -> Dict[str, List[str]]:
        """Get information about database tables and columns"""
        cursor = self.connection.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        table_info = {}
        for table in tables:
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [(row[1], row[2]) for row in cursor.fetchall()]
            table_info[table] = columns
            
        return table_info