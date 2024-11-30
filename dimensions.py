import pandas as pd

# Function to calculate L, B, H
def calculate_lbh(df):
    df['L'] = (df['x2'] - df['x1']).abs()  # Length
    df['B'] = (df['y2'] - df['y1']).abs()  # Breadth
    df['H'] = (df['z2'] - df['z1']).abs()  # Height
    return df[['L', 'B', 'H']]  # Return only L, B, H columns

# Input and output CSV files
input_csv = "output1.csv"
output_csv = "cuboid_dimensions.csv"

# Read the input file
data = pd.read_csv(input_csv)

# Calculate dimensions
dimensions = calculate_lbh(data)

# Save the results to a new file
dimensions.to_csv(output_csv, index=False)
