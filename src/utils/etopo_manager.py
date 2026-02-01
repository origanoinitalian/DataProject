from dash.html import A
import numpy as np
from netCDF4 import Dataset
import os
from pathlib import Path

#credit to Ryota Kiuchi, Ph.D. for the excellent tutorial
def etopo(lon_area, lat_area, resolution):
    """
    Reads ETOPO1 topography data from a NetCDF file.
    
    Returns:
        tuple: (longitude grid, latitude grid, topography data)
    """
    current_dir = Path(__file__).resolve().parent
    root_dir = current_dir.parent.parent
    new_path = os.path.join(root_dir, "data", "cleaned", "ETOPO1_Ice_g_gdal.grd")
    data = Dataset(new_path, 'r')

    lon_range = data.variables['x_range'][:]
    lat_range = data.variables['y_range'][:]
    topo_range = data.variables['z_range'][:]
    spacing = data.variables['spacing'][:]
    dimension = data.variables['dimension'][:]
    z = data.variables['z'][:]
    lon_num = dimension[0]
    lat_num = dimension[1]

    lon_input = np.zeros(lon_num); lat_input = np.zeros(lat_num)
    for i in range(lon_num):
        lon_input[i] = lon_range[0] + i * spacing[0]
    for i in range(lat_num):
        lat_input[i] = lat_range[0] + i * spacing[1]
    lon, lat = np.meshgrid(lon_input, lat_input)
    topo = np.reshape(z, (lat_num, lon_num))
    if ((resolution < spacing[0]) | (resolution < spacing[1])):
        print('Set the highest resolution')
    else:
        skip = int(resolution/spacing[0])
        lon = lon[::skip,::skip]
        lat = lat[::skip,::skip]
        topo = topo[::skip,::skip]
    topo = topo[::-1]
  
    range1 = np.where((lon>=lon_area[0]) & (lon<=lon_area[1]))
    lon = lon[range1]; lat = lat[range1]; topo = topo[range1]
    range2 = np.where((lat>=lat_area[0]) & (lat<=lat_area[1]))
    lon = lon[range2]; lat = lat[range2]; topo = topo[range2]
  
    lon_num = len(np.unique(lon))
    lat_num = len(np.unique(lat))
    lon = np.reshape(lon, (lat_num, lon_num))
    lat = np.reshape(lat, (lat_num, lon_num))
    topo = np.reshape(topo, (lat_num, lon_num))
  
    return lon, lat, topo

def degree_to_radians(degree):
    return degree * np.pi/180

def mapping_to_sphere(lon ,lat, radius=1):
    """Maps 2D longitude/latitude coordinates to 3D Cartesian coordinates."""
    lon=np.array(lon, dtype=np.float64)
    lat=np.array(lat, dtype=np.float64)
    lon=degree_to_radians(lon)
    lat=degree_to_radians(lat)
    xs=radius*np.cos(lon)*np.cos(lat)
    ys=radius*np.sin(lon)*np.cos(lat)
    zs=radius*np.sin(lat)
    return xs, ys, zs