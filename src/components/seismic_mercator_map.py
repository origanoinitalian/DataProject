import plotly.express as px
from dash import html

def render_seismic_map(df):
    base_layout = dict(
        mapbox_style="carto-darkmatter",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin={"r":0,"t":0,"l":0,"b":0},
        font=dict(color="white"),
        mapbox=dict(
            style="carto-darkmatter",
            center=dict(lat=0, lon=0),
            zoom=1,
            bounds={"west": -180, "east": 180, "south": -90, "north": 90}
        )
    )

    if df.empty:
        fig = px.scatter_mapbox()
        fig.update_layout(**base_layout)
        return fig

    if len(df) > 15000:
        df_map = df[df['magnitude'] >= 3.5]
    else:
        df_map = df

    fig = px.scatter_mapbox(
        df_map, 
        lat="latitude", 
        lon="longitude", 
        color="magnitude",
        size="magnitude",
        size_max=12,
        color_continuous_scale="Inferno", 
        hover_name="region", 
        hover_data={"latitude": False, "longitude": False, "depth": True, "date-label": True, "magnitude": True},
        height=600
    )
    
    fig.update_layout(**base_layout)
    
    fig.update_layout(
        uirevision='constant',
        coloraxis_colorbar=dict(
            title=dict(text="Mag", font=dict(color="white")),
            thickness=10, 
            len=0.5, 
            yanchor="top", y=0.95, xanchor="right", x=0.98,
            tickfont=dict(color="#b0b0b0")
        )
    )

    return fig
