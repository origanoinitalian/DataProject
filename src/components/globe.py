import plotly.graph_objs as go
import numpy as np
from src.utils.etopo_manager import etopo

def mapping_to_sphere(lon, lat, radius=1):
    lon = np.array(lon, dtype=np.float64)
    lat = np.array(lat, dtype=np.float64)
    lon_rad = np.radians(lon)
    lat_rad = np.radians(lat)
    xs = radius * np.cos(lon_rad) * np.cos(lat_rad)
    ys = radius * np.sin(lon_rad) * np.cos(lat_rad)
    zs = radius * np.sin(lat_rad)
    return xs, ys, zs

def get_etopo_trace():
    RESOLUTION = 0.8
    lon_topo, lat_topo, topo = etopo([-180., 180.], [-90., 90.], RESOLUTION)
    xs, ys, zs = mapping_to_sphere(lon_topo, lat_topo)
    Ctopo = [
        [0, 'rgb(0, 0, 70)'], [0.2, 'rgb(0, 90, 150)'], 
        [0.4, 'rgb(150, 180, 230)'], [0.5, 'rgb(210, 230, 250)'],
        [0.50001, 'rgb(0, 120, 0)'], [0.57, 'rgb(220, 180, 130)'], 
        [0.65, 'rgb(120, 100, 0)'], [0.75, 'rgb(80, 70, 0)'], 
        [0.9, 'rgb(200, 200, 200)'], [1.0, 'rgb(255, 255, 255)']
    ]
    return go.Surface(
        x=xs, y=ys, z=zs,
        surfacecolor=topo,
        colorscale=Ctopo,
        cmin=-8000,
        cmax=8000,
        showscale=False,
        hoverinfo='skip'
    )

def get_quakes_trace(df):
    if df.empty:
        return go.Scatter3d()

    evlon = df['longitude'].values
    evlat = df['latitude'].values
    evDepth = df['depth'].values
    evMag = df['magnitude'].values
    xs_org, ys_org, zs_org = mapping_to_sphere(evlon, evlat)
    ratio = 1.15 - (evDepth * 2e-4)
    xs_ev = xs_org * ratio
    ys_ev = ys_org * ratio
    zs_ev = zs_org * ratio

    return go.Scatter3d(
        x=xs_ev,
        y=ys_ev,
        z=zs_ev,
        mode='markers',
        name='Earthquakes',
        marker=dict(
            size=1.0 * evMag,
            color=evDepth,
            colorscale='Jet',  
            reversescale=True,
            opacity=1.0,
            cmin=0,
            cmax=700,
            showscale=True,
            colorbar=dict(
                title=dict(
                    text='Source Depth',
                    font=dict(color='white', family='Courier New')
                ),
                tickfont=dict(color='white', family='Courier New'),
                x=0.9,
                thickness=20
            )
        ),
        text=[f"Mag: {m}<br>Depth: {d}km<br>{place}" 
              for m, d, place in zip(evMag, evDepth, df['region'])],
        hoverinfo='text'
    )
