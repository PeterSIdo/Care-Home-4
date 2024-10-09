import sys
import os
from datetime import datetime  # Add this import statement

# Add the absolute path to the Python path
sys.path.append('c:/Users/Peter/Documents/CareRecordsPG')

from app.db.db_connection import get_db
from app.models import FluidChart
from db_connection import connect_to_db

def main():
    SessionLocal = connect_to_db()
    session = SessionLocal()  # Create a session instance
    try:
        # Optionally, execute a simple query to verify the connection
        session.execute("SELECT 1")
        print("Database connection established:", session)
    finally:
        session.close()  # Ensure the session is closed

def insert_test_data():
    db = next(get_db())
    test_data = [
        FluidChart(
            resident_initials='JD',
            timestamp=datetime.now(),
            fluid_type='Water',
            fluid_volume=250,
            fluid_note='Morning intake',
            staff_initials='AB'
        ),
        FluidChart(
            resident_initials='Peter',
            timestamp=datetime.now(),
            fluid_type='beer',
            fluid_volume=330,
            fluid_note='Lunch intake',
            staff_initials='CD'
        )
    ]
    db.add_all(test_data)
    db.commit()
    
    print("Test data inserted successfully.")

if __name__ == "__main__":
    insert_test_data()