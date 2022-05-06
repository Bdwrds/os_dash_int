from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import time
from skimage import io
import dash_leaflet as dl
import pandas as pd

DEBUG = True

NUM_ATYPES = 15
DEFAULT_FIG_MODE = "layout"
annotation_colormap = px.colors.qualitative.Light24

OSM_KEY_LS = ['amenity', 'railway', 'military', 'man_made', 'shop']

DEFAULT_ATYPE = OSM_KEY_LS[0]

# prepare bijective type<->color mapping
typ_col_pairs = [
    (t, annotation_colormap[n % len(annotation_colormap)])
    for n, t in enumerate(OSM_KEY_LS)
]
# types to colors
color_dict = {}
# colors to types
type_dict = {}
for typ, col in typ_col_pairs:
    color_dict[typ] = col
    type_dict[col] = typ

filelist = [
    "images/town.jpg"
]


fig = px.imshow(io.imread(filelist[0]), binary_backend="jpg")

fig.update_layout(
    newshape_line_color=color_dict[DEFAULT_ATYPE],
    margin=dict(l=0, r=0, b=0, t=0, pad=4),
    dragmode="drawrect",
)


# Cards
tab_image_annotation = dbc.Card(
    id="imagebox",
    children=[
        dbc.CardHeader(html.H2("Image for Triangulation")),
        dbc.CardBody(
            [
                dcc.Graph(
                    id="image-tri",
                    figure=fig,
                    config={"modeBarButtonsToAdd": ["drawrect", "eraseshape"]},
                )
            ]
        ),
    ],
)

tab_annotated_data = dbc.Card(
    [   dbc.CardHeader(html.H2("Add Image Features")),
        dbc.CardBody(
            [dbc.Row(
                [
                    html.Label("Feature 1"),
                    dbc.Col(
                        dcc.Dropdown(
                            id="feature-key-1",
                            options=[{"label": t, "value": t} for t in OSM_KEY_LS],
                            value=OSM_KEY_LS[0],
                            clearable=False,
                        ),
                    ),
                    dbc.Col(dcc.Dropdown(id="feature-value-1"),),
                    html.Br(),
                    html.Br(),
                    html.Label("Feature 2"),
                    dbc.Col(
                        dcc.Dropdown(
                            id="feature-key-2",
                            options=[{"label": t, "value": t} for t in OSM_KEY_LS],
                            value=OSM_KEY_LS[0],
                            clearable=False,
                        ),
                    ),
                    dbc.Col(dcc.Dropdown(id="feature-value-2"),),
                    html.Br(),
                    html.Br(),
                    html.Label("Feature 3 (Optional)"),
                    dbc.Col(
                        dcc.Dropdown(
                            id="feature-key-3",
                            options=[{"label": t, "value": t} for t in OSM_KEY_LS],
                            value=OSM_KEY_LS[0],
                            clearable=False,
                        ),
                    ),
                    dbc.Col(dcc.Dropdown(id="feature-value-3"),),
                ]),
            ]
        )
    ],
)



tab_map = dbc.Card(
        [dbc.CardHeader(html.H2("View mapping")),
         dbc.CardBody(
             [
                 html.Div(children=[
                    dl.Map(
                        [dl.TileLayer(), dl.GeoJSON(id="geojson", data=None)], style={'width': '100%', 'height': '500px'}, zoom=10,
                        center=(51.455638052568475, -2.48042),
                        id='map'
                    ),
                    html.Br(),
                    html.H5('Search Coordinates'),
                    html.Div(id="log")],
                    style={'padding': 10, 'flex': 1}),
                 ])
         ]
)



tab_save_documents = \
    dbc.Card(
        [dbc.CardHeader(html.H2("Search Features")),
         dbc.CardBody(
             [
                 html.Div(children=[
                html.Div(className='six columns', children=[
                    html.Button('Submit OSM Query', id='sub-button-1', n_clicks=0),
                    html.Br(),
                    html.Br(),
                    dcc.Loading(
                        id="loading-1",
                        type="default",
                        children=[
                            html.Div(id='submit-output')
                        ]),
                    html.Br(),
                    dcc.ConfirmDialog(
                            id='confirm-danger',
                            message='Please enter a "Max Distance (Km)" between your features before clicking "Add Features to Map"!',
                        ),
                    html.Label('Max Distance (km)'),
                    dbc.Col(dcc.Input(id='input-max-dist', type='number'), width=3),
                    html.Br(),
                    html.Br(),
                    html.Button('Add Features to Map', id='sub-button-2', n_clicks=0),
                    dbc.Table.from_dataframe(id='print-output', df=pd.DataFrame()),
                    ], style={'padding': 5, 'flex': 1}),
                ], style=dict(display='flex'))
                 ])
         ]
    )


tab_upload_documents = \
    dbc.Card(
        [dbc.CardHeader(html.H2("Workflow")),
         dbc.CardBody(
             [
                 html.Div(children=[
                    html.H6('1. Upload a new image'),
                    html.H6('2. Identify 2-3 features in the image from dropdown key-value list'),
                    html.H6('3. Restrict Mapping to relevant coordinates'),
                    html.H6('4. Query OSM for Features within area'),
                    html.H6('5. Set the "Max Distance (Km)" between all features'),
                    html.H6('6. Click "Add Features to Map" to populate the map'),
                    ],
                    style={'padding': 10, 'flex': 1})
                 ])
         ]
    )

tab_output_documents = \
    dbc.Card(
        [dbc.CardHeader(html.H2("Upload Image")),
         dbc.CardBody(
             [
                 html.Div(children=[
                    dcc.Upload(
                            id='upload-image',
                            children=html.Div([
                                'Drop or ',
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
                            # Dont' allow multiple files to be uploaded
                            multiple=False
                        ),
                    html.Div(id='output-image-upload'),
                    ], style={'padding': 10, 'flex': 1})
             ])
         ]
    )


tab_workflow = dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(tab_upload_documents, md=8),
                        dbc.Col(tab_output_documents, md=4),
                    ],
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(tab_image_annotation, md=8),
                        dbc.Col(tab_annotated_data, md=4),
                    ],
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(tab_map, md=8),
                        dbc.Col(tab_save_documents, md=4),
                    ],
                ),
            ],
            fluid=True,
        )