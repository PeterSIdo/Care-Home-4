# c:/Users/Peter/Documents/Care-Home-4/app/utils.py
import hashlib
import time

def generate_unique_id(name, surname):
    # Combine name, surname, and the current timestamp
    full_name = f"{name}{surname}{time.time()}"
    # Generate a hash of the combined string
    unique_id = hashlib.sha256(full_name.encode()).hexdigest()[:10]  # Truncate for brevity
    return unique_id