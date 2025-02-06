This script extracts historical monthly climate data (in NetCDF format) from the Copernicus Climate Data Store and processes it to generate time series for specific cities using latitude and longitude coordinates.

Key Steps:
1. Install Dependencies: The required libraries openpyxl and netCDF4 are installed for reading city-level data from an Excel file and accessing climate data from the NetCDF file.

2. Load City Data: The cities_ESP.xlsx file is loaded, which contains the latitude and longitude coordinates of cities.

3. Access Copernicus Global Data: The monthly global climate data (global.nc file) is accessed using the netCDF4 library. The script retrieves temperature data (t2m) and the latitude and longitude variables from the NetCDF file.

4. Match City Coordinates to Climate Data:
The latitude and longitude values for each city from the Excel file are used to find the closest matching coordinates in the global dataset by calculating the squared differences between each city's latitude and longitude and the climate dataset's latitude and longitude.

5. Time Series Generation: The script generates time series data for each city, extracting temperature data (t2m) corresponding to each city’s coordinates across the time dimension.

6. Saving Data: The time series data for each city is saved as a CSV file with the city name as the filename. The data is indexed by Date-Time and contains the temperature data for each city.
