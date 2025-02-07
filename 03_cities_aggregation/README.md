### Temperature shock calculation 

This script processes temperature data from multiple Indian cities, aggregates the data monthly, 
computes population-weighted average temperatures at the country level, and calculates temperature shocks. 

## Step 1: Read CSV files and Convert Temperatures
- Reads temperature data from multiple CSV files.
- Extract city names from filenames.
- Converts temperature values from Kelvin to Celsius.
- Parses the Date-Time column into a proper datetime format.

## Step 2: Data Filtering and Aggregation
- Filters data from 1995 to 2023.
- Aggregates temperature data at a monthly level.
- Outputs the cleaned dataset (IND_cities_1996.csv).
