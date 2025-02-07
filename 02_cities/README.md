# City-Level Time Series Data Extraction from global.nc file extracted in 01_download

This script extracts historical monthly climate data (in NetCDF format) from the **Copernicus Climate Data Store (CDS)** and processes it to generate time series for specific cities using latitude and longitude coordinates.

## Key Steps:

### 1. Install Dependencies:
The required libraries `openpyxl` and `netCDF4` are installed for:
- Reading city-level data from an Excel file (`IND_cities.xlsx`).
- Accessing climate data from the Copernicus global NetCDF file (`global.nc`).
- *Note: The global.nc data is not uploaded here due to storage constraints. However, following the steps in 01_download will allow access to the dataset.*

### 2. Load City Data: 
The IND_cities.xlsx file, which contains the latitude and longitude coordinates of Indian cities, is loaded.
- The city coordinates were obtained from the **SEDAC Gridded Population of the World v4**, which originally provided shapefiles.
- These shapefiles were converted into an Excel file (IND_cities.xlsx) to facilitate data extraction.

### 3. Access Copernicus Global Data:
The monthly global climate data (global.nc file) is accessed using the netCDF4 library. The script retrieves **temperature data (t2m)** and the latitude and longitude variables from the NetCDF file.

### 4. Match City Coordinates to Climate Data:
For each city in the Excel file, the script calculates the squared differences between the city’s latitude and longitude and the latitude and longitude from the global dataset. This allows the script to identify the closest matching coordinates in the global dataset.

### 5. Time Series Generation: 
The script generates time series data for each city by extracting the corresponding temperature data (t2m) at the closest latitude and longitude coordinates for each time point. The time series is indexed by Date-Time, which is calculated from the time variable in the NetCDF file.

### 6. Saving Data: 
The generated time series data for each city is saved as a CSV file. Each file is named after the city and contains two columns:
*Date-Time*: The date and time of the observation.
*Temperature (°C)*: The temperature data (t2m) corresponding to that date and
