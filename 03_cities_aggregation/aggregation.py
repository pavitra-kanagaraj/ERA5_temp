#Housekeeping
import os, sys
cwd = os.getcwd() 
print("Current working directory:", cwd)
import pandas as pd
import glob

Step 1: Read CSV files and convert temperatures
# Function to convert Kelvin to Celsius
def kelvin_to_celsius(kelvin):
    return kelvin - 273.15

# Function to safely convert strings to floats, setting non-numeric values to NaN
def safe_float_conversion(value):
    try:
        return float(value)
    except ValueError:
        return float('nan')

# Get all CSV files in the directory
csv_files = glob.glob("YOUR FILE PATH OF WHERE YOU STORED THE CSV FILES FROM 02_cities")

# List to store DataFrames
data_frames = []
    
# Read each CSV file
for file in csv_files:
    # Extract city name from the filename
    city_name = file.split("/")[-1].split(".csv")[0]
    
    df = pd.read_csv(file, header=0)

    # Check if 'Date-Time' column exists
    if 'Date-Time' in df.columns:
        df['Date-Time'] = pd.to_datetime(df['Date-Time'], dayfirst=True)
    else:
        print(f"'Date-Time' column not found in {file}")
        continue
    
    # Convert temperature values to float
    df['Temp(K)'] = df['Temp(K)'].apply(safe_float_conversion)      
    df['Temp(C)'] = df['Temp(K)'].apply(kelvin_to_celsius)
    # Add city column
    df['City'] = city_name
    
    # Append the DataFrame to the list
    data_frames.append(df)

# Step 2: Combining Data and Monthly Aggregation
# Combine all DataFrames into one
combined_df = pd.concat(data_frames, ignore_index=True)

# Save the total DataFrame as an Excel file
combined_df.to_csv('Output/IND_cities.csv', index=False) 

combined_df
import datetime

# Filter data for the specified date range (I NEED ONLY FROM THEN SINCE THE ECONOMIC DATA ON INFLATION IS AVAILABLE ONLY THEN)
start_date = datetime.datetime(1995, 1, 1)
end_date = datetime.datetime(2023, 12, 31)
filtered_df = combined_df[(combined_df['Date-Time'] >= start_date) & (combined_df['Date-Time'] <= end_date)]

# Save the filtered DataFrame as an Excel file
filtered_df.to_csv('Output/IND_cities_1996.csv', index=False)
import pandas as pd

cleaned_df = filtered_df
cleaned_df.columns
import datetime

# Convert 'Date-Time' column to datetime format
cleaned_df['Date-Time'] = pd.to_datetime(cleaned_df['Date-Time'])

# Create a new column 'Year' to store the year information
cleaned_df['Year'] = cleaned_df['Date-Time'].dt.year
cleaned_df['Month'] = cleaned_df['Date-Time'].apply(lambda x: str(x)[8:10])
cleaned_df['Month'] = cleaned_df['Month'].astype(int)

cleaned_df
# Group the data by both 'Year' and 'Month' and calculate the sum of temperature for each group
monthly_sum_temp = cleaned_df.groupby(['Year', 'Month'])['Temp(C)'].mean()
# Reset index to include 'Month' as a column
monthly_sum_temp_1 = monthly_sum_temp.reset_index()

# Save the averaged monthly DataFrame as an Excel file
monthly_sum_temp_1.to_excel('Output/IND_AVE_MONTH.xlsx', index=False)

# Step 3: Population weighted-average of temperature
# Load the population data
population_df = pd.read_excel("cities_IND.xlsx", header=0)
population_df

# Reshape population data to long format
population_long_df = population_df.melt(id_vars=['City_Number', 'CENTROID_X', 'CENTROID_Y'], 
                                        value_vars=['UN_2000_E', 'UN_2005_E', 'UN_2010_E', 'UN_2015_E', 'UN_2020_E'], 
                                        var_name='Year', value_name='Population')

# Extract year from the 'Year' column
population_long_df['Year'] = population_long_df['Year'].str.extract('(\d+)').astype(int)
population_long_df.rename(columns={'City_Number': 'City'}, inplace=True)
population_long_df

# Create a complete DataFrame for interpolation
years = range(2000, 2024)
cities = population_long_df['City'].unique()
index = pd.MultiIndex.from_product([years, cities], names=['Year', 'City'])
population_full_df = pd.DataFrame(index=index).reset_index()

# Merge and interpolate
population_full_df = population_full_df.merge(population_long_df, on=['Year', 'City'], how='left')
population_full_df['Population'] = population_full_df.groupby('City')['Population'].transform(lambda x: x.interpolate())

# Ensure no missing values remain
#assert population_full_df['Population'].isna().sum() == 0
population_full_df

cleaned_df['City'] = cleaned_df['City'].astype(str)
population_full_df['City'] = population_full_df['City'].astype(str)

# Merge temperature data with the interpolated population data
merged_df = cleaned_df.merge(population_full_df, left_on=['Year', 'City'], right_on=['Year', 'City'])
merged_df 

# Compute the population-weighted average temperature for each month
def population_weighted_avg(group):
    return (group['Temp(C)'] * group['Population']).sum() / group['Population'].sum()

# Group by year and month and compute the weighted average
population_weighted_avg_df = merged_df.groupby(['Year', 'Month']).apply(population_weighted_avg).reset_index()
population_weighted_avg_df.columns = ['Year', 'Month', 'Population_Weighted_Avg_Temp(C)']

# Save the result to a Excel file
population_weighted_avg_df.to_excel('Output/weighted_avg_temp.xlsx', index=False)

#  Step 4: Calculate the shock
# Convert 'Year' and 'Month' to datetime format
population_weighted_avg_df['Date'] = pd.to_datetime(population_weighted_avg_df['Year'].astype(str) + '-' + population_weighted_avg_df['Month'].astype(str) + '-01')
population_weighted_avg_df
# Iterate through each year and month from 2000 to 2023
for year in range(2005, 2024):  # Starting from 2000 instead of 1999
    for month in range(1, 13):
        # Define the range for the past five years
        start_year = year - 5
        end_year = year - 1
        
        # Filter data for the past five years for the same month
        past_five_years_data = population_weighted_avg_df[(population_weighted_avg_df['Year'] >= start_year) & 
                                                          (population_weighted_avg_df['Year'] <= end_year) & 
                                                          (population_weighted_avg_df['Month'] == month)]
        
        # Calculate the five-year average temperature for the current month
        if not past_five_years_data.empty:
            five_year_avg = past_five_years_data['Population_Weighted_Avg_Temp(C)'].mean()
        
            # Get the temperature for the current month and year
            current_temp = population_weighted_avg_df[(population_weighted_avg_df['Year'] == year) & 
                                                      (population_weighted_avg_df['Month'] == month)]['Population_Weighted_Avg_Temp(C)'].values
            if len(current_temp) > 0:
                deviation = current_temp[0] - five_year_avg
                results.append({
                    'Year': year,
                    'Month': month,
                    'Temp(C)': current_temp[0],
                    'Five_Year_Avg_Temp(C)': five_year_avg,
                    'Deviation': deviation
                })

# Convert the results to a DataFrame
results_df = pd.DataFrame(results)

# Convert 'Year' and 'Month' to datetime format
results_df['Date'] = pd.to_datetime(results_df['Year'].astype(str) + '-' + results_df['Month'].astype(str) + '-01')

# Display the results
print(results_df)

results_df.to_excel('Output/w_shock_IND.xlsx', index=False)
