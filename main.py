from dash import Dash, dcc, html  
import plotly.express as px 
import dash_ag_grid as dag
from src.utils.get_data import DataProcessor
from src.utils.to_datetime import to_datetime
import pandas as pd

app = Dash()

dataprocessor = DataProcessor('2024-01-01', '2024-01-02', 'data/raw/raw_earthquakes.json', 'data/cleaned/cleaned_earthquakes.csv')

def main():
    df = pd.read_json('data/cleaned/filtered_earthquake_data.json')
    app.layout = [html.Div(children="Hello World"),
                  dag.AgGrid(
                      rowData=df.to_dict('records'),
                      columnDefs=[{"field": i} for i in df.columns]
                      )
                  ]
    app.run(debug=True)

if __name__ == "__main__":
    dataprocessor.fetch_data()
    dataprocessor.clean_data()
    #main()
    #api_runner()

