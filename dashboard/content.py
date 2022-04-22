
# content.py
import dash_bootstrap_components as dbc
from dash import dcc, html
from dashboard.index import app
from dashboard.layout.callbacks import documents, annotate

navbar = dbc.NavbarSimple(
    brand="Bellingcat Demo APP",
    brand_href="#",
    color="dark",
    dark=True,
    fluid=True,
)

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 62.5,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "height": "100%",
    "z-layout": 1,
    "overflow-x": "hidden",
    "transition": "all 0.5s",
    "padding": "0.5rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "transition": "margin-left .5s",
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

sidebar = html.Div(
    [
        html.H6("Menu", className="display-6"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("1-Intro", href="/1-intro", id="page-1-link"),
                dbc.NavLink("2-Training", href="/2-training", id="page-2-link"),
                dbc.NavLink("3-Documents", href="/3-documents", id="page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

content = html.Div(
    id="page-content",
    style=CONTENT_STYLE)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        navbar,
        sidebar,
        content,
    ],
)