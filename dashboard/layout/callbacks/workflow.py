
from dash.dependencies import Input, Output, State
from dash import dcc, html
import plotly.express as px
from skimage import io
from dash.exceptions import PreventUpdate
import dash_leaflet.express as dlx
import overpy
import json
import numpy as np
import pandas as pd
from sklearn.metrics import DistanceMetric
import datetime
from dashboard.index import app
import os
import base64

UPLOAD_DIR = "images"
DATA_DIR = "data"

api = overpy.Overpass()

@app.callback(Output('feature-value-1', 'options'), Input('feature-key-1', 'value'))
def dropdown_options(value):
    return feature_dropdown_options(value)

@app.callback(Output('feature-value-2', 'options'), Input('feature-key-2', 'value'))
def dropdown_options(value):
    return feature_dropdown_options(value)

@app.callback(Output('feature-value-3', 'options'), Input('feature-key-3', 'value'))
def dropdown_options(value):
    return feature_dropdown_options(value)

def feature_dropdown_options(value):
    if value == "amenity":
        return ['place_of_worship', 'pub', 'restaurant', 'university', 'school', 'fuel', 'atm', 'police', 'hospital', 'library']
    elif value == "railway":
        return ['station', 'level_crossing', 'disused', 'subway', 'tram']
    elif value == "military":
        return ['airfield', 'checkpoint', 'bunker', 'checkpoint', 'training_area', 'danger_area', 'bunker']
    elif value == "man_made":
        return ['communications_tower', 'crane', 'lighthouse', 'windmill', 'water_tap', 'water_well', 'telescope']
    elif value == 'shop':
        return ['supermarket', 'bakery', 'bicycle', 'pet', 'chemist']
    elif value == ['tourism']:
        return ['museum', 'hotel', 'attraction']
    else:
        return [None]


@app.callback(Output("log", "children"), Input("map", "bounds"))
def log_bounds(bounds):
    return json.dumps(bounds)


@app.callback(
    Output('submit-output', 'children'),
    [Input("sub-button-1", "n_clicks")],
    [State("feature-key-1", "value"), State("feature-value-1", "value"),
    State("feature-key-2", "value"), State("feature-value-2", "value"),
    State("feature-key-3", "value"), State("feature-value-3", "value"),
    State("map", "bounds")]
)
def print_output(n_clicks, key_1, value_1, key_2, value_2, key_3, value_3, bbox):
    if n_clicks is None:
        print("prevent print_output")
        raise PreventUpdate
    elif n_clicks > 0:
        return([build_query(key_1, value_1, key_2, value_2, key_3, value_3, bbox)])


@app.callback(Output('confirm-danger', 'displayed'),
              Input("sub-button-2", "n_clicks"),
              State("input-max-dist", "value"))
def display_confirm(clicks, max_d):
    if clicks > 0:
        if max_d is None:
            return True
        return False
    raise PreventUpdate


@app.callback(
    [Output('geojson', 'data')],
    [Input("sub-button-2", "n_clicks"),
     State("input-max-dist", "value"),
     State("feature-value-3", "value")]
)
def find_overlap(n_clicks, max_d, value_3):
    if max_d is None:
        print("prevent find_overlap")
        raise PreventUpdate
    elif n_clicks > 0:
        df1 = load_data('feature_1')
        df2 = load_data('feature_2')
        df_dist = compare_dist(df1, df2, max_d)
        if value_3 is not None:
            df3 = load_data('feature_3')
            df_dist_ext = compare_dist(df1, df3, max_d)
            df_dist_fil = pd.merge(left=df_dist, right=df_dist_ext,  how='inner', on ='feature_1')
            df_comb = pd.concat([df1.loc[df1.feature_1.isin(df_dist_fil.feature_1), :], \
                                 df2.loc[df2.feature_2.isin(df_dist_fil.feature_2), :]])
            df_comb = pd.concat([df_comb, df3.loc[df3.feature_3.isin(df_dist_fil.feature_3), :]])
        else:
            df_comb = pd.concat([df1.loc[df1.feature_1.isin(df_dist.feature_1), :], \
                                 df2.loc[df2.feature_2.isin(df_dist.feature_2), :]])
        features_df = pd.read_csv(os.path.join(DATA_DIR, 'features_key.csv'))
        df_final = pd.merge(left=df_comb, right=features_df,  how='inner', on ='feature')
        geojson = dlx.dicts_to_geojson([{**mkr, **dict(tooltip=\
                                                           f"{mkr['name']} | {mkr['Key']}-{mkr['Value']}\
                                                            | ({mkr['lat']}, {mkr['lon']})")\
                                                           } for mkr in df_final.to_dict('records')])
        return [geojson]


