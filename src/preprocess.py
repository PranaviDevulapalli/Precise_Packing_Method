import pandas as pd
import os

# Load raw dataset
df = pd.read_csv("F:/SaiU/semester 4/Sri/data/processed_data.csv")

# Print available columns
print("📋 Available columns:", df.columns.tolist())

# Rename columns to match internal naming convention
df.rename(columns={
    'Length': 'length_inc',
    'Width': 'width_inc',
    'Height': 'height_inc',
    'Weight (kg)': 'weight_kg'
}, inplace=True)

# Drop rows with missing values in key columns
df.dropna(subset=['length_inc', 'width_inc', 'height_inc', 'weight_kg'], inplace=True)

# Feature engineering
df['volume_cm3'] = df['length_inc'] * df['width_inc'] * df['height_inc']
df['density'] = df['weight_kg'] / df['volume_cm3']

# Save the cleaned and engineered dataset
os.makedirs("data", exist_ok=True)
df.to_csv("data/processed_data.csv", index=False)

print("✅ Data Preprocessing Completed. File saved to 'data/processed_data.csv'")
