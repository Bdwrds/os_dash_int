"""
author: Ben E
date: 2022-04-22
"""
from dashboard.content import app


server = app.server
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)