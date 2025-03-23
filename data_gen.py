import random
import csv
import os

# Function to calculate BMI
def calculate_bmi(weight_lb, height_cm):
    weight_kg = weight_lb * 0.453592  # Convert lbs to kg
    height_m = height_cm / 100  # Convert cm to meters
    if height_m == 0:  # Prevent division by zero
        height_m = 1.0
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)

# Function to generate health metrics based on age and BMI
def generate_health_metrics(age, bmi):
    # Heart Rate (bpm): Medically possible range
    heart_rate = random.randint(20, 220)
    if bmi > 30:  # Increase heart rate for obese individuals
        heart_rate = int(heart_rate * 1.1)
        heart_rate = min(heart_rate, 220)  # Cap at the maximum range

    # Respiratory Rate (breaths/min): Medically possible range
    respiratory_rate = random.randint(5, 80)
    if bmi > 30:  # Increase respiratory rate for obese individuals
        respiratory_rate = int(respiratory_rate * 1.1)
        respiratory_rate = min(respiratory_rate, 80)  # Cap at the maximum range

    # Body Temperature (°F): Medically possible range
    body_temp = round(random.uniform(89.6, 107.6), 1)
    if age >= 65:  # Slightly lower max for elderly
        body_temp = round(random.uniform(89.6, 104.1), 1)

    return heart_rate, respiratory_rate, body_temp

# Generate health metrics data
def generate_health_metrics_data(num_records):
    print(f"Generating {num_records} health metrics records...")
    records = []

    for _ in range(num_records):
        # Generate age
        age = random.randint(0, 90)

        # Generate weight and height to calculate BMI
        if age < 1:
            weight_lb = random.randint(6, 15)
        elif age < 12:
            weight_lb = random.randint(20, 100)
        elif age < 18:
            weight_lb = random.randint(60, 200)
        else:
            weight_lb = random.randint(100, 330)
        height_cm = random.randint(50, 200)
        bmi = calculate_bmi(weight_lb, height_cm)

        # Generate health metrics
        heart_rate, respiratory_rate, body_temp = generate_health_metrics(age, bmi)

        record = {
            "age": age,
            "bmi": bmi,
            "heart_rate": heart_rate,
            "respiratory_rate": respiratory_rate,
            "body_temp": body_temp
        }
        records.append(record)

    print(f"Generated {len(records)} health metrics records.")
    return records

# Save data to CSV
def save_to_csv(records, filename="health_metrics_data.csv"):
    if not records:
        print("No data to save.")
        return
    
    try:
        # Ensure the directory exists
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        
        # Get the absolute path for clarity
        absolute_path = os.path.abspath(filename)
        print(f"Attempting to save CSV file to: {absolute_path}")

        headers = records[0].keys()
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for record in records:
                writer.writerow(record)
        print(f"Data saved to {absolute_path}")
    except Exception as e:
        print(f"Error saving data to CSV: {str(e)}")
        raise

# Main execution
if __name__ == "__main__":
    try:
        print(f"Current working directory: {os.getcwd()}")
        # Generate data for 20,000 records
        num_records = 20000
        health_metrics_data = generate_health_metrics_data(num_records)
        save_to_csv(health_metrics_data, filename="health_metrics_data.csv")
    except Exception as e:
        print(f"An error occurred during script execution: {str(e)}")
        raise