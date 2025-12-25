import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import date
from src.utils.data_processor import data_loader
from src.components.histogram import render_histogram

dash.register_page(__name__, path='/analytics', name="Analyses")

df_init = data_loader()
if not df_init.empty:
    min_date = df_init['date-time'].min().date()
    max_date = df_init['date-time'].max().date()
else:
    min_date = date(2023, 1, 1)
    max_date = date(2024, 1, 1)

layout = html.Div([
    dbc.Container([
        html.H2("Analytics", className="mb-4 text-white"),
        dbc.Card([
            dbc.CardBody([
                html.Label("Select a period:", className="text-white mb-2"),
                dcc.DatePickerRange(
                    id='date-range-picker',
                    min_date_allowed=min_date,
                    max_date_allowed=max_date,
                    start_date=min_date, 
                    end_date=max_date,
                    display_format='DD/MM/YYYY',
                    style={'backgroundColor': '#1e1e1e', 'color': 'black'}
                ),
            ])
        ], className="mb-4 shadow-sm border-0", style={"backgroundColor": "#2c2c2c"}),
        dbc.Row([
            dbc.Col(
                dbc.Card(
                    dbc.CardBody([
                        dcc.Graph(id='dynamic-histogram', config={"displayModeBar": False})
                    ]),
                    className="shadow-lg border-0",
                    style={"backgroundColor": "#1e1e1e"}
                ),
                width=12
            )
        ])
    ], fluid=True)
])

@callback(
    Output('dynamic-histogram', 'figure'),
    [Input('date-range-picker', 'start_date'),
     Input('date-range-picker', 'end_date')]
)
def update_histogram(start_date, end_date):
    df = data_loader()

    if df.empty:
        return render_histogram(df) 

    mask = (df['date-time'] >= pd.to_datetime(start_date)) & \
           (df['date-time'] <= pd.to_datetime(end_date))
    df_filtered = df.loc[mask]
    return render_histogram(df_filtered)
