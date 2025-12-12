import dash
from dash import Dash, html  
import dash_bootstrap_components as dbc
from src.utils.data_processor import manage_data
from src.utils.arg_parser import parse_arguments
from src.components.navbar import create_navbar


app = Dash(
        __name__,
        use_pages=True,
        pages_folder="src/pages",
        external_stylesheets=[dbc.themes.VAPOR, dbc.icons.BOOTSTRAP]
        )

app.layout = html.Div([
    create_navbar(),
    dbc.Container([
        dash.page_container
        ], fluid=True, className="p-4")#fluid true to take all the width
    ])

def main():
    args = parse_arguments()
    manage_data(
        should_fetch=args.fetch_data,
        start_time=args.start_time,
        end_time=args.end_time
    )
    app.run(debug=True)



if __name__ == "__main__":
    main()
    #api_runner()

