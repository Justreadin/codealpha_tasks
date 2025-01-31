import pandas as pd
from scripts.db_operations import fetch_data

# Fetch data from the database
df = fetch_data()

# Display the first few rows to inspect the data
print("Data Sample:")
print(df.head())

# Check for missing values
print("\nMissing Values Summary:")
print(df.isnull().sum())
