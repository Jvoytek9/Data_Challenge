import os
from datetime import date
import datetime
import pandas as pd
import itertools
import math
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
                        'content' : 'Compilation of modern Surfactant/Foam Literature for applications in waterless geothermal fracking. ' +
                        'Built with the concept of being added to easily.'
                    },
                    {
                        'name' : 'image',
                        'property' : 'og:image',
                        'content' : 'assets/thumbnail.png'
                    },
                    {
                        'name' : 'keywords',
                        'property' : 'og:keywords',
                        'content' : 'Python, Plotly, Dash, Waterless, Geothermal, Fracking'
                    }
                ]
            )

server = app.server
app.config.suppress_callback_exceptions = True
app.title = "Data Challenge"

if 'DYNO' in os.environ:
    app_name = os.environ['DASH_APP_NAME']
else:
    app_name = 'dash-3dscatterplot'

Graph_Height = 605

today = date.today()
today = today.strftime("%m/%d/%Y")

county_confirmed_cases=pd.read_csv('https://query.data.world/s/qcn2c577llw3aasduxurmcicaulkst')
state_codes = pd.read_csv(r"C:\Users\Josh\OneDrive\Documents\Data_Challenge\Scripts\data\states.csv")
dv=pd.read_csv('https://covidtracking.com/data/download/all-states-history.csv')

dv = dv.drop('positiveScore', 1)
dv = dv.replace({'#REF!': np.nan})
dv[['date', 'state', 'dataQualityGrade']] = dv[['date', 'state', 'dataQualityGrade']].fillna(value="Not Defined")

dv['timeWeeks'] = (pd.Timestamp.now().normalize() - pd.to_datetime(dv['date'])) / np.timedelta64(1, 'D')
dv['timeWeeks'] /= 7
max_time = dv['timeWeeks'].iat[-1]
max_time = math.ceil(max_time)
interval = int(math.ceil(max_time/10))

intervals = []
for i in range(1,interval+1):
    intervals.append(i*10)

dv['Color'] = "any"
names = list(dict.fromkeys(dv['state']))
color = [
    '#1f77b4',  # muted blue
    '#ff7f0e',  # safety orange
    '#2ca02c',  # cooked asparagus green
    '#d62728',  # brick red
    '#9467bd',  # muted purple
    '#8c564b',  # chestnut brown
    '#e377c2',  # raspberry yogurt pink
    '#bcbd22',  # curry yellow-green
    '#17becf',  # blue-teal
    'black', 'blue', 'blueviolet', 'cadetblue',
    'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
    'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
    'darkgoldenrod', 'darkgray', 'darkgrey', 'darkgreen',
    'darkkhaki', 'darkmagenta', 'darkolivegreen', 'darkorange',
    'darkorchid', 'darkred', 'darksalmon', 'darkseagreen',
    'darkslateblue', 'darkslategray', 'darkslategrey',
    'darkturquoise', 'darkviolet', 'deeppink', 'deepskyblue',
    'dimgray', 'dimgrey', 'dodgerblue', 'firebrick',
    'floralwhite', 'forestgreen', 'fuchsia', 'gainsboro',
    'ghostwhite', 'gold', 'goldenrod', 'gray', 'grey', 'green',
    'greenyellow', 'honeydew', 'hotpink', 'indianred', 'indigo',
    'ivory', 'khaki', 'lavender', 'lavenderblush', 'lawngreen',
    'lemonchiffon', 'lightblue', 'lightcoral', 'lightcyan',
    'lightgoldenrodyellow', 'lightgray', 'lightgrey',
    'lightgreen', 'lightpink', 'lightsalmon', 'lightseagreen',
    'lightskyblue', 'lightslategray', 'lightslategrey',
    'lightsteelblue', 'lightyellow', 'lime', 'limegreen',
    'linen', 'magenta', 'maroon', 'mediumaquamarine',
    'mediumblue', 'mediumorchid', 'mediumpurple',
    'mediumseagreen', 'mediumslateblue', 'mediumspringgreen',
    'mediumturquoise', 'mediumvioletred', 'midnightblue',
    'mintcream', 'mistyrose', 'moccasin', 'navajowhite', 'navy',
    'oldlace', 'olive', 'olivedrab', 'orange', 'orangered',
    'orchid', 'palegoldenrod', 'palegreen', 'paleturquoise',
    'palevioletred', 'papayawhip', 'peachpuff', 'peru', 'pink',
    'plum', 'powderblue', 'purple', 'red', 'rosybrown',
    'royalblue', 'saddlebrown', 'salmon', 'sandybrown',
    'seagreen', 'seashell', 'sienna', 'silver', 'skyblue',
    'slateblue', 'slategray', 'slategrey', 'springgreen',
    'steelblue', 'tan', 'teal', 'thistle', 'tomato', 'turquoise',
    'violet', 'wheat', 'whitesmoke', 'yellow',
    'yellowgreen'
]
color_index = 0
for i in names:
    dv.loc[dv.state == i, 'Color'] = color[color_index]
    color_index += 1
