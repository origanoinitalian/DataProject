import dash
from dash import Dash, html  
import dash_bootstrap_components as dbc
from src.utils.data_processor import manage_data
from src.utils.arg_parser import parse_arguments
from src.components.navbar import create_navbar

from src.components.visualizations import create_magnitude_distribution_hist

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



    try:
        df = pd.read_csv('data/cleaned/cleaned_earthquakes.csv')

    except FileNotFoundError:
        print("Cleaned data file not found. Run with 'python3 main.py --fetch-data'.")
        return

    app.layout = html.Div([
        html.H1("Earthquake Dashboard"),
    
        create_magnitude_distribution_hist(df)
    ])

    app.run(debug=True)

if __name__ == "__main__":
    main()
    #api_runner()

