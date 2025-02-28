import pandas as pd

# Read the Excel file
# Replace 'your_file.xlsx' with your Excel file name
df = pd.read_excel('bdayexcell.xlsx')    

# Display the first few rows of the data
print("First few rows of the Excel file:")
print(df.head())

# Get basic information about the dataset
print("\nDataset information:")
print(df.info())

# Get basic statistics of numerical columns
print("\nBasic statistics:")
print(df.describe())
