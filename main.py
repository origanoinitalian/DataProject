from dash import Dash, dcc, html  
import plotly.express as px 
import dash_ag_grid as dag
from src.utils.data_processor import DataProcessor, manage_data
from src.utils.arg_parser import parse_arguments
import pandas as pd

app = Dash(__name__)

def main():
    args = parse_arguments()
    manage_data(
        should_fetch=args.fetch_data,
        start_time=args.start_time,
        end_time=args.end_time
    )

if __name__ == "__main__":

    main()
    #api_runner()

