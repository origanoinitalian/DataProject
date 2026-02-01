import requests
import json
import pandas as pd
import os
import time
from datetime import datetime, timedelta

class DataProcessor:
    def __init__(self, start_time: str, end_time: str, save_raw_path: str, save_clean_path: str):
        self._start_time = datetime.strptime(start_time, "%Y-%m-%d")
        self._end_time = datetime.strptime(end_time, "%Y-%m-%d")
        self._save_raw_path = save_raw_path
        self._save_clean_path = save_clean_path
        self._base_url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

    def _fetch_single_chunk(self, start: datetime, end: datetime):
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
        cleaned_df.to_csv(self._save_clean_path, index=False)
        print(f"Cleaned data saved: {self._save_clean_path}")


def manage_data(should_fetch: bool, start_time: str = None, end_time: str = None) -> None:
    RAW_PATH = 'data/raw/raw_earthquakes.json'
    CLEAN_PATH = 'data/cleaned/cleaned_earthquakes.csv'

    if not start_time or not end_time:
        end_time = datetime.now().strftime('%Y-%m-%d')
        start_time = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        print(f"Default dates : {start_time} -> {end_time}")

    processor = DataProcessor(start_time, end_time, RAW_PATH, CLEAN_PATH)

    if should_fetch:
        processor.fetch_data()
        processor.clean_data()
    else:
        if not os.path.exists(CLEAN_PATH):
            print("Careful, no local data found: run with --fetch-data")

def data_loader():
    DATA_PATH = "data/cleaned/cleaned_earthquakes.csv"
    if not os.path.exists(DATA_PATH):
        return pd.DataFrame()
    
    df = pd.read_csv(DATA_PATH)
    if 'date-time' in df.columns:
        df['date-time'] = pd.to_datetime(df['date-time'])
    return df
