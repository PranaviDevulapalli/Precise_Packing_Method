import pandas as pd

# Load dataset
df = pd.read_csv("C:/Users/DELL/Downloads/ecommerce_product_dataset.csv")  # Adjust path as needed

# Rename columns for consistency
df.rename(columns={
    'Length (cm)': 'Length',
    'Breadth (cm)': 'Width',
    'Height (cm)': 'Height'
}, inplace=True)

# Compute Volume (L × W × H)
df['Volume'] = df['Length'] * df['Width'] * df['Height']

# Save processed dataset
df.to_csv("data/processed_data.csv", index=False)

print("✅ Feature Engineering Completed. Processed data saved!")
