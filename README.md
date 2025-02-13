# ERA5 Weather-Inflation Analysis

## Overview
This project analyzes the impact of weather shocks on inflation using ERA5 reanalysis data. The study uses local projection methods and spans over 7 million spatial observations across Germany, India, and Spain.

## Data
- **Source:** ERA5 Reanalysis Data (from ECMWF)
- **Format:** NetCDF, CSV

## Repository Structure
- `01_download/`: Extract historical data on monthly temperature from Copernicus Climate Data Store (CDS) in NetCDF format
- `02_cities/`: Generates a time series on monthly temperature for a specific set of cities for each country
- `03_cities_aggregation/`: Aggregates the city-level temperature data using population weights to determine each country's monthly average from 1995 to 2023. And compute the monthly temperature deviation from the past five-year average.

