"""
author: Ben E
date: 2022-10-22
"""
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
import dash_leaflet as dl



tab_map = html.Div(children=[
    html.H4('Mapping Section'),
    html.Br(),
    dl.Map(
        [dl.TileLayer(), dl.GeoJSON(id="geojson", data=None)], style={'width': '100%', 'height': '500px'}, zoom=10,
        center=(51.455638052568475, -2.48042),
        id='map'
    ),
    html.Div(id="log")],
    style={'padding': 10, 'flex': 1})


OSM_KEY_LS = ['amenity', 'railway', 'military', 'man_made']


tab_save_documents = html.Div(children=[
    html.Div(className='six columns', children=[
        html.Label('Feature 1'),
        dcc.Dropdown(OSM_KEY_LS, OSM_KEY_LS[0], id='node-key-1'),
        dcc.Dropdown(id='node-value-1'),
        html.Br(),
        html.Label('Max Distance (km)'),
        dcc.Input(id='input-max-dist-1-2', type='number'),
        html.Br(),
        html.Button('Submit Query', id='sub-button', n_clicks=0),
        html.Br(),
        html.Label('Output Summary:'),
        html.Br(),
        html.Br(),
        dcc.Loading(
            id="loading-1",
            type="default",
            children=[
                html.Div(id='submit-output')
            ]),
        html.Br(),
        html.Button('Update Map', id='sub-button-2', n_clicks=0),
        dbc.Table.from_dataframe(id='print-output', df=pd.DataFrame()),
        ], style={'padding': 5, 'flex': 1}),
    html.Div(className='six columns', children=[
        html.Label('Feature 2'),
        dcc.Dropdown(OSM_KEY_LS, OSM_KEY_LS[0],  id='node-key-2'),
        dcc.Dropdown(id='node-value-2'),
        ], style={'padding': 5, 'flex': 1}),
    ], style=dict(display='flex'))


tab_mapping = dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(tab_map, md=8),
                        dbc.Col(tab_save_documents, md=4),
                    ],
                ),
            ],
            fluid=True,
        )
