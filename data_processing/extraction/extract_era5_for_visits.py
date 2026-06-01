# Extracts wave height, u-wind, and v-wind from WHACS hindcast NetCDF files for failed
# COTS survey visits between 2020 and 2024, using KDTree lookup to the nearest grid point.

import pandas as pd
import numpy as np
import pathlib

from data_processing.extraction.weather_extractor import ERA5Extractor

def construct_csvs_with_era5_weather_data(cots_dfs_with_coords: list[pd.DataFrame], era5_base_path: pathlib.Path) -> list[pd.DataFrame]:
    # Initializing our WhacsWeatherExtractor.
    era5_extractor = ERA5Extractor(era5_base_path)

    result_dfs = []

    for cots_with_coords in cots_dfs_with_coords:
        # First let's filter our df down.
        cots_df = cots_with_coords.dropna(subset=['x', 'y'])
        dropped_num = len(cots_with_coords) - len(cots_df)
        if dropped_num > 0:
            print(f"Dropping {dropped_num} rows due to missing coordinates.")
        
        # The one absolute incompatibility between our surveyData and our COTS data is the name of the date column.
        # Otherwise, both can use this function just fine.
        if "Date " in cots_df.columns:
            cots_df.rename(columns={"Date ": "date"}, inplace=True)
            cots_df['date'] = pd.to_datetime(cots_df['date'], dayfirst=True, errors='raise')
        elif "Date" in cots_df.columns:
            cots_df.rename(columns={"Date": "date"}, inplace=True)
            cots_df['date'] = pd.to_datetime(cots_df['date'], dayfirst=True, errors='raise')
        elif "date" in cots_df.columns:
            cots_df['date'] = pd.to_datetime(cots_df['date'], format="ISO8601", errors='raise')
        else:
            raise Exception("No date column found in COTS data. Available columns: " + ", ".join(cots_df.columns))
        
        filtered_df = cots_df[(cots_df['date'] >= '2005-01-01') & (cots_df['date'] < '2026-01-01')]
        dropped_num = len(cots_df) - len(filtered_df)
        if dropped_num > 0:
            print(f"Dropping {dropped_num} rows falling outside of 2020-2023.")
        
        cots_df = filtered_df

        if len(cots_df) == 0:
            raise Exception("No COTS visits found after filtering.")
            
        # Adding and filling our new weather columns.
        results = {
            'wave_height': [],
            'wave_period': [],
            'wave_direction': [],
            'precipitation': [],
            'u_wind': [],
            'v_wind': []
        }

        for _, row in cots_df.iterrows():
            date = row['date']
            x_coord = row['x']
            y_coord = row['y']
            coords = np.array([[x_coord, y_coord]])

            wave_height = era5_extractor.extract_batch_daytime_hours_mean_by_parameter("swh", date, coords)[0]
            wave_period = era5_extractor.extract_batch_daytime_hours_mean_by_parameter("mwp", date, coords)[0]
            wave_direction = era5_extractor.extract_batch_daytime_hours_mean_by_parameter("mwd", date, coords)[0]
            precipitation = era5_extractor.extract_batch_daytime_hours_mean_by_parameter("avg_tprate", date, coords)[0]
            u_wind = era5_extractor.extract_batch_daytime_hours_mean_by_parameter("u10", date, coords)[0]
            v_wind = era5_extractor.extract_batch_daytime_hours_mean_by_parameter("v10", date, coords)[0]

            results['wave_height'].append(wave_height)
            results['wave_period'].append(wave_period)
            results['wave_direction'].append(wave_direction)
            results['precipitation'].append(precipitation)
            results['u_wind'].append(u_wind)
            results['v_wind'].append(v_wind)

        cots_df = pd.concat([
            cots_df,
            pd.DataFrame(results, index=cots_df.index)
        ], axis=1)

        result_dfs.append(cots_df)

    return result_dfs