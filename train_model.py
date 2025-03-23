import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import pickle
import os

# Function to categorize health metrics based on medical ranges
def categorize_health_metrics(df):
    print("Categorizing health metrics...")
    # Initialize columns for categories
    df['heart_rate_category'] = 'Normal'
    df['respiratory_rate_category'] = 'Normal'
    df['body_temp_category'] = 'Normal'

    # Categorize Heart Rate (bpm)
    for idx, row in df.iterrows():
        age = row['age']
        heart_rate = row['heart_rate']

        if age < 1:  # Newborns (0–1 year)
            if heart_rate < 70 or heart_rate > 190:
                df.at[idx, 'heart_rate_category'] = 'Emergency'
            elif (heart_rate >= 70 and heart_rate < 100) or (heart_rate > 150 and heart_rate <= 190):
                df.at[idx, 'heart_rate_category'] = 'Abnormal'
        elif age < 12:  # Children (1–11 years)
            if heart_rate < 60 or heart_rate > 160:
                df.at[idx, 'heart_rate_category'] = 'Emergency'
            elif (heart_rate >= 60 and heart_rate < 80) or (heart_rate > 120 and heart_rate <= 160):
                df.at[idx, 'heart_rate_category'] = 'Abnormal'
        else:  # Adults (12+ years)
            if heart_rate < 40 or heart_rate > 180:
                df.at[idx, 'heart_rate_category'] = 'Emergency'
            elif (heart_rate >= 40 and heart_rate < 60) or (heart_rate > 100 and heart_rate <= 180):
                df.at[idx, 'heart_rate_category'] = 'Abnormal'

    # Categorize Respiratory Rate (breaths/min)
    for idx, row in df.iterrows():
        age = row['age']
        respiratory_rate = row['respiratory_rate']

        if age < 1:  # Newborns
            if respiratory_rate < 30 or respiratory_rate > 70:
                df.at[idx, 'respiratory_rate_category'] = 'Emergency'
            elif (respiratory_rate >= 30 and respiratory_rate < 40) or (respiratory_rate > 50 and respiratory_rate <= 70):
                df.at[idx, 'respiratory_rate_category'] = 'Abnormal'
        elif age < 12:  # Children
            if respiratory_rate < 20 or respiratory_rate > 50:
                df.at[idx, 'respiratory_rate_category'] = 'Emergency'
            elif (respiratory_rate >= 20 and respiratory_rate < 25) or (respiratory_rate > 30 and respiratory_rate <= 50):
                df.at[idx, 'respiratory_rate_category'] = 'Abnormal'
        else:  # Adults
            if respiratory_rate < 8 or respiratory_rate > 40:
                df.at[idx, 'respiratory_rate_category'] = 'Emergency'
            elif (respiratory_rate >= 8 and respiratory_rate < 12) or (respiratory_rate > 20 and respiratory_rate <= 40):
                df.at[idx, 'respiratory_rate_category'] = 'Abnormal'

    # Categorize Body Temperature (°F)
    for idx, row in df.iterrows():
        body_temp = row['body_temp']
        if body_temp < 95 or body_temp > 104:
            df.at[idx, 'body_temp_category'] = 'Emergency'
        elif (body_temp >= 95 and body_temp < 97) or (body_temp > 99 and body_temp <= 104):
            df.at[idx, 'body_temp_category'] = 'Abnormal'

    return df

# Load the data
print("Loading data...")
try:
    data = pd.read_csv("health_metrics_data.csv")
except FileNotFoundError:
    print("Error: 'health_metrics_data.csv' not found. Please ensure the file exists in the current directory.")
    exit(1)
print(f"Loaded {len(data)} records.")

# Verify the expected columns are present
expected_columns = ['age', 'bmi', 'heart_rate', 'respiratory_rate', 'body_temp']
if not all(col in data.columns for col in expected_columns):
    print(f"Error: CSV file must contain the following columns: {expected_columns}")
    print(f"Found columns: {list(data.columns)}")
    exit(1)

# Categorize the health metrics
data = categorize_health_metrics(data)

# Features and target labels
features = ['age', 'bmi', 'heart_rate', 'respiratory_rate', 'body_temp']
target_columns = ['heart_rate_category', 'respiratory_rate_category', 'body_temp_category']

# Encode the categorical labels
print("Encoding categorical labels...")
label_encoders = {}
for metric in ['heart_rate', 'respiratory_rate', 'body_temp']:
    le = LabelEncoder()
    data[f'{metric}_category'] = le.fit_transform(data[f'{metric}_category'])
    label_encoders[metric] = le
    # Save the label encoder as a .pkl file
    with open(f'{metric}_label_encoder.pkl', 'wb') as file:
        pickle.dump(le, file)
    print(f"Saved label encoder for {metric} as {metric}_label_encoder.pkl")

# Prepare the features and target data for multi-output classification
X = data[features]
y = data[target_columns]

# Split the data into training and testing sets
print("Splitting data into training and testing sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a single multi-output model
print("Training a single multi-output model...")
base_model = RandomForestClassifier(n_estimators=100, random_state=42)
model = MultiOutputClassifier(base_model, n_jobs=-1)  # n_jobs=-1 for parallel processing
model.fit(X_train, y_train)

# Evaluate the model for each metric
print("\nEvaluating the model...")
for i, metric in enumerate(['heart_rate', 'respiratory_rate', 'body_temp']):
    y_pred = model.predict(X_test)[:, i]
    y_true = y_test.iloc[:, i]
    accuracy = np.mean(y_pred == y_true)
    print(f"Accuracy for {metric}: {accuracy:.4f}")

# Save the model as a single .pkl file
print("\nSaving the trained model...")
with open('trained_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Trained model saved as 'trained_model.pkl'.")
print("Label encoders saved as 'heart_rate_label_encoder.pkl', 'respiratory_rate_label_encoder.pkl', and 'body_temp_label_encoder.pkl'.")
print("Training completed successfully.")