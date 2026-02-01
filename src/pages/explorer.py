import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from datetime import date, datetime, timedelta
from src.components.globe import get_etopo_trace, get_quakes_trace
from src.utils.data_processor import data_loader, DataProcessor

dash.register_page(__name__, path='/explorer', name="3D Explorer")

try:
    ETOPO_TRACE = get_etopo_trace()
except Exception as e:
    print(f"Error loading ETOPO data: {e}")
    ETOPO_TRACE = go.Surface() 

initial_layout = go.Layout(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, b=0, t=0),
    showlegend=False,
    uirevision='constant',
    scene=dict(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        aspectmode='manual',
        aspectratio=dict(x=1, y=1, z=1),
        camera=dict(
            eye=dict(x=1.6, y=1.6, z=1.6),
            center=dict(x=0, y=0, z=0)
        )
    )
)

def layout():
    """Defines the layout structure for the 3D Explorer page."""
    df_init = data_loader()

    if not df_init.empty:
        min_date = df_init['date-time'].min().date()
        max_date = datetime.now().date()
    else:
        min_date = date(2023, 1, 1)
        max_date = datetime.now().date()

    fig_init = go.Figure(data=[ETOPO_TRACE], layout=initial_layout)
    return html.Div([
        dbc.Container([
            html.Div([
                html.H2("3D earthquake explorer", className="text-white text-center d-inline-block me-3"),
                dbc.Badge(
                    "LIVE DATA", 
                    color="danger", 
                    className="p-2 animate__animated animate__pulse animate__infinite",
                    style={"verticalAlign": "top", "fontSize": "0.8rem"}
                )
            ], className="text-center pt-4 mb-4"),

            dcc.Interval(
                id='interval-component',
                interval=60*1000, 
                n_intervals=0
            ),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Label("Filter by Date Range:", className="text-white mb-2 me-3"),
                            dcc.DatePickerRange(
                                id='globe-date-picker',
                                min_date_allowed=min_date,
                                max_date_allowed=max_date,
                                start_date=min_date,
                                end_date=max_date,
                                display_format='DD/MM/YYYY',
                                style={'backgroundColor': '#1e1e1e', 'color': 'black'}
                            ),
                        ], className="d-flex justify-content-center align-items-center")
                    ], className="mb-4 shadow-sm border-0", style={"backgroundColor": "#2c2c2c"})
                ], width=8, className="offset-2")
            ]),

            dbc.Row([
                dbc.Col([
                    dcc.Loading(
                        id="loading-globe",
                        type="cube",
                        color="#119DFF",
                        children=[
                            dcc.Graph(
                                id='earth-3d-globe',
                                figure=fig_init,
                                style={'height': '80vh', 'width': '100%'},
                                config={'displayModeBar': False}
                            )
                        ]
                    )
                ], width=12, className="p-0")
            ])
        ], fluid=True)
    ], style={"backgroundColor": "black", "minHeight": "100vh", "overflow": "hidden"})


@callback(
    Output('earth-3d-globe', 'figure'),
    [Input('globe-date-picker', 'start_date'),
     Input('globe-date-picker', 'end_date'),
     Input('interval-component', 'n_intervals')]
)
def update_globe(start_date, end_date, n_intervals):
    """Callback to update the 3D globe with filtered historical and live data."""
    df_main = data_loader()
    
    selected_end = pd.to_datetime(end_date)
    today = datetime.now()
    
    if (today - selected_end).days < 2:
        df_live = DataProcessor.fetch_live_data()
        if not df_live.empty and not df_main.empty:
            df_combined = pd.concat([df_main, df_live])
            df = df_combined.drop_duplicates(subset='id', keep='last')
        elif not df_live.empty:
            df = df_live
        else:
            df = df_main
    else:
        df = df_main
    
    if df.empty:
        return go.Figure(data=[ETOPO_TRACE], layout=initial_layout)
    
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date) + timedelta(days=1)
    
    if df['date-time'].dt.tz is not None:
         df['date-time'] = df['date-time'].dt.tz_convert(None)

    mask = (df['date-time'] >= start) & (df['date-time'] <= end)
    df_filtered = df.loc[mask]
    quakes_trace = get_quakes_trace(df_filtered)

    return go.Figure(data=[ETOPO_TRACE, quakes_trace], layout=initial_layout)