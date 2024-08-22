import pandas as pd
import sqlite3

# Step 1: Read the CSV file into a DataFrame
csv_file_path = 'c:/Users/Peter/Documents/Care-Home-4/populate_food_chart.csv'
df = pd.read_csv(csv_file_path)

# Step 2: Connect to the SQLite database
db_path = 'c:/Users/Peter/Documents/Care-Home-4/care4.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 3: Insert data into the food_chart table
for index, row in df.iterrows():
    cursor.execute('''
        INSERT INTO food_chart (resident_initials, timestamp, food_name, food_amount, food_note, staff_initials)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (row['resident_initials'], row['timestamp'], row['food_name'], row['food_amount'], row['food_note'], row['staff_initials']))

# Commit the transaction and close the connection
conn.commit()
conn.close()