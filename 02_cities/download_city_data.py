# Install required packages
%pip install openpyxl
%pip install netCDF4

import pandas as pd
import netCDF4 as nc
import datetime
import os

# Load city data with latitude and longitude coordinates
df = pd.read_excel('/kaggle/input/cities-esp/IND_cities.xlsx', index_col=0)

# Load the NetCDF global climate data
data = nc.Dataset("/kaggle/input/monthly/global.nc")
longitude_values = df['CENTROID_X'].values
latitude_values = df['CENTROID_Y'].values

lat = data.variables['latitude'][:]
lon = data.variables['longitude'][:]
temp_data = data.variables['t2m'][:]

# Extract time data
unit = data.variables['time'].units
times = data.variables['time'][:]
ref_date = datetime.datetime(int(unit[12:16]), int(unit[17:19]), int(unit[20:22]))

# Directory to save output files
dir_out = "/kaggle/working/output"

# Loop through cities and extract time series for each city
for key, value in df.iterrows():
    country = key
    file_name = "{}.csv".format(country)
    lon_point = value[1]
    lat_point = value[2]

    # Calculate squared differences to find closest match for latitude and longitude
    sq_diff_lat = (lat - lat_point)**2
    sq_diff_lon = (lon - lon_point)**2
    min_index_lat = sq_diff_lat.argmin()
    min_index_lon = sq_diff_lon.argmin()

    # Generate time series data
    date_range = []
    temp = []
    for index, time in enumerate(times):
        date_time = ref_date + datetime.timedelta(hours=int(time))
        date_range.append(date_time)
        temp.append(temp_data[index, 0, min_index_lat, min_index_lon])

    # Create a DataFrame and save to CSV
    df_out = pd.DataFrame(date_range, columns=["Date-Time"])
    df_out["Date-Time"] = date_range
    df_out = df_out.set_index(["Date-Time"])
    df_out["Temp({})".format(unit)] = temp

    # Save to output directory
    df_out.to_csv(os.path.join(dir_out, file_name), index=True)

    print(f"Time series data for {country} saved as {file_name}")
