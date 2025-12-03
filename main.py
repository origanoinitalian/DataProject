from dash import Dash, dcc, html  
import plotly.express as px 
from src.utils.get_data import api_runner

year = 2002

gapminder = px.data.gapminder()
years = sorted(gapminder["year"].unique())
data_by_year = {y: gapminder.query("year == @y") for y in years}

app = Dash(__name__)

fig = px.scatter(
    data_by_year[year],
    x="gdpPercap",
    y="lifeExp",
    color="continent",
    size="pop",
    hover_name="country",
    size_max=60,
    log_x=True,
    labels={"gdpPercap": "GDP per capita", "lifeExp": "Life expectancy"},
    title=f"Life expectancy vs GDP per capita ({year})",
)

app.layout = html.Div(
    children=[
        html.H1(
            children=f"Life expectancy vs GDP per capita ({year})",
            style={"textAlign": "center", "color": "#7FDBFF"},
        ),
        dcc.Graph(id="graph1", figure=fig),
        html.Div(
            children=(
                "The graph above shows the relationship between life expectancy and GDP per capita "
                f"for year {year}. Each continent has its own color and point size is proportional "
                "to country population. Hover for details."
            )
        ),
    ]
)

if __name__ == "__main__":
    #app.run(debug=True)
    api_runner()

