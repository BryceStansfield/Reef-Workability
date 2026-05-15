# Calculates realistic wind component ranges for given wave heights from WHACS hindcast data applied to reef centroids.
import pandas as pd
from scipy.spatial import ConvexHull

class WindWaveConstraintAnalysis:
    def __init__(self, reef_centroid_weather_df: pd.DataFrame):
        self.reef_centroid_weather_df = reef_centroid_weather_df
        self.compute()
        self.compute_quantiles()

    def compute(self):
        # We get a convex hull of u_wind, and v_wind by month.
        self.convex_hulls = {}
        
        for month, df in self.reef_centroid_weather_df[["month", "u_wind", "v_wind"]].groupby('month'):
            new_df = df.copy()
            new_df.drop(columns=["month"], inplace=True)
            self.convex_hulls[month] = ConvexHull(new_df.values)
    
    def compute_quantiles(self):
        # We get the 1st and 99th percentile of u, v, wind magnitude, and wave height for each month.
        # This is to draw a realistic box of weather conditions for later graphing.
        self.quantiles_by_month = self.reef_centroid_weather_df[["month", "wave_height", "u_wind", "v_wind", "wind_magnitude"]].groupby('month').quantile([0.01, 0.99]).unstack(level=1)
   
    def get_quantiles_for_month(self, month, attribute):        
        return self.quantiles_by_month.loc[month][attribute]
