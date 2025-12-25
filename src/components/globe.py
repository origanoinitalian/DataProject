from src.utils.etopo_manager import *
import plotly.graph_objs as go
from dash import dcc

def prepare_plot():
    RESOLUTION = 0.8
    LON_AREA = [-180., 180.]
    LAT_AREA = [-90., 90.]

    lon_topo, lat_topo, topo = etopo(LON_AREA, LAT_AREA, RESOLUTION)
    xs, ys, zs = mapping_to_sphere(lon_topo, lat_topo)
    Ctopo = [[0, 'rgb(0, 0, 70)'],[0.2, 'rgb(0,90,150)'], 
              [0.4, 'rgb(150,180,230)'], [0.5, 'rgb(210,230,250)'],
              [0.50001, 'rgb(0,120,0)'], [0.57, 'rgb(220,180,130)'], 
              [0.65, 'rgb(120,100,0)'], [0.75, 'rgb(80,70,0)'], 
              [0.9, 'rgb(200,200,200)'], [1.0, 'rgb(255,255,255)']]
    cmin = -8000
    cmax = 8000
    topo_sphere=dict(type='surface',
        x=xs,
        y=ys,
        z=zs,
        colorscale=Ctopo,
        surfacecolor=topo,
        showscale=False,
        cmin=cmin,
        cmax=cmax
    )
    noaxis=dict(showbackground=False,
        showgrid=False,
        showline=False,
        showticklabels=False,
        ticks='',
        title='',
        zeroline=False
    )

    return topo_sphere, noaxis

def sphere_component():
    title_color = 'white'
    bgcolor = 'black'
    topo_sphere, noaxis = prepare_plot()
    layout = go.Layout(
    autosize=True, 
    margin=dict(l=0, r=0, b=0, t=0),
    title=dict(
        text='3D spherical topography map',
        font=dict(family='Courier New', color=title_color),
        y=0.99
    ),
    showlegend = False,
    scene = dict(
    xaxis = noaxis,
    yaxis = noaxis,
    zaxis = noaxis,
    aspectmode='manual',
    aspectratio=go.layout.scene.Aspectratio(
      x=1, y=1, z=1)),
    paper_bgcolor = bgcolor,
    plot_bgcolor = bgcolor)
    plot_data = [topo_sphere]
    fig = go.Figure(data=plot_data, layout=layout)
    return dcc.Graph(
        id='earth-3d-globe',
        figure=fig,
        config={'displayModeBar': False},
        style={'height': '80vh'}
    )
