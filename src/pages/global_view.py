import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, datetime, timedelta

from src.utils.data_processor import data_loader
from src.components.seismic_mercator_map import render_seismic_map
from src.components.seismic_grid import render_seismic_grid

dash.register_page(__name__, path='/global-view', name="Global View")

def layout():
    """Generates the layout for the 2D Global View (Map + Data Grid)."""
    min_date = date(2000, 1, 1)
    max_date = datetime.now().date()
    start_default = (datetime.now() - timedelta(days=30)).date()

    return html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.H2("Global seismic activity", className="text-white fw-bold mb-0", style={'letterSpacing': '-1px'}),
                    html.P("Interactive mercator map", className="text-muted small"),
                ], md=6),
                dbc.Col([
                    dcc.DatePickerRange(
                        id='view-date-picker',
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        start_date=start_default,
                        end_date=max_date,
                        display_format='DD/MM/YYYY',
                        style={'backgroundColor': '#0a0a0a', 'color': 'white', 'border': '1px solid #333', 'float': 'right'}
                    ),
                ], md=6, className="d-flex align-items-center justify-content-end")
            ], className="py-4 align-items-center"),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody(
                            dcc.Loading(
                                dcc.Graph(
                                    id='map-2d', 
                                    style={"height": "65vh"},
                                    config={"displayModeBar": False, "scrollZoom": True}
                                ),
                                color="#d64541"
                            ), 
                            className="p-0"
                        )
                    ], className="shadow-lg border-0 mb-4", style={"borderRadius": "12px", "overflow": "hidden"})
                ], width=12)
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Detailed Event Log", className="bg-transparent border-0 text-white fw-bold pt-4 px-4"),
                        dbc.CardBody(
                            dcc.Loading(
                                html.Div(id="table-container"),
                                color="#d64541"
                            ),
                            className="p-0"
                        )
                    ], className="shadow-lg border-0 mb-5", style={"backgroundColor": "#0a0a0a", "borderRadius": "12px"})
                ], width=12)
            ])

        ], fluid=True, className="px-4")
    ])


@callback(
    [Output('map-2d', 'figure'),
     Output('table-container', 'children')],
    [Input('view-date-picker', 'start_date'),
     Input('view-date-picker', 'end_date')]
)
def update_view(start_date, end_date):
    """Updates the 2D map and data grid based on selected dates."""
    df = data_loader()
    
    if df.empty:
        return render_seismic_map(pd.DataFrame()), html.Div("No data available", className="text-white p-4 text-center")
    mask = (df['date-time'] >= pd.to_datetime(start_date)) & \
           (df['date-time'] <= pd.to_datetime(end_date))
    df_filtered = df.loc[mask].copy()
    fig =render_seismic_map(df_filtered)
    grid = render_seismic_grid(df_filtered)

    return fig, grid