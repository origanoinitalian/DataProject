import dash_ag_grid as dag

GRID_STYLE = {
    "--ag-header-foreground-color": "#b0b0b0",
    "--ag-header-background-color": "#141414",
    "--ag-background-color": "#0a0a0a",
    "--ag-foreground-color": "#ffffff",
    "--ag-row-hover-color": "#222222",
    "--ag-odd-row-background-color": "#0f0f0f",
    "--ag-borders": "none",
    "--ag-border-color": "rgba(0,0,0,0)",
    "fontFamily": "Roboto, sans-serif"
}

def render_seismic_grid(df):
    if df.empty:
        return []

    columnDefs = [
        {"field": "date-label", "headerName": "DATE", "sortable": True, "filter": True, "width": 160},
        {"field": "region", "headerName": "LOCATION", "sortable": True, "filter": True, "flex": 1},
        {
            "field": "magnitude", 
            "headerName": "MAG", 
            "sortable": True, 
            "filter": "agNumberColumnFilter", 
            "width": 100,
            "cellStyle": {"styleConditions": [
                {"condition": "params.value >= 6", "style": {"color": "#ff4136", "fontWeight": "bold"}},
                {"condition": "params.value >= 4", "style": {"color": "#ff851b"}},
                {"condition": "params.value < 4", "style": {"color": "#aaaaaa"}},
            ]}
        },
        {"field": "depth", "headerName": "DEPTH (km)", "sortable": True, "filter": "agNumberColumnFilter", "width": 130},
    ]

    df_table = df.sort_values(by="date-time", ascending=False).head(1000)

    grid = dag.AgGrid(
        id="seismic-grid",
        rowData=df_table.to_dict("records"),
        columnDefs=columnDefs,
        defaultColDef={"resizable": True, "sortable": True, "filter": True},
        columnSize="sizeToFit",
        dashGridOptions={"pagination": True, "paginationPageSize": 15, "rowSelection": "single"},
        className="ag-theme-alpine-dark",
        style={"height": "600px", "width": "100%", **GRID_STYLE}
    )

    return grid
