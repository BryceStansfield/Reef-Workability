from data_processing.extraction.whacs_weather_extractor import WhacsWeatherExtractor
import pandas as pd
import pathlib
from datetime import datetime, timedelta
import numpy as np

def extract_historical_whacs_for_centroids(centroids_path: pathlib.Path, whacs_base_path: pathlib.Path, start_date: datetime = datetime(2005,1,1), end_date: datetime = datetime(2023, 12, 31)):
    centroids = []

    with open(centroids_path, 'r') as f:
        centroids_txt = [line.strip() for line in f.readlines()]

        for txt_centroid in centroids_txt:
            if len(txt_centroid) == 0:
                continue

            lat_str, lon_str = txt_centroid.split(",")
            centroids.append((float(lat_str), float(lon_str)))
    
    historical_centroid_weather_data = pd.DataFrame(columns=["centroid_index", "month", "latitude", "longitude", "datetime", "wave_height", "u_wind", "v_wind", "wind_magnitude"])

    cur_date = start_date
    while cur_date <= end_date:
        print(f"Extracting WHACS data for {cur_date.strftime('%Y-%m-%d')}")
        for i, (lat, lon) in enumerate(centroids):
            extractor = WhacsWeatherExtractor(whacs_base_path)
            hs = extractor.extract_batch_6_hours_mean_by_parameter("hs", cur_date, np.array([[lon, lat]]))[0]
            uwnd = extractor.extract_batch_6_hours_mean_by_parameter("uwnd", cur_date, np.array([[lon, lat]]))[0]
            vwnd = extractor.extract_batch_6_hours_mean_by_parameter("vwnd", cur_date, np.array([[lon, lat]]))[0]

            historical_centroid_weather_data = historical_centroid_weather_data.append({
                "centroid_index": i,
                "month": cur_date.month,
                "y": lat,
                "x": lon,
                "datetime": cur_date,
                "wave_height": hs,
                "u_wind": uwnd,
                "v_wind": vwnd,
                "wind_magnitude": np.hypot(uwnd, vwnd)
            }, ignore_index=True)

        cur_date += timedelta(days=1)
    
    return historical_centroid_weather_data