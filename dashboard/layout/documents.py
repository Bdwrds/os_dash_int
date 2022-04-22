"""
author: Ben E
date: 2022-10-22
"""
from dash import dcc, html
from dash.dependencies import Input, Output, State
from app import app
import datetime

tab_documents = html.Div(children=[
    html.H2('Demo APP Exploring OSINT'),
    html.Br(),
    dcc.Upload(
            id='upload-image',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files')
            ]),
            style={
                'width': '40%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            # Allow multiple files to be uploaded
            multiple=True
        ),
    html.Div(id='output-image-upload'),
    html.Label('Dropdown'),
    dcc.Dropdown(['New York City', 'Montréal', 'San Francisco'], 'Montréal',style={
                'width': '40%'}),\
], style={'padding': 10, 'flex': 1})
