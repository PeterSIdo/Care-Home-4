import sqlite3
import pandas as pd

conn = sqlite3.connect('care4.db')
cursor = conn.cursor()

# Fetch data
query = '''
    SELECT resident_initials, timestamp, food_name, food_amount, food_note, staff_initials 
    FROM food_chart
'''
df = pd.read_sql_query(query, conn)

conn.close()

# Export DataFRame to Excel file
df.to_excel('food_chart.xlsx', index=False)