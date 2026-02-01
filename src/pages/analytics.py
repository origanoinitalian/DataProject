import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date, datetime
from src.utils.data_processor import data_loader
from src.components.histogram import render_histogram
from src.components.analytics_charts import (
    render_kpi_cards, 
    render_scatter_depth_mag, 
    render_top_regions
)

dash.register_page(__name__, path='/', name="Analysis")

def layout():
    """Constructs the dashboard layout for the Analytics page."""
    min_date = date(2000, 1, 1)
    max_date = datetime.now().date()
    start_default = date(2023, 1, 1)

    return html.Div([
        dbc.Container([
            html.H2("Seismic analytics", className="mb-4 text-white"),
            
            dbc.Card([
                dbc.CardBody([
                    html.Label("Select analysis period:", className="text-white mb-2"),
                    dcc.DatePickerRange(
                        id='date-range-picker',
                        min_date_allowed=min_date,
                        max_date_allowed=max_date,
                        start_date=start_default,
                        end_date=max_date,
                        display_format='DD/MM/YYYY',
                        style={'backgroundColor': '#1e1e1e', 'color': 'black'}
                    ),
                ])
            ], className="mb-4 shadow-sm border-0", style={"backgroundColor": "#2c2c2c"}),

            dbc.Row(id='kpi-row', className="mb-4"),

            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(dcc.Loading(dcc.Graph(id='dynamic-histogram', config={"displayModeBar": False}), color="#119DFF")),
                        className="shadow-lg border-0 h-100", style={"backgroundColor": "#1e1e1e"}
                    ), md=6, className="mb-4"
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(dcc.Loading(dcc.Graph(id='scatter-depth', config={"displayModeBar": False}), color="#119DFF")),
                        className="shadow-lg border-0 h-100", style={"backgroundColor": "#1e1e1e"}
                    ), md=6, className="mb-4"
                )
            ]),

            dbc.Row([
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(dcc.Loading(dcc.Graph(id='bar-regions', config={"displayModeBar": False}), color="#119DFF")),
                        className="shadow-lg border-0", style={"backgroundColor": "#1e1e1e"}
                    ), width=12
                )
            ])

        ], fluid=True)
    ])


@callback(
    [Output('kpi-row', 'children'),
     Output('dynamic-histogram', 'figure'),
     Output('scatter-depth', 'figure'),
     Output('bar-regions', 'figure')],
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_analytics(start_date, end_date):
    """Updates all analytic charts and KPIs based on the selected date range."""
    df = data_loader()

    if df.empty:
        return render_kpi_cards(df), {}, {}, {}

    mask = (df['date-time'] >= pd.to_datetime(start_date)) & \
           (df['date-time'] <= pd.to_datetime(end_date))
    df_filtered = df.loc[mask]

    kpis = render_kpi_cards(df_filtered)
    hist_fig = render_histogram(df_filtered)
    scatter_fig = render_scatter_depth_mag(df_filtered)
    bar_fig = render_top_regions(df_filtered)

    return kpis, hist_fig, scatter_fig, bar_fig