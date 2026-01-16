import pandas as pd

# Load the CSV file
cars = pd.read_csv('quikr_car.csv')

# Filter rows where 'year' is numeric
cars = cars[cars['year'].str.isnumeric()]

# Convert 'year' column to int
cars['year'] = cars['year'].astype(int)

# Clean kms_driven
cars['kms_driven'] = cars['kms_driven'].astype(str).str.extract(r'([0-9,]+)')[0].str.replace(',','')
cars['kms_driven'] = pd.to_numeric(cars['kms_driven'], errors='coerce')
cars = cars.dropna(subset=['kms_driven']).copy()
cars['kms_driven'] = cars['kms_driven'].astype(int)
cars.reset_index(drop=True, inplace=True)

# Clean Price
cars = cars[cars['Price'] != "Ask For Price"]
cars['Price'] = cars['Price'].str.replace(',','').astype(int)

# Further clean kms_driven
cars['kms_driven'] = cars['kms_driven'].astype(str).str.split(' ').str.get(0).str.replace(',','')
cars = cars[cars['kms_driven'].str.isnumeric()]
cars['kms_driven'] = cars['kms_driven'].astype(int)

# Drop rows with missing fuel_type
cars = cars[~cars['fuel_type'].isna()]

# Shorten name to first 3 words
cars['name'] = cars['name'].str.split(' ').str.slice(0,3).str.join(' ')

# Filter out high prices
cars = cars[cars['Price']<6e6].reset_index(drop=True)

# Save the cleaned data
cars.to_csv('cleaned_cars.csv', index=False)

print("Data cleaned and saved to 'cleaned_cars.csv'")
