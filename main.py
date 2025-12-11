from dash import Dash, dcc, html  
import plotly.express as px 
import dash_ag_grid as dag
from src.utils.data_processor import DataProcessor, manage_data
from src.utils.arg_parser import parse_arguments
import pandas as pd
from src.components.visualizations import create_magnitude_distribution_hist

app = Dash(__name__)

def main():
    args = parse_arguments()
    manage_data(
        should_fetch=args.fetch_data,
        start_time=args.start_time,
        end_time=args.end_time
    )

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

