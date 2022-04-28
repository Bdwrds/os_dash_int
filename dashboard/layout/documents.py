"""
author: Ben E
date: 2022-10-22
"""
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
import datetime

tab_upload_documents = html.Div(children=[
    html.H4('Uploading new images'),
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
    ],
    style={'padding': 10, 'flex': 1})

tab_save_documents = html.Div(children=[
    html.Div(id='output-image-upload'),
    html.Label('Uploaded Image'),
    html.Br(),
    dcc.Input(
            id="image_name",
            type="text",
            placeholder="Enter image name",
        ),
    html.Button('Submit', id='textarea-state-example-button', n_clicks=0),
    ], style={'padding': 10, 'flex': 1})


tab_documents = dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(tab_upload_documents, md=5),
                        dbc.Col(tab_save_documents, md=7),
                    ],
                ),
            ],
            fluid=True,
        )
