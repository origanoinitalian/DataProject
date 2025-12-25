import dash
from dash import html
import dash_bootstrap_components as dbc
from src.components.globe import sphere_component

dash.register_page(__name__, path='/explorer', name="Explorer 3D")

layout = html.Div([
    dbc.Container([
        html.H1("3D mapping of global earthquakes", className="text-center text-white mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Spinner(
                    sphere_component(),
                    color="primary",
                    type="grow",
                    fullscreen=True, 
                )
            ], width=12)
        ])
    ], fluid=True)
], style={"backgroundColor": "black", "minHeight": "100vh"})
