import requests
import json
import pandas as pd

class DataProcessor:
    def __init__(self, start_time: str, end_time: str, save_raw_path: str, save_clean_path: str) -> None:
        self._start_time = start_time
        self._end_time = end_time
        self._save_raw_path = save_raw_path
        self._save_clean_path = save_clean_path

    def fetch_data(self) -> None:
        response = requests.get(f'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={self._start_time}&endtime={self._end_time}')
        data = response.json()
        new_features = []

        for feature in data['features']:
            filterd_features = {
                'magnitude': feature['properties']['mag'],
                'place': feature['properties']['place'],
                'time': feature['properties']['time'],
                'significant' : feature['properties']['sig'],
                'number_of_stations': feature['properties']['nst'],
                'distance_epicenter': feature['properties']['dmin'],
                'rms': feature['properties']['rms'],
                'type': feature['properties']['type'],
                'title': feature['properties']['title'],
                'id' : feature['id'],
                'coordinates': feature['geometry']['coordinates'],
                'url': feature['properties']['url']
            }
            new_features.append(filterd_features)
        
        with open(f"{self._save_raw_path}", "w") as f:
            json.dump(new_features, f, indent=4)

    def clean_data(self) -> None:
        with open(self._save_raw_path, 'r') as f:
            data = json.load(f)
        df = pd.DataFrame(data)

        df['longitude'] = df['coordinates'].apply(lambda x: x[0])
        df['latitude'] = df['coordinates'].apply(lambda x: x[1])
        df['depth'] = df['coordinates'].apply(lambda x: x[2])
        df['date-time'] = pd.to_datetime(df['time'], unit='ms')
        df['date-label'] = df['date-time'].dt.strftime('%d-%m-%Y %H:%M')
        df['region'] = df['place'].apply(lambda x: x.split(',')[-1].strip() if ',' in x else x)
        columns_to_keep = ['id', 'title', 'magnitude', 'date-time', 'date-label',
                           'latitude', 'longitude', 'depth', 'region']
        existing_columns = [col for col in columns_to_keep if col in df.columns]
        cleaned_df = df[existing_columns]
        cleaned_df.to_csv(self._save_clean_path, index=False)

     
