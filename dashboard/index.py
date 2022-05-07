"""
author: Ben E
date: 2022-04-22
"""
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import dash_auth
import os

CREDENTIAL_UN = os.environ.get('CREDENTIAL_UN')
CREDENTIAL_PW = os.environ.get('CREDENTIAL_PW')

# create dash app with basic auth
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
auth = dash_auth.BasicAuth(app, {CREDENTIAL_UN: CREDENTIAL_PW})