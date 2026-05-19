import pathlib
from data_processing.collection.download_tools import *

def download_noaa_ww3(download_path: pathlib.Path):
    url_filenames = [
        ("https://erddap.aoml.noaa.gov/hdb/erddap/griddap/WaveWatch_2025.nc?Thgt%5B(2025-01-01):1:(2025-12-31T23:00:00Z)%5D%5B(-8):1:(-45)%5D%5B(96):1:(168)%5D", "2025_wave_heights.nc")
    ]

    for url, filename in url_filenames:
        download_file(url, download_path, None, filename)
