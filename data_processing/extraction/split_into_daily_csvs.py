import pandas as pd
import pathlib

def split_into_daily_subsets(year, table: pd.DataFrame, dump_path: pathlib.Path):
    dump_path.mkdir(parents=True, exist_ok=True)

    subset_table = table[table["datetime"].dt.year == year]

    for day, df in subset_table.groupby("datetime"):
        df.to_csv(dump_path / f"{day.strftime('%Y-%m-%d')}.csv")