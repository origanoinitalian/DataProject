import requests
import json
import pandas as pd
import os
import time
import gzip
import shutil
from datetime import datetime, timedelta, timezone
from src.utils.cache_config import cache
from tqdm import tqdm

class DataProcessor:
    """
    Handles fetching, cleaning, and saving earthquake data from the API.
    """
    def __init__(self, start_time: str, end_time: str, save_raw_path: str, save_clean_path: str):
        """Initializes the processor with time range and file paths."""
        self._start_time = datetime.strptime(start_time, "%Y-%m-%d")
        self._end_time = datetime.strptime(end_time, "%Y-%m-%d")
        self._save_raw_path = save_raw_path
        self._save_clean_path = save_clean_path
        self._base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    def _fetch_single_chunk(self, start: datetime, end: datetime):
        """Fetches a specific time chunk of data from the API."""
        params = {
            'format': 'geojson',
            'starttime': start.strftime("%Y-%m-%d"),
            'endtime': end.strftime("%Y-%m-%d"),
            'minmagnitude': 4
        }
        try:
            response = requests.get(self._base_url, params=params, timeout=20)
            if response.status_code == 429:
                print("Rate limited, waiting 10s.")
                time.sleep(10)
                return self._fetch_single_chunk(start, end)
            response.raise_for_status()
            data = response.json()
            return data.get('features', [])
        except requests.exceptions.RequestException as e:
            print(f"Error on chunk {start.date()} -> {end.date()}: {e}")
            return []

    def fetch_data(self) -> None:
        """Iterates through the date range to fetch and save raw earthquake data."""
        all_features = []
        current_start = self._start_time
        chunk_size = timedelta(days=30)
        print(f"Starting data loading: {self._start_time.date()} -> {self._end_time.date()}")

        while current_start < self._end_time:
            current_end = min(current_start + chunk_size, self._end_time)
            print(f"   ... Currently fetching: {current_start.date()} to {current_end.date()}")
            chunk_features = self._fetch_single_chunk(current_start, current_end)
            for feature in chunk_features:
                props = feature['properties']
                geom = feature['geometry']
                clean_feat = {
                    'id': feature['id'],
                    'magnitude': props['mag'],
                    'magnitude_type': props['magType'],
                    'place': props['place'],
                    'time': props['time'],
                    'title': props['title'],
                    'coordinates': geom['coordinates'],
                    'url': props['url']
                }
                all_features.append(clean_feat)
            current_start = current_end
            time.sleep(1.0) 

        print(f"Data loading over. {len(all_features)} seisms found.")
        os.makedirs(os.path.dirname(self._save_raw_path), exist_ok=True)
        with open(self._save_raw_path, "w") as f:
            json.dump(all_features, f, indent=4)

    def clean_data(self) -> None:
        """Reads raw JSON data, processes columns, and saves as optimized Parquet."""
        if not os.path.exists(self._save_raw_path):
            print("No file found, run --fetch-data")
            return

        with open(self._save_raw_path, 'r') as f:
            data = json.load(f)

        if not data:
            print("Empty file or no data found")
            return

        df = pd.DataFrame(data)
        
        df['longitude'] = df['coordinates'].apply(lambda x: x[0] if x else None)
        df['latitude'] = df['coordinates'].apply(lambda x: x[1] if x else None)
        df['depth'] = df['coordinates'].apply(lambda x: x[2] if x else None)
        df['date-time'] = pd.to_datetime(df['time'], unit='ms')
        df['date-label'] = df['date-time'].dt.strftime('%d-%m-%Y %H:%M')
        df['region'] = df['place'].apply(lambda x: x.split(',')[-1].strip() if x and ',' in x else x)
        
        cols = ['id', 'title', 'magnitude', 'date-time', 'date-label', 
                'latitude', 'longitude', 'depth', 'region', 'url']
        final_cols = [c for c in cols if c in df.columns]
        cleaned_df = df[final_cols]
        
        os.makedirs(os.path.dirname(self._save_clean_path), exist_ok=True)
        cleaned_df.to_parquet(self._save_clean_path, index=False) 
        print(f"Cleaned data saved: {self._save_clean_path}")

    @staticmethod
    def fetch_live_data() -> pd.DataFrame:
        """Fetches the last 24 hours of seismic data for real-time updates."""
        try:
            now = datetime.now(timezone.utc)
            start_time = (now - timedelta(hours=24)).strftime('%Y-%m-%d')
            url = "https://earthquake.usgs.gov/fdsnws/event/1/query"
            params = {'format': 'geojson', 'starttime': start_time, 'minmagnitude': 2}
            
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if not data.get('features'):
                return pd.DataFrame()
            
            features_list = []
            for feature in data['features']:
                props = feature['properties']
                geom = feature['geometry']
                features_list.append({
                    'id': feature['id'],
                    'magnitude': props['mag'],
                    'place': props['place'],
                    'time': props['time'],
                    'latitude': geom['coordinates'][1],
                    'longitude': geom['coordinates'][0],
                    'depth': geom['coordinates'][2],
                    'url': props['url']
                })
            
            df = pd.DataFrame(features_list)
            df['date-time'] = pd.to_datetime(df['time'], unit='ms')
            df['date-label'] = df['date-time'].dt.strftime('%d-%m-%Y %H:%M')
            df['region'] = df['place'].apply(lambda x: x.split(',')[-1].strip() if x and ',' in x else x)
            return df

        except Exception as e:
            print(f"Live Fetch Error: {e}")
            return pd.DataFrame()


