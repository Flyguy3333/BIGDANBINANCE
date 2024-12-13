import pandas as pd

# Load the CSV file
file_path = "candlesticks_with_indicators.csv"
data = pd.read_csv(file_path, header=None, skip_blank_lines=False)

# Identify and remove duplicate header rows
data.columns = data.iloc[0]  # Set the first row as the header
data = data[1:]              # Drop the original header row

# Remove rows with missing data
data_cleaned = data.dropna(how='any')

# Save the cleaned data back to a new CSV
cleaned_file_path = "candlesticks_with_indicators_cleaned.csv"
data_cleaned.to_csv(cleaned_file_path, index=False)

print(f"Cleaned data saved to {cleaned_file_path}")
