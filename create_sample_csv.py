
import pandas as pd
import os

large_csv_path = os.path.join("data", "openfoodfacts.csv")
sample_csv_path = os.path.join("data", "sample_openfoodfacts.csv")

# Create the data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

try:
    # Read the first 10,000 rows of the large CSV
    df = pd.read_csv(large_csv_path, nrows=10000, sep='\t', engine='python', on_bad_lines='skip')
    
    # Save the sample to a new CSV file
    df.to_csv(sample_csv_path, index=False)
    
    print(f"Successfully created a sample CSV with 10,000 rows at: {sample_csv_path}")
    
except FileNotFoundError:
    print(f"Error: The file {large_csv_path} was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
