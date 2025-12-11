import pandas as pd
import numpy as np
import plotly.graph_objs as go
from dash import dcc

def create_magnitude_distribution_hist(df: pd.DataFrame) -> dcc.Graph:
    
    bins = np.arange(-1, 10.5, 0.5)
    counts, bin_edges = np.histogram(df['magnitude'], bins=bins)

    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])            #slicing

    fig = go.Figure(data = [
        go.Bar(
            x=bin_centers,
            y=counts,
            marker_color='indianred',
            opacity=0.8)
    ])

    fig.update_layout(
        title='Earthquake Magnitude Distribution',
        xaxis_title='Magnitude',
        yaxis_title='Count: Number of Earthquakes',
        bargap=0.1
    )

    return dcc.Graph(id='simple-mag-hist', figure=fig)