def load_data(fname):
    df = pd.read_csv(f'data/{fname}.csv', index_col=0)
    df[['lat_rad', 'lon_rad']] = (np.radians(df.loc[:, ['lat', 'lon']]))
    df.rename(columns={"id": fname}, inplace=True)
    df['feature'] = fname
    return df


def compare_dist(df1, df2, max_distance):
    dist = DistanceMetric.get_metric('haversine')
    col_name1, col_name2 = [df1.columns[0], df2.columns[0]]
    dist_matrix = (dist.pairwise(df1[['lat_rad', 'lon_rad']], df2[['lat_rad', 'lon_rad']]) * 3959)
    df_dist = pd.DataFrame(dist_matrix, index=df1.loc[:, col_name1], columns=df2.loc[:, col_name2])
    df_dist_m = pd.melt(df_dist.reset_index(), id_vars=col_name1)
    return df_dist_m.loc[df_dist_m.value < max_distance, :]


def build_query(key_1, value_1, key_2, value_2, key_3, value_3, bbox):
    lat1, lon1 = bbox[0]
    lat2, lon2 = bbox[1]
    # fetch all ways and nodes
    api_query1 = f"node[{key_1}={value_1}] ({lat1},{lon1},{lat2},{lon2});out;"
    api_query2 = f"node[{key_2}={value_2}] ({lat1},{lon1},{lat2},{lon2});out;"
    api_query3 = f"node[{key_3}={value_3}] ({lat1},{lon1},{lat2},{lon2});out;"
    result1 = api.query(api_query1)
    print(f"q1: {api_query1}")
    result2 = api.query(api_query2)
    print(f"q2: {api_query2}")
    result3 = api.query(api_query3)
    print(f"q3: {api_query3}")

    ids = ["id", "lat", "lon", "name"]

    if value_3 is not None:
        features = [result1, result2, result3]
    else:
        features = [result1, result2]

    for val, feat in enumerate(features):
        tmp_dc = list()
        for node in feat.nodes:
            tmp_dc.append([node.id, float(node.lat), float(node.lon), node.tags.get('name')])
        pd.DataFrame(tmp_dc, columns=ids).to_csv(os.path.join(DATA_DIR, f'feature_{val+1}.csv'))

    features_ls = [['feature_1', key_1, value_1],['feature_2', key_2, value_2],['feature_3', key_3, value_3]]
    features_df = pd.DataFrame(features_ls, columns=['feature', 'Key', 'Value'])
    features_df.to_csv(os.path.join(DATA_DIR, 'features_key.csv'))

    print("Saved CSV for each feature")
    result_string = html.Div([html.H5('Features Summary:'),
                              html.H6(f"{key_1}-{value_1}: {str(len(result1.nodes))}"),
                            html.H6(f"{key_2}-{value_2}: {str(len(result2.nodes))}"),
                            html.H6(f"{key_3}-{value_3}: {str(len(result3.nodes))}")])
    return result_string


# image upload func
@app.callback([Output('output-image-upload', 'children'), Output('image-tri', 'figure')],
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is None:
        raise PreventUpdate
    else:
        img_path = save_file(list_of_names, list_of_contents)
        fig = px.imshow(io.imread(img_path), binary_backend="jpg")
        fig.update_layout(
            newshape_line_color='#FD3216',
            margin=dict(l=0, r=0, b=0, t=0, pad=4),
            dragmode="drawrect",
        )
        return [parse_contents(list_of_names, list_of_dates), fig]

def parse_contents(filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),
    ])

def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    fn = os.path.join(UPLOAD_DIR, name)
    with open(fn, "wb") as fp:
        fp.write(base64.decodebytes(data))
    return fn

