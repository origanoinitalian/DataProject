import dash_bootstrap_components as dbc

def create_navbar():
    navbar = dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Global view", href="/global-view", active="exact")),
                dbc.NavItem(dbc.NavLink("Analytics", href="/", active="exact")),
                dbc.NavItem(dbc.NavLink("Explorer", href="/explorer", active="exact")),
                dbc.NavItem(dbc.NavLink("About", href="/about", active="exact")),
            ],
            brand="Earthquake tracker",
            brand_href="/",
            color="dark",#TODO: button to change from dark/light
            dark=True,
            className="mb-4" #just to put the margin down
        )
    return navbar
