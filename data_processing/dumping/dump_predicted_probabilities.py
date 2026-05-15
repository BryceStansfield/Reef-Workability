import pandas as pd
import pathlib

def dump_daily_probs_for_year(predicted_workability, year, dump_directory: pathlib.Path, as_daily_csvs=True):
    dump_directory.mkdir(parents=True, exist_ok=True)

    subset = predicted_workability[predicted_workability["datetime"].year == year]
    
    if as_daily_csvs:
        for day, df in subset.groupby("datetime"):
            csv_path = dump_directory / f"{day.strftime('%Y-%m-%d')}.csv"

            df.to_csv(csv_path)
    else:
        subset.to_csv(dump_directory / f"{year}.csv")