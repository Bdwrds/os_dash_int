"""
author: Ben E
date: 2022-04-22
"""
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
