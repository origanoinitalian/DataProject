import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html

DARK_GRAPH_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white'),
    margin=dict(l=40, r=20, t=40, b=40),
    xaxis=dict(gridcolor='#444'),
    yaxis=dict(gridcolor='#444')
)

def render_kpi_cards(df):
    if df.empty:
        count, max_mag, avg_depth = 0, 0, 0
    else:
        count = len(df)
        max_mag = df['magnitude'].max()
        avg_depth = df['depth'].mean()

    def create_card(title, value, icon, color):
        return dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4(icon, className="mb-2", style={"color": color}),
                    html.H6(title, className="text-white-50"),
                    html.H3(f"{value}", className="text-white fw-bold")
                ])
            ], className="shadow-sm border-0 h-100", style={"backgroundColor": "#1e1e1e"}),
            md=4, className="mb-3"
        )

    return [
        create_card("Total Events", f"{count:,}", "", "#119DFF"),
        create_card("Max Magnitude", f"{max_mag:.1f}", "", "#FF4136"),
        create_card("Avg Depth", f"{avg_depth:.1f} km", "", "#2ECC40"),
    ]

def render_scatter_depth_mag(df):
    """Scatter Plot: Profondeur vs Magnitude"""
    if df.empty: return {}
    
    fig = px.scatter(
        df, x="depth", y="magnitude", color="magnitude",
        color_continuous_scale="Turbo",
        title="Magnitude vs Depth",
        labels={"depth": "Depth (km)", "magnitude": "Magnitude"}
    )
    fig.update_layout(**DARK_GRAPH_LAYOUT)
    fig.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=0)))
    return fig

def render_top_regions(df):
    if df.empty:
        return {}

    top_regions = df['region'].value_counts().nlargest(10).reset_index()
    top_regions.columns = ['region', 'count']

    fig = px.bar(
        top_regions, x="count", y="region", orientation='h',
        title="Top 10 Active Regions",
        color="count", color_continuous_scale="Viridis"
    )
    fig.update_layout(**DARK_GRAPH_LAYOUT)
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig
