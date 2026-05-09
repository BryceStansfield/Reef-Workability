import threading
from datetime import datetime
import requests
import pathlib
from tqdm import tqdm

class DownloadProgress:
    def __init__(self):
        self._lock = threading.Lock()
        self.total_files = 0
        self.completed_files = 0
        self.start_time = datetime.now()

    def update(self):
        with self._lock:
            self.completed_files += 1
            elapsed_time = datetime.now() - self.start_time
            if self.completed_files > 0:
                avg_time_per_file = elapsed_time / self.completed_files
                estimated_total_time = avg_time_per_file * self.total_files
                remaining_time = estimated_total_time - elapsed_time
                print(f"Completed: {self.completed_files}/{self.total_files} files | Remaining time: {remaining_time}")    

def download_file(url: str, folder: pathlib.Path, progress_tracker: DownloadProgress) -> bool:
    try:
        session = requests.Session()
        response = session.get(url, stream=True, timeout=30)

        if response.status_code == 200:
            filename = url.split('/')[-1]
            filepath: pathlib.Path = folder / filename
            folder.mkdir(parents=True, exist_ok=True)

            if filepath.exists() and filepath.stat().st_size == int(response.headers.get('content-length', 0)):
                print(f"File {filename} already exists and is complete. Skipping download.")
                progress_tracker.update()
                return True

            total_size = int(response.headers.get('content-length', 0))

            with tqdm(total=total_size, unit='B', unit_scale=True, desc=filename) as progress_bar:
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content():
                        if chunk:
                            f.write(chunk)
                            progress_bar.update(len(chunk))

            if total_size > 0 and filepath.stat().st_size != total_size:
                print(f"Size mismatch for {filename}. Download may be incomplete.")
                return False

            print(f"Successfully downloaded {filename}")
            progress_tracker.update()
            return True
        else:
            print(f"Failed to download {url}: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")
        return False
