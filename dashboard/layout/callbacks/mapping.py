import dash
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dcc, html
import dash_leaflet.express as dlx
from dash.exceptions import PreventUpdate
from dashboard.index import app
from func import haversine
import overpy
import json
import numpy as np
from sklearn.metrics import DistanceMetric

api = overpy.Overpass()

@app.callback(Output("log", "children"), Input("map", "bounds"))
def log_bounds(bounds):
    return json.dumps(bounds)

@app.callback(
    Output('submit-output', 'children'),
    [Input("sub-button", "n_clicks")],
    [State("node-key-1", "value"), State("node-value-1", "value"),
    State("node-key-2", "value"), State("node-value-2", "value"),
    State("input-max-dist-1-2", "value"),
    State("map", "bounds")]
)
def print_output(n_clicks, key_1, value_1, key_2, value_2, max_d, bbox):
    if max_d is None:
        raise PreventUpdate
    elif n_clicks > 0:
        return(build_query(key_1, value_1, key_2, value_2, max_d, bbox))


@app.callback([Output('geojson', 'data')],
    [Input("sub-button-2", "n_clicks"),
    State("input-max-dist-1-2", "value")]
)
def print_output(n_clicks, max_d):
    if max_d is None:
        PreventUpdate
    elif n_clicks>0:
        df1 = pd.read_csv('feature_1.csv', index_col=0)
        df2 = pd.read_csv('feature_2.csv', index_col=0)
        df1[['lat_rad', 'lon_rad']] = (np.radians(df1.loc[:, ['lat', 'lon']]))
        df2[['lat_rad', 'lon_rad']] = (np.radians(df2.loc[:, ['lat', 'lon']]))
        df1.rename(columns={"id": "f1"}, inplace=True)
        df2.rename(columns={"id": "f2"}, inplace=True)
        dist = DistanceMetric.get_metric('haversine')
        dist_matrix = (dist.pairwise(df1[['lat_rad', 'lon_rad']], df2[['lat_rad', 'lon_rad']])*3959)
        df_dist = pd.DataFrame(dist_matrix, index=df1['f1'], columns=df2['f2'])
        df_dist_m = pd.melt(df_dist.reset_index(), id_vars='f1')
        df_dist_m.columns = ['f1', 'f2', 'km']
        f1_items = df_dist_m.loc[df_dist_m.km < max_d, ].f1.unique()
        f2_items = df_dist_m.loc[df_dist_m.km < max_d, ].f2.unique()
        df1_items = df1.loc[df1.f1.isin(f1_items), ['name','lat', 'lon']]
        df2_items = df2.loc[df2.f2.isin(f2_items), ['name','lat', 'lon']]
        df_dict = pd.concat([df1_items, df2_items]).to_dict('records')
        geojson = dlx.dicts_to_geojson([{**mkr, **dict(tooltip=mkr['name'])} for mkr in df_dict])
        return [geojson]


@app.callback(Output('node-value-1', 'options'), Input('node-key-1', 'value'))
def dropdown_options(value):
    return feature_dropdown_options(value)

@app.callback(Output('node-value-2', 'options'), Input('node-key-2', 'value'))
def dropdown_options(value):
    return feature_dropdown_options(value)

def feature_dropdown_options(value):
    if value == "amenity":
        return ['place_of_worship', 'pub', 'restaurant', 'university', 'school', 'fuel', 'atm', 'police']
    elif value == "railway":
        return ['station', 'level_crossing', 'disused', 'subway', 'tram']
    elif value == "military":
        return ['airfield', 'checkpoint', 'bunker', 'checkpoint', 'training_area', 'danger_area', 'bunker']
    elif value == "man_made":
        return ['communications_tower', 'crane', 'lighthouse', 'windmill', 'water_tap', 'water_well', 'telescope']
    else:
        return None

def build_query(key_1, value_1, key_2, value_2, max_d, bbox):
    if max_d is None:
        raise PreventUpdate
    lat1, lon1 = bbox[0]
    lat2, lon2 = bbox[1]
    # fetch all ways and nodes
    api_query1 = f"node[{key_1}={value_1}] ({lat1},{lon1},{lat2},{lon2});out;"
    api_query2 = f"node[{key_2}={value_2}] ({lat1},{lon1},{lat2},{lon2});out;"
    result1 = api.query(api_query1)
    print(f"q1: {api_query1}")
    result2 = api.query(api_query2)
    print(f"q2: {api_query2}")

    ids = ["id", "lat", "lon", "name"]
    tmp_dc = list()
    for node in result1.nodes:
        tmp_dc.append([node.id, float(node.lat), float(node.lon), node.tags.get('name')])
    pd.DataFrame(tmp_dc, columns=ids).to_csv('feature_1.csv')

    tmp_dc = list()
    for node in result2.nodes:
        tmp_dc.append([node.id, float(node.lat), float(node.lon), node.tags.get('name')])
    pd.DataFrame(tmp_dc, columns=ids).to_csv('feature_2.csv')

    return f"{key_1}:{str(len(result1.nodes))} - {key_2}:{str(len(result2.nodes))}"