def manage_data(should_fetch: bool, start_time: str = None, end_time: str = None) -> None:
    """Orchestrates data fetching and cleaning based on user args."""
    RAW_PATH = 'data/raw/raw_earthquakes.json'
    CLEAN_PATH = 'data/cleaned/cleaned_earthquakes.parquet'

    if not start_time or not end_time:
        end_time = datetime.now().strftime('%Y-%m-%d')
        start_time = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

    processor = DataProcessor(start_time, end_time, RAW_PATH, CLEAN_PATH)

    if should_fetch:
        processor.fetch_data()
        processor.clean_data()
    else:
        if os.path.exists(RAW_PATH) and not os.path.exists(CLEAN_PATH):
            print("Converting existing RAW JSON to Parquet...")
            processor.clean_data()
        elif not os.path.exists(CLEAN_PATH):
            print("Careful, no local data found: run with --fetch-data")
    check_and_download_etopo()

@cache.memoize(timeout=3600)
def data_loader():
    """Loads clean Parquet data with caching."""
    DATA_PATH = "data/cleaned/cleaned_earthquakes.parquet"
    
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
    df = pd.read_parquet(DATA_PATH)
    
    return df

import os
import requests
import gzip
import shutil
from tqdm import tqdm

def check_and_download_etopo():
    """
    Checks if the ETOPO1 file exists. If it doesn't, we download it with a progress bar and unzip it.
    """
    ETOPO_PATH = "data/cleaned/ETOPO1_Ice_g_gdal.grd"
    ETOPO_URL = "https://www.ngdc.noaa.gov/mgg/global/relief/ETOPO1/data/ice_surface/grid_registered/netcdf/ETOPO1_Ice_g_gdal.grd.gz"
    
    if os.path.exists(ETOPO_PATH):
        return

    print("ETOPO1 topography data missing.")
    os.makedirs(os.path.dirname(ETOPO_PATH), exist_ok=True)
    
    try:
        with requests.get(ETOPO_URL, stream=True) as response:
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            block_size = 8192
            temp_gz_path = ETOPO_PATH + ".gz"
            print(f"Downloading from NOAA ({total_size / (1024*1024):.2f} MB)...")
            
            with open(temp_gz_path, 'wb') as f, tqdm(
                desc="Downloading",
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=block_size):
                    size = f.write(chunk)
                    bar.update(size) 

        print("Unzipping topography data...")        
        with gzip.open(temp_gz_path, 'rb') as f_in:
            with open(ETOPO_PATH, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        
        os.remove(temp_gz_path)
        print("ETOPO1 setup complete.")
        
    except Exception as e:
        print(f"Error downloading ETOPO1: {e}")
        print("The 3D globe will appear flat.")
        if os.path.exists(temp_gz_path):
            os.remove(temp_gz_path)