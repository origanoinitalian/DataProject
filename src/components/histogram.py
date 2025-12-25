import plotly.express as px
import pandas as pd
from dash import dcc

def empty_histogram():
    return dcc.Graph(
        figure={
            "layout": {
                "xaxis": {"visible": False},
                "yaxis": {"visible": False},
                "annotations": [{
                    "text": "No data on this period",
                    "xref": "paper", "yref": "paper",
                    "showarrow": False,
                    "font": {"size": 20, "color": "white"}
                }],
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)"
            }
        },
        config={"displayModeBar": False}
    )

def render_histogram(df: pd.DataFrame):
    if df.empty:
        return empty_histogram()

    df_histo = df.copy()
    #we categorize by depth, a seisme occuring
    # between 0 and 70km is superficial (dangerous)
    # 70 and 300km is intermediate
    # and >300km is deep enough to be considered not dangerous

    bins = [0, 70, 300, 1000] 
    labels = ["Superficial (<70km)", "Intermediate (70-300km)", "Deep (>300km)"]
    df_histo['Depth class'] = pd.cut(df_histo['depth'], bins=bins, labels=labels)

    histo = px.histogram(
        df_histo,
        x="magnitude",
        color="Depth class",
        nbins=20,
        marginal=None,
        hover_data=None,
        color_discrete_map={
            "Superficial (<70km)": "#ff5e57",
            "Intermediate (70-300km)": "#ffa801",
            "Deep (>300km)": "#575fcf"
        },
        template="plotly_dark"
    )
    histo.update_layout(
            title={
                'text': "Magnitude distribution",
                'y':0.99, 'x':0.5,
                'xanchor': 'center',
                'yanchor': 'top'
                },
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            xaxis_title="Richter magnitude",
            yaxis_title="Number of earthquakes",
            bargap=0.1,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
        )
    )
    histo.update_traces(
        selector=dict(type='histogram'),
        hovertemplate="Magnitude: <b>%{x}</b><br>Number: <b>%{y}</b><extra></extra>"
    )
    histo.update_traces(
        selector=dict(type='box'),
        hoverinfo='skip'
    )
    return histo
