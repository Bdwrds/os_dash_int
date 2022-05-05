
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dcc, html
#from dashboard.layout.documents import tab_documents
from dashboard.layout.workflow import tab_workflow
#from dashboard.layout.mapping import tab_mapping

from dashboard.index import app

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/1-intro"]:
        return html.P("This is the content of page 1!")
    elif pathname == "/2-training":
        return tab_workflow
    #elif pathname == "/3-mapping":
    #    return tab_mapping
    #elif pathname == "/4-documents":
        #return tab_documents
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )

