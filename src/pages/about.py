import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/about', name="About")

COLORS = {
    "background": "#000000",
    "card_bg": "#1e1e1e",
    "text_primary": "#ffffff",
    "text_secondary": "#b0b0b0",
    "accent": "#119DFF"
}

def feature_card(title, description, icon_char):
    return dbc.Card([
        dbc.CardBody([
            html.H3(icon_char, className="mb-3", style={"color": COLORS["accent"]}),
            html.H5(title, className="card-title text-white"),
            html.P(description, className="card-text", style={"color": COLORS["text_secondary"]})
        ])
    ], className="h-100 border-0 shadow-sm", style={"backgroundColor": "#252525"})

layout = html.Div([
    dbc.Container([
        
        dbc.Row([
            dbc.Col([
                html.H1("About the Project", className="display-4 fw-bold mb-3"),
                html.P(
                    "Visualizing the pulse of our planet through data.", 
                    className="lead", 
                    style={"color": COLORS["accent"]}
                ),
                html.Hr(className="my-4", style={"borderColor": "#333"})
            ], width=12, className="text-center pt-5")
        ]),

        dbc.Row([
            dbc.Col([
                html.P(
                    "The Earthquake 3D Explorer is an interactive data visualization tool designed "
                    "to monitor and analyze global seismic activity. By combining real-time data "
                    "with high-resolution topography, this dashboard provides a unique perspective "
                    "on the geological events shaping our world.",
                    className="text-center fs-5",
                    style={"color": COLORS["text_secondary"], "maxWidth": "800px", "margin": "0 auto"}
                )
            ], width=12, className="mb-5")
        ]),

        dbc.Row([
            dbc.Col(feature_card(
                "Real-Time Data", 
                "Fetches the latest seismic events directly from the USGS API, ensuring up-to-date monitoring of global activity.",
                ""
            ), md=4, className="mb-4"),
            
            dbc.Col(feature_card(
                "3D Visualization", 
                "Utilizes the ETOPO1 Global Relief Model to map earthquakes on a realistic, interactive 3D sphere.",
                ""
            ), md=4, className="mb-4"),
            
            dbc.Col(feature_card(
                "Deep Analytics", 
                "Explore trends with interactive histograms, filtering events by magnitude, depth, and time ranges.",
                ""
            ), md=4, className="mb-4"),
        ], className="mb-5"),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Technical Stack & Credits", className="border-bottom-0 fw-bold text-white"),
                    dbc.CardBody([
                        html.Ul([
                            html.Li([html.Span("Framework: ", className="fw-bold text-white"), "Python, Dash & Plotly"]),
                            html.Li([html.Span("Data Source: ", className="fw-bold text-white"), "USGS Earthquake Hazards Program"]),
                            html.Li([html.Span("Topography: ", className="fw-bold text-white"), "NOAA ETOPO1 Global Relief Model"]),
                            html.Li([html.Span("Developer: ", className="fw-bold text-white"), "Yanis Amedjkane && Avishan Abdinzehad"]),
                        ], className="list-unstyled", style={"color": COLORS["text_secondary"]})
                    ])
                ], style={"backgroundColor": COLORS["card_bg"]}, className="border-0")
            ], width={"size": 8, "offset": 2})
        ]),

        dbc.Row([
            dbc.Col([
                html.A(
                    html.Button("View Source Code on GitHub", className="btn btn-outline-light mt-4"),
                    href="https://github.com/origanoinitalian/DataProject",
                    target="_blank"
                )
            ], className="text-center pb-5")
        ])

    ], fluid=True)
], style={"backgroundColor": COLORS["background"], "minHeight": "100vh"})
