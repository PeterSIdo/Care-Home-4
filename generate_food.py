import pandas as pd
import random
from datetime import datetime, timedelta

# Load the food list from the CSV file
food_list = pd.read_csv('c:/Users/Peter/Documents/Care-Home-4/app/instance/food_list.csv', header=None)
food_list.columns = ['food_name']

# Define meal times
meal_times = {
    'breakfast': ('08:00', '09:30'),
    'lunch': ('12:30', '13:30'),
    'supper': ('18:00', '19:30')
}

# Function to generate a random timestamp within a given time range
def random_time(start, end):
    start_time = datetime.strptime(start, '%H:%M')
    end_time = datetime.strptime(end, '%H:%M')
    random_time = start_time + timedelta(minutes=random.randint(0, int((end_time - start_time).total_seconds() / 60)))
    return random_time.strftime('%Y-%m-%d %H:%M:%S')

# Generate daily food intake data
def generate_food_intake_data(food_list, meal_times):
    data = []
    for meal, (start, end) in meal_times.items():
        food_item = random.choice(food_list['food_name'])
        timestamp = random_time(start, end)
        data.append({
            'resident_initials': 'AB',
            'timestamp': timestamp,
            'food_name': food_item,
            'food_amount': random.randint(1, 3),  # Random amount
            'food_note': '',
            'staff_initials': 'XY'
        })
    return data

# Generate data
food_intake_data = generate_food_intake_data(food_list, meal_times)

# Convert the data to a DataFrame
df = pd.DataFrame(food_intake_data)

# Export to CSV
df.to_csv('daily_food_intake.csv', index=False)