import requests
import pathlib as Path
import json
import pandas as pd

def api_runner():

    response = requests.get('https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2024-01-01&endtime=2024-01-02')
    data = response.json()
    with open("earthquake_data.json", "w") as f:
        json.dump(data, f, indent=4)
    
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
            'id:' : feature['id'],
            'coordinates': feature['geometry']['coordinates']
            
        }
        new_features.append(filterd_features)
    
    new_json = {'earthquakes': new_features}
    with open("filtered_earthquake_data.json", "w") as f:
        json.dump(new_json, f, indent=4)
    
api_runner()


