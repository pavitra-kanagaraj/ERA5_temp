# ERA5 Weather-Inflation Analysis

## Overview
This project analyzes the impact of weather shocks on inflation using ERA5 reanalysis data. The study uses local projection methods and spans over 7 million spatial observations across Germany, India, and Spain.

## Data
- **Source:** ERA5 Reanalysis Data (from ECMWF)
- **Format:** NetCDF, CSV

## Methodology
- Extract weather data (temperature, precipitation)
- Aggregate and clean the data
- Conduct time-series and spatial econometric analysis
- Visualize key findings

## Repository Structure
- `data/`: Raw and processed datasets
- `notebooks/`: Jupyter notebooks for analysis
- `scripts/`: Python scripts for automation

## Installation
```bash
pip install -r requirements.txt