#print(dv[dv.Study == "Kruss 2019"]) #check for colors you do not like

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

graph = dbc.Row([
    dbc.Col([
        html.Div([
            html.Div([html.H1("Graph 2")],style={'text-align':"center", "margin-left":"auto","margin-right":"auto", 'color':"white"}),
            dbc.Row([
                dbc.Col(html.H6("X: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-xaxis2", placeholder = "Select x-axis", value = "timeWeeks",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[3:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),

            dbc.Row([
                dbc.Col(html.H6("Y: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-yaxis2", placeholder = "Select y-axis", value = "deathIncrease",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[3:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),

            dbc.Row([
                dcc.RadioItems(
                    id='toggle2',
                    options=[{'label': i, 'value': i} for i in ['Show Less','Show More']],
                    value='Show Less',
                    labelStyle={"padding-right":"10px","margin":"auto"},
                    style={"text-align":"center","margin":"auto"}
                ),
            ],style={'text-align':"center","margin-left": "auto", "margin-right": "auto"}),

            html.Div([
                html.Div(id='controls-container2', children=[

                    html.Hr(),

                    html.Div(
                        dcc.Checklist(
                            id = 'bestfit2',
                            options= [{'label': i, 'value': i} for i in ['Scatter','Poly-Fit','Log-Fit','Exp-Fit', 'Power-Fit']],
                            value = ['Scatter'],
                            labelStyle={"padding-right":"10px","margin":"auto"}
                        )
                    ,style={"margin":"auto"}),

                    html.Div([
                        html.H6("Degree:",style={"padding-top":"10px"}),
                        dcc.Slider(
                            id="input_fit2",
                            max=3,
                            min=1,
                            value=1,
                            step=1,
                            included=False,
                            marks={
                                1: {'label': '1'},
                                2: {'label': '2'},
                                3: {'label': '3'}
                            }
                        )
                    ]),

                html.Hr(),

                html.Details([
                    html.Summary("Time-Elapsed(Weeks)"),

                    html.Div([
                        dcc.Slider(
                            id="gasses2",
                            max=max(intervals),
                            min=min(intervals),
                            value=max(intervals),
                            step=10,
                            included=True,
                            marks= {i: '{}'.format(i) for i in intervals},
                        )
                    ],style={"padding-top":"10%"}),
                ]),

                html.Hr(),

                html.Details([
                    html.Summary("States"),

                    dbc.Row([
                        dbc.Col(
                            dbc.Button('Select All', id='allsurf2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='dallsurf2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'surfactants2',
                        options= [{'label': surfactant, 'value': surfactant} for surfactant in np.sort(list(dict.fromkeys(state_codes["State"]+"("+state_codes["Code"]+")")))],
                        value = list(dict.fromkeys(state_codes["State"]+"("+state_codes["Code"]+")")),
                        labelStyle={'display': 'block'}
                    ),
                ]),

                html.Hr(),

                html.Details([
                    html.Summary("Data Quality Rating"),

                    dbc.Row([
                        dbc.Col(
                            dbc.Button('Select All', id='allsconc2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='dallsconc2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'sconc2',
                        options= [{'label': sc, 'value': sc} for sc in np.sort(list(dict.fromkeys(dv['dataQualityGrade'])))],
                        value = list(dict.fromkeys(dv['dataQualityGrade'])),
                        labelStyle={'display': 'block'}
                    ),
                ]),

                html.Hr(),

                ],style={"display":"none"}),
            ],style={"text-align":"center", "margin-left": "auto", "margin-right": "auto", "width": "80%", "backgroundColor": 'white', "border-radius":3,"position":"relative"}),


        ],id="compare_dropdown",style={"display":"None"}),

        html.Div([html.H1("Data Challenge")],
            style={'text-align':"center", "margin-right":"auto","margin-left":"auto", 'color':"white","width": "80%","padding-top":"15%"}),

        html.Div([
            dbc.Row([
                dbc.Col(html.H6("X: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-xaxis", placeholder = "Select x-axis", value = "timeWeeks",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[3:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),


            dbc.Row([
                dbc.Col(html.H6("Y: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-yaxis", placeholder = "Select y-axis", value = "positiveIncrease",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[3:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),

            html.Div([
                
                dbc.Row([
                    dcc.RadioItems(
                        id='toggle',
                        options=[{'label': i, 'value': i} for i in ['Show Less','Show More']],
                        value='Show Less',
                        labelStyle={"padding-right":"10px","margin":"auto"},
                        style={"text-align":"center","margin":"auto"}
                    ),
                ],style={'text-align':"center","margin-left": "auto", "margin-right": "auto"}),

                html.Div(id='controls-container', children=[

                    html.Hr(),

                    html.Div(
                        dcc.RadioItems(
                            id='addComp',
                            options=[{'label': i, 'value': i} for i in ['No Compare','Compare']],
                            value='No Compare',
                            labelStyle={"padding-right":"10px","margin":"auto","padding-bottom":"10px"}
                        )
                    ,style={"margin":"auto"}),

                    html.Div(
                        dcc.Checklist(
                            id = 'bestfit',
                            options= [{'label': i, 'value': i} for i in ['Scatter','Poly-Fit','Log-Fit','Exp-Fit', 'Power-Fit']],
                            value = ['Scatter'],
                            labelStyle={"padding-right":"10px","margin":"auto"}
                        )
                    ,style={"margin":"auto"}),

                    html.Div([
                        html.H6("Degree:",style={"padding-top":"10px"}),
                        dcc.Slider(
                            id="input_fit",
                            max=3,
                            min=1,
                            value=1,
                            step=1,
                            included=False,
                            marks={
                                1: {'label': '1'},
                                2: {'label': '2'},
                                3: {'label': '3'}
                            }
                        )
                    ]),

                html.Hr(),

                html.Details([
                    html.Summary("Time-Elapsed(Weeks)"),

                    html.Div([
                        dcc.Slider(
                            id="gasses",
                            max=max(intervals),
                            min=min(intervals),
                            value=max(intervals),
                            step=10,
                            included=True,
                            marks= {i: '{}'.format(i) for i in intervals},
                        )
                    ],style={"padding-top":"10%"}),
                ]),

                html.Hr(),

                html.Details([
                    html.Summary("States"),

                    dbc.Row([
                        dbc.Col(
                            dbc.Button('Select All', id='allsurf', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='dallsurf', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'surfactants',
                        options= [{'label': surfactant, 'value': surfactant} for surfactant in np.sort(list(dict.fromkeys(state_codes["State"]+"("+state_codes["Code"]+")")))],
                        value = list(dict.fromkeys(state_codes["State"]+"("+state_codes["Code"]+")")),
                        labelStyle={'display': 'block'}
                    ),
                ]),

                html.Hr(),

                html.Details([
                    html.Summary("Data Quality Rating"),

                    dbc.Row([
                        dbc.Col(
                            dbc.Button('Select All', id='allsconc', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='dallsconc', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'sconc',
                        options= [{'label': sc, 'value': sc} for sc in np.sort(list(dict.fromkeys(dv['dataQualityGrade'])))],
                        value = list(dict.fromkeys(dv['dataQualityGrade'])),
                        labelStyle={'display': 'block'}
                    ),
                ]),

                html.Hr(),

                ],style={"display":"none"}),
            ],style={"text-align":"center", "margin-left": "auto", "margin-right": "auto", "width": "80%", "backgroundColor": 'white', "border-radius":3,"position":"relative"}),

        ],style={'text-align':"center","margin-left": "auto", "margin-right": "auto", "width": "100%"}),

        dcc.Link('Home', href='/',style={'position':'absolute','top':0, 'left':0,"padding":5,"color":"white","font-size":18})

    ],style={'backgroundColor': '#9E1B34'},width=2),

    dbc.Col([
        dcc.Tabs(id="tabs", children=[
            dcc.Tab(label='2-Dimensions', children=[
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            dcc.Graph(id="comp1_2D_graph",
                            config = {'toImageButtonOptions':
                            {'width': None,
                            'height': None,
                            'format': 'png',
                            'filename': '2D_Plot_Comp1'}
                            })
                        ])
                    ),

                    dbc.Col(
                        html.Div([
                            dcc.Graph(id="comp2_2D_graph",
                                config = {'toImageButtonOptions':
                                {'width': None,
                                'height': None,
                                'format': 'png',
                                'filename': '2D_Plot_Comp2'}
                                })
                            ])
                    ,id="compare_graph_2D",style={"display":"None"})
                ],no_gutters=True),

                dbc.Row([
                    dbc.Col(
                        dt.DataTable(
                            id='comp1_2D_table',
                            page_current=0,
                            page_size=75,
                            export_format='xlsx',
                            style_data_conditional=[
                            {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                            }
                            ],
                            style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'},
                            style_table={"height":"20vh","min-height":"20vh"},
                            fixed_rows={'headers': True},
                            style_cell={
                                'height': 'auto',
                                'minWidth': 'auto', 'width': 'auto', 'maxWidth': 'auto',
                                'whiteSpace': 'normal'
                            },
                            css=[{'selector': '.row', 'rule': 'margin: 0'}]
                        ),style={"padding-left":20,"padding-right":20}
                    ),

                    dbc.Col(
                        dt.DataTable(
                            id='comp2_2D_table',
                            page_current=0,
                            page_size=75,
                            columns=[{'id': c, 'name': c} for c in dv.columns[3:-1]],
                            export_format='xlsx',
                            style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': 'rgb(248, 248, 248)'
                                }
                            ],
                            style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'},
                            style_table={"height":"20vh","min-height":"20vh"},
                            fixed_rows={'headers': True},
                            style_cell={
                                'height': 'auto',
                                'minWidth': 'auto', 'width': 'auto', 'maxWidth': 'auto',
                                'whiteSpace': 'normal'
                            },
                            css=[{'selector': '.row', 'rule': 'margin: 0'}]
                        )
                    ,style={"display":"None"},id="compare_table_2D")
                ],no_gutters=True)
            ]),

            dcc.Tab(label='Table', children=[
                dt.DataTable(
                    id='table',
                    data = dv.to_dict('records'),
                    columns = [{'id': c, 'name': c} for c in dv.columns[:-1]],
                    page_current=0,
                    page_size=75,
                    style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(248, 248, 248)'
                    }],
                    style_header={'backgroundColor': 'rgb(230, 230, 230)','fontWeight': 'bold'},
                    style_cell={
                        'height': 'auto',
                        'minWidth': 'auto', 'width': 'auto', 'maxWidth': 'auto',
                        'whiteSpace': 'normal'
                    },
                    style_table={
                        'height': "87vh",
                        'min-height': "87vh",
                        'overflowY': 'scroll',
                        'overflowX': 'scroll',
                        'width': '100%',
                        'minWidth': '100%',
                    },
                    css=[{'selector': '.row', 'rule': 'margin: 0'}]
                )
            ])
        ])
    ])
],no_gutters=True,style={"height":"100vh"})

home = html.Div([
    dbc.Row([
        dbc.Col(
            dcc.Link('Graph', href='/graph',style={'position':'absolute','top':0, 'left':0,"padding":5,"color":"white","font-size":18}),
            width=3
        ),
        dbc.Col([
            dcc.Tabs(id="tabs", children=[
                dcc.Tab(label='Risk Calculator', children=[
                    html.Br(),
                    html.H1("Calculator",style={"text-align":"center"}),
                    html.Br(),
                    
                    html.P("Last Updated: " + today,style={"text-align":"center"})
                ]),
                dcc.Tab(label='About', children=[
                    html.Br(),
                    html.H1("Team",style={"text-align":"center"}),
                    html.Br(),
                    dbc.Row([
                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="/assets/Voytek.jpg", top=True,style={"height":"25vh","width":"100%"}),
                                dbc.CardBody(
                                    [
                                        html.H5("Josh Voytek", className="card-title"),
                                        html.Hr(),
                                        html.H6("MechE Student"),
                                        html.A("josh.voytek@temple.edu", href="mailto: josh.voytek@temple.edu")
                                    ]
                                ,style={"text-align":"center"})
                            ])
                        ),

                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="/assets/Maltepes.JPG", top=True,style={"height":"25vh","width":"100%"}),
                                dbc.CardBody(
                                    [
                                        html.H5("Maria Maltepes", className="card-title"),
                                        html.Hr(),
                                        html.H6("Bioinformatics Student"),
                                        html.A("maria.maltepes@temple.edu", href="mailto: maria.maltepes@temple.edu")
                                    ]
                                ,style={"text-align":"center"})
                            ])
                        ),
                        dbc.Col(
                            dbc.Card([
                                dbc.CardImg(src="/assets/Legner.jpg", top=True,style={"height":"25vh","width":"100%"}),
                                dbc.CardBody(
                                    [
                                        html.H5("Anna Lengner", className="card-title"),
                                        html.Hr(),
                                        html.H6("BioE Student"),
                                        html.A("anna.lengner@temple.edu", href="mailto: anna.lengner@temple.edu")
                                    ]
                                ,style={"text-align":"center"})
                            ])
                        ),
                    ],style={"margin-left":"auto","margin-right":"auto","width":"80%"},no_gutters=True),
                    
                    html.Br(),
                    html.Div([
                        html.A("Here", href="https://covidtracking.com/about-data/data-definitions", style={"display":"inline-block"}),
                        html.P("is a link which defines each of the variables used in this dashboard.", style={"margin-left": "5px","display":"inline-block"}),
                        html.P("We added a variable, timeWeeks, which is the time-elapsed(units:weeks) from when the data was recorded to today. All data displayed in this site taken from the Covid Tracking Project.", style={"display":"inline-block"})
                    ],style={"font-size":23,"padding-left":30,"padding-right":30,"text-align":"center"})
                ])
            ]),
        ],style={"backgroundColor":"white"}),
        dbc.Col(style={'backgroundColor': '#9E1B34',"height":"100vh"},width=3)
    ],style={'backgroundColor': '#9E1B34',"height":"100%"},no_gutters=True)
])

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/graph':
        return graph
    else:
        return home

@app.callback(
    Output('controls-container', 'style'),
    [Input('toggle', 'value')])

def toggle_showmore_container(toggle_value):
    if toggle_value == 'Show More':
        return {'display': 'block','max-height':250,'overflow-y':'auto',"border-top":"1px black solid"}
    else:
        return {'display': 'none'}

@app.callback(
    Output('controls-container2', 'style'),
    [Input('toggle2', 'value')])

def toggle_showmore_container2(toggle_value):
    if toggle_value == 'Show More':
        return {'display': 'block','max-height':250,'overflow-y':'auto',"border-top":"1px black solid"}
    else:
        return {'display': 'none'}

@app.callback(
    [Output('surfactants', 'value')],
    [Input('allsurf', 'n_clicks'),
     Input('dallsurf', 'n_clicks')],
    [State('surfactants', 'value'),
     State('surfactants', 'options')]
)
def select_deselect_all_surfactants(allsurf,dallsurf,surf_value,surf_options):          
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if changed_id == 'allsurf.n_clicks':
        return([[value['value'] for value in surf_options]])
    elif changed_id == 'dallsurf.n_clicks':
        return([[]])
    else:
        return([surf_value])

@app.callback(
    [Output('surfactants2', 'value')],
    [Input('allsurf2', 'n_clicks'),
     Input('dallsurf2', 'n_clicks')],
    [State('surfactants2', 'value'),
     State('surfactants2', 'options')]
)
def select_deselect_all_surfactants2(allsurf,dallsurf,surf_value,surf_options):          
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

    if changed_id == 'allsurf2.n_clicks':
        return([[value['value'] for value in surf_options]])
    elif changed_id == 'dallsurf2.n_clicks':
        return([[]])
    else:
        return([surf_value])

@app.callback(
    [Output('sconc', 'value')],
    [Input('allsconc', 'n_clicks'),
     Input('dallsconc', 'n_clicks')],
    [State('sconc', 'value'),
     State('sconc', 'options')]
)
def select_deselect_all_surfconc(allsconc,dallscon,sconc_value,sconc_options):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if changed_id == 'allsconc.n_clicks':
        return([[value['value'] for value in sconc_options]])
    elif changed_id == 'dallsconc.n_clicks':
        return([[]])
    else:
        return([sconc_value])

@app.callback(
    [Output('sconc2', 'value')],
    [Input('allsconc2', 'n_clicks'),
     Input('dallsconc2', 'n_clicks')],
    [State('sconc2', 'value'),
     State('sconc2', 'options')]
)
def select_deselect_all_surfconc2(allsconc,dallscon,sconc_value,sconc_options):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    
    if changed_id == 'allsconc2.n_clicks':
        return([[value['value'] for value in sconc_options]])
    elif changed_id == 'dallsconc2.n_clicks':
        return([[]])
    else:
        return([sconc_value])

@app.callback(
    [Output('compare_dropdown', 'style'),
     Output('compare_graph_2D', 'style'),
     Output('compare_table_2D', 'style'),
     Output('toggle2', 'style')],
    [Input('addComp', 'value')])
def toggle_compare_container(compare_value):
    if compare_value == 'Compare':
        return [{'display': 'block',"position":"absolute","top":"55%","margin-right":"auto","margin-left":"auto","width":"100%","text-align":"center"},
                {'display': 'block'},
                {'display': 'block'},
                {"text-align":"center","margin":"auto","backgroundColor": 'white', "border-radius":3,"width":"80%"}]
    else:
        return [{'display': 'none'},
                {'display': 'none'},
                {'display': 'none'},
                {'display': 'none'}]

@app.callback(
    Output('table', 'style_data_conditional'),
    [Input("select-xaxis", "value"),
     Input("select-yaxis", "value")]
)
def update_master_table_styles(x,y):
    return [
    {
        'if': {'row_index': 'odd'},
        'backgroundColor': 'rgb(248, 248, 248)'
    },
    {
        'if': { 'column_id': x },
        'background_color': '#0066CC',
        'color': 'white',
    },
    {
        'if': { 'column_id': y },
        'background_color': '#0066CC',
        'color': 'white',
    }]

@app.callback(
    [Output("comp1_2D_graph", "figure"),
    Output("comp1_2D_table", "data"),
    Output("comp1_2D_table", "columns")],
    [Input("select-xaxis", "value"),
     Input("select-yaxis", "value"),
     Input('addComp', 'value'),
     Input("bestfit", "value"),
     Input("input_fit", "value"),
     Input('gasses', 'value'),
     Input('surfactants', 'value'),
     Input('sconc', 'value')],
)
def update_comp1_2D(selected_x, selected_y, comp, fit, order, ga, sur, surc):
    cl = dv[dv['timeWeeks'] <= ga]

    codes = []
    for element in sur:
        code = element[element.find("(")+1:element.find(")")]
        codes.append(code)
    ea = cl[cl["state"].isin(codes)]

    cleaned = ea[ea["dataQualityGrade"].isin(surc)]

    data = []
    for i in names:
        name_array = cleaned[cleaned.state == i]

        if len(name_array[selected_x].values) != 0 and len(name_array[selected_y].values) != 0:
            group_value = str(name_array.state.values[0])

            name_array = name_array.dropna(subset=[selected_x, selected_y],axis="rows")
            name_array.reset_index(drop=True)
            name_array.sort_values(by=selected_x, inplace=True)

            if len(name_array[selected_x]) > 2:
                x = np.array(name_array[selected_x])
                y = np.array(name_array[selected_y])
            else:
                continue
        else:
            continue

        if('Scatter' in fit):
            trace = go.Scattergl(x=x,y=y,
            hovertext= "Date Recorded: " + name_array.date
            + "<br />State: " + i
            + "<br />Data Quality: " + name_array["dataQualityGrade"],
            hoverinfo='text',mode='markers', marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
            name=i,legendgroup=group_value)

            data.append(trace)
        
        if('Poly-Fit' in fit):
            if('Scatter' in fit):
                showLegend = False
            else:
                showLegend = True
                
            z = np.polyfit(x,y,order)
            f = np.poly1d(z)

            y_new = f(x)

            f_new = []
            for num in f:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))

            if order == 1:
                equation = "y = " + str(f_new[1]) + "x + " + str(f_new[0])
                residuals = y- y_new
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((y-np.mean(y))**2)
                r_squared = str(np.round(1 - (ss_res / ss_tot),3))

            elif order == 2:
                equation = "y = " + str(f_new[2]) + "x² + " + str(f_new[1]) + "x + " + str(f_new[0])
                r_squared = "Non-Linear"
            elif order == 3:
                equation = "y = " + str(f_new[3]) + "x³ + " + str(f_new[2]) + "x² + " + str(f_new[1]) + "x + " + str(f_new[0])
                r_squared = "Non-Linear"

            trace = go.Scattergl(x = x, y = y_new,
            hovertext= "State: " + name_array.state
            + "<br />" + equation
            + "<br />R Squared: " + r_squared,
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=group_value)

            data.append(trace)

        if('Log-Fit' in fit):
            if('Scatter' in fit or "Poly-Fit" in fit):
                showLegend = False
            else:
                showLegend = True

            def logarithmic(x, a, b, c):
                return  a * np.log(b * x) + c
            
            popt, _ = curve_fit(logarithmic, x, y, maxfev = 999999999)

            y_new = logarithmic(x, popt[0],popt[1], popt[2])

            f_new = []
            for num in popt:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))

            trace = go.Scattergl(x = x, y = y_new,
            hovertext= "State: " + i
            + "<br />y = " + str(f_new[0]) + " * log(" + str(f_new[1]) + " * x) + " + str(f_new[2]),
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=group_value)

            data.append(trace)

        if('Exp-Fit' in fit):
            if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit):
                showLegend = False
            else:
                showLegend = True

            def exponential(x, a, b, c):
                return a * np.exp(b * x) + c
            
            popt, _ = curve_fit(exponential, x, y, maxfev = 999999999)

            y_new = exponential(x, popt[0],popt[1],popt[2])

            f_new = []
            for num in popt:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))

            trace = go.Scattergl(x = x, y = y_new,
            hovertext= "State: " + i
            + "<br />y = " + str(f_new[0]) + " * e^(" + str(f_new[1]) + " * x) + " + str(f_new[2]),
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=group_value)

            data.append(trace)

        if('Power-Fit' in fit):
            if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit or "Exp-Fit" in fit):
                showLegend = False
            else:
                showLegend = True

            def power(x, a, N, b):
                return a * np.power(x,N) + b
            
            popt, _ = curve_fit(power, x, y, maxfev = 999999999)

            y_new = power(x, popt[0],popt[1],popt[2])

            f_new = []
            for num in popt:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))
            

            trace = go.Scattergl(x = x, y = y_new,
            hovertext= "State: " + i
            + "<br />y = " + str(f_new[0]) + " * x^(" + str(f_new[1]) + ") + " + str(f_new[2]),
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=group_value)

            data.append(trace)

    cleaned = cleaned[[selected_x,selected_y]]

    return [{
        'data': data,
        'layout': go.Layout(
            yaxis={
                "title":selected_y,
                "titlefont_size":20,
                "tickfont_size":18,
            },
            xaxis={
                "title":selected_x,
                "titlefont_size":20,
                "tickfont_size":18
            },
            legend={
                "font_size": 24,
            },
            font={
                "family":"Times New Roman",
            },
            hovermode="closest",
            height=Graph_Height
        )
    },cleaned.to_dict('records'), [{'id': c, 'name': c} for c in cleaned.columns]]

@app.callback(
    [Output("comp2_2D_graph", "figure"),
     Output("comp2_2D_table", "data"),
     Output("comp2_2D_table", "columns")],
    [Input("select-xaxis2", "value"),
     Input("select-yaxis2", "value"),
     Input('addComp', 'value'),
     Input("bestfit2", "value"),
     Input("input_fit2", "value"),
     Input('gasses2', 'value'),
     Input('surfactants2', 'value'),
     Input('sconc2', 'value')],
)
def update_comp2_2D(selected_x, selected_y, comp, fit, order, ga, sur, surc):
    if comp == "No Compare":
        return [{},[],[]]
        
    cl = dv[dv['timeWeeks'] <= ga]

    codes = []
    for element in sur:
        code = element[element.find("(")+1:element.find(")")]
        codes.append(code)
    ea = cl[cl["state"].isin(codes)]

    cleaned = ea[ea["dataQualityGrade"].isin(surc)]

    data = []
    for i in names:
        name_array = cleaned[cleaned.state == i]

        if len(name_array[selected_x].values) != 0 and len(name_array[selected_y].values) != 0:
            group_value = str(name_array.state.values[0])

            name_array = name_array.dropna(subset=[selected_x, selected_y],axis="rows")
            name_array.reset_index(drop=True)
            name_array.sort_values(by=selected_x, inplace=True)

            if len(name_array[selected_x]) > 2:
                x = np.array(name_array[selected_x])
                y = np.array(name_array[selected_y])
            else:
                continue
        else:
            continue

        if('Scatter' in fit):
            trace = go.Scattergl(x=x,y=y,
            hovertext= "Date Recorded: " + name_array.date
            + "<br />State: " + i
            + "<br />Data Quality: " + name_array["dataQualityGrade"],
            hoverinfo='text',mode='markers', marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
            name=i,legendgroup=group_value)

            data.append(trace)
        
        if('Poly-Fit' in fit):
            if('Scatter' in fit):
                showLegend = False
            else:
                showLegend = True
                
            z = np.polyfit(x,y,order)
            f = np.poly1d(z)

            y_new = f(x)

            f_new = []
            for num in f:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))

            if order == 1:
                equation = "y = " + str(f_new[1]) + "x + " + str(f_new[0])
                residuals = y- y_new
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((y-np.mean(y))**2)
                r_squared = str(np.round(1 - (ss_res / ss_tot),3))

            elif order == 2:
                equation = "y = " + str(f_new[2]) + "x² + " + str(f_new[1]) + "x + " + str(f_new[0])
                r_squared = "Non-Linear"
            elif order == 3:
                equation = "y = " + str(f_new[3]) + "x³ + " + str(f_new[2]) + "x² + " + str(f_new[1]) + "x + " + str(f_new[0])
                r_squared = "Non-Linear"

            trace = go.Scattergl(x = x, y = y_new,
            hovertext= "State: " + name_array.state
            + "<br />" + equation
            + "<br />R Squared: " + r_squared,
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=group_value)

            data.append(trace)

        if('Log-Fit' in fit):
            if('Scatter' in fit or "Poly-Fit" in fit):
                showLegend = False
            else:
                showLegend = True

            def logarithmic(x, a, b, c):
                return  a * np.log(b * x) + c
            
            popt, _ = curve_fit(logarithmic, x, y, maxfev = 999999999)

            y_new = logarithmic(x, popt[0],popt[1], popt[2])

            f_new = []
            for num in popt:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))

            trace = go.Scattergl(x = x, y = y_new,
            hovertext= "State: " + i
            + "<br />y = " + str(f_new[0]) + " * log(" + str(f_new[1]) + " * x) + " + str(f_new[2]),
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=group_value)

            data.append(trace)

        if('Exp-Fit' in fit):
            if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit):
                showLegend = False
            else:
                showLegend = True

            def exponential(x, a, b, c):
                return a * np.exp(b * x) + c
            
            popt, _ = curve_fit(exponential, x, y, maxfev = 999999999)

            y_new = exponential(x, popt[0],popt[1],popt[2])

            f_new = []
            for num in popt:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))

            trace = go.Scattergl(x = x, y = y_new,
            hovertext= "State: " + i
            + "<br />y = " + str(f_new[0]) + " * e^(" + str(f_new[1]) + " * x) + " + str(f_new[2]),
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=group_value)

            data.append(trace)

        if('Power-Fit' in fit):
            if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit or "Exp-Fit" in fit):
                showLegend = False
            else:
                showLegend = True

            def power(x, a, N, b):
                return a * np.power(x,N) + b
            
            popt, _ = curve_fit(power, x, y, maxfev = 999999999)

            y_new = power(x, popt[0],popt[1],popt[2])

            f_new = []
            for num in popt:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))
            

            trace = go.Scattergl(x = x, y = y_new,
            hovertext= "State: " + i
            + "<br />y = " + str(f_new[0]) + " * x^(" + str(f_new[1]) + ") + " + str(f_new[2]),
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=group_value)

            data.append(trace)

    cleaned = cleaned[[selected_x,selected_y]]

    return [{
        'data': data,
        'layout': go.Layout(
            yaxis={
                "title":selected_y,
                "titlefont_size":20,
                "tickfont_size":18,
            },
            xaxis={
                "title":selected_x,
                "titlefont_size":20,
                "tickfont_size":18
            },
            legend={
                "font_size": 24,
            },
            font={
                "family":"Times New Roman",
            },
            hovermode="closest",
            height=Graph_Height
        )
    },cleaned.to_dict('records'), [{'id': c, 'name': c} for c in cleaned.columns]]

if __name__ == '__main__':
    app.run_server(debug=True)