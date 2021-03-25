import os
import math
import requests

import pandas as pd
import numpy as np
np.warnings.filterwarnings('ignore')
from scipy.optimize import curve_fit
#pylint: disable=unbalanced-tuple-unpacking

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
import plotly.graph_objs as go
from plotly.subplots import make_subplots

from risk_calculator import Create_Calculator, register_risk_callbacks
from graphs import Create_Graphs, register_graphs_callbacks

app = dash.Dash(__name__,
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[
                    {
                        'name' : 'author',
                        'content' : 'Josh Voytek'
                    },
                    {
                        'name' : 'type',
                        'property' : 'og:type',
                        'content' : 'Data Visualization'
                    },
                    {
                        'name' : 'description',
                        'property' : 'og:description',
                        'content' : 'Compilation of Covid-19 data for ease of visualization. '
                    },
                    {
                        'name' : 'image',
                        'property' : 'og:image',
                        'content' : 'assets/thumbnail.PNG'
                    },
                    {
                        'name' : 'keywords',
                        'property' : 'og:keywords',
                        'content' : 'Python, Plotly, Dash, Covid-19, Coronavirus, Pandemic'
                    }
                ]
            )

register_risk_callbacks(app)
register_graphs_callbacks(app)

server = app.server
app.config.suppress_callback_exceptions = True
app.title = "Kassandra Database"

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/graphs':
        return Create_Graphs()
    else:
        return Create_Calculator()

if __name__ == '__main__':
    app.run_server(debug=True)