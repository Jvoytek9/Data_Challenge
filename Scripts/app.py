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

state_codes = pd.read_csv(r"C:\Users\Josh\OneDrive\Documents\Data_Challenge\Scripts\data\states.csv")
master = pd.read_csv(r"C:\Users\Josh\OneDrive\Documents\Data_Challenge\Scripts\data\master.csv")
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
#print(dv[dv.State == "Kruss 2019"]) #check for colors you do not like

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
                        dcc.RangeSlider(
                            id="gasses2",
                            max=max(intervals),
                            min=min(intervals),
                            value=[min(intervals),max(intervals)],
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
                        dcc.RangeSlider(
                            id="gasses",
                            max=max(intervals),
                            min=min(intervals),
                            value=[min(intervals),max(intervals)],
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

                    html.Div([
                        html.H3("Risk Calculator",style={"display":"block"}),
                        
                        html.Br(),
                        html.H5("1. Basic Information: ",style={"display":"block"}),
                        
                        dcc.RadioItems(id="sex_input", options=[{'label': i, 'value': i} for i in master["sex"].dropna()],labelStyle={"padding-right":"5px"}),

                        dcc.Input(id="age_input", type="number", placeholder="Enter Age", min=0, debounce=True,style={"text-align":"center","width":"25%"}),

                        dcc.Dropdown(id="race_input", placeholder="Select Race", 
                        options= [{'label': i, 'value': i} for i in np.sort(list(dict.fromkeys(master["RACE"].dropna())))]
                        ,style={"width":"50%","margin":"auto"}),

                        dcc.Dropdown(id="state_input", placeholder="Select State", 
                        options= [{'label': i, 'value': i} for i in np.sort(list(dict.fromkeys(state_codes["State"].dropna()+"("+state_codes["Code"].dropna()+")")))]
                        ,style={"width":"50%","margin":"auto"}),

                        dcc.Dropdown(id="county_input", placeholder="Select County", 
                        options= [{'label': i, 'value': i} for i in np.sort(list(dict.fromkeys(master["COUNTY"].dropna())))]
                        ,style={"width":"50%","margin":"auto"}),

                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.H5("2. Preexisting Conditions: "),
                        html.Br(),

                        dcc.Checklist(id = 'med_input',
                        options= [{'label': sc, 'value': sc} for sc in np.sort(list(dict.fromkeys(master['prexistingCond'].dropna())))],
                        labelStyle={'display': 'inline-block',"padding-right":"15px"},
                        style={"width":"80%","margin":"auto"}),

                        html.Br(),
                        html.Br(),
                        html.Br(),
                        html.H5("3. Behaviour", style={"text-align":"center"}),
                        html.Br(),

                        dbc.Row([
                            dbc.Col(
                                html.H6("Activity:"),
                            ),
                            dbc.Col(
                                html.H6("Frequency Last 2 Weeks:")
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Getting takeout:"),
                            ),
                            dbc.Col(
                                dcc.Input(id="takeout_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Walk/run/bike with others outside:")
                            ),
                            dbc.Col(
                                dcc.Input(id="walk_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Visited library or museum:")
                            ),
                            dbc.Col(
                                dcc.Input(id="library_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Eating outside at resturant:"),
                            ),
                            dbc.Col(
                                dcc.Input(id="eatOutside_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Walking in a busy town:")
                            ),
                            dbc.Col(
                                dcc.Input(id="walkingTown_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Attended a backyard bbq:")
                            ),
                            dbc.Col(
                                dcc.Input(id="BBQ_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Went to a beach:")
                            ),
                            dbc.Col(
                                dcc.Input(id="beach_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Shopped at a mall:")
                            ),
                            dbc.Col(
                                dcc.Input(id="mall_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Visiting an elderly relative/friend at home:")
                            ),
                            dbc.Col(
                                dcc.Input(id="grandpa_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Swam in a public pool:")
                            ),
                            dbc.Col(
                                dcc.Input(id="pool_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),
                            
                        dbc.Row([
                            dbc.Col(
                                html.P("Went to a salon/barber:")
                            ),
                            dbc.Col(
                                dcc.Input(id="barber_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Eating inside a resturant:")
                            ),
                            dbc.Col(
                                dcc.Input(id="eatInside_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Traveled by plane:")
                            ),
                            dbc.Col(
                                dcc.Input(id="plane_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Ate at a buffet:")
                            ),
                            dbc.Col(
                                dcc.Input(id="buffet_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Worked out at a gym:")
                            ),
                            dbc.Col(
                                dcc.Input(id="gym_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),

                        dbc.Row([
                            dbc.Col(
                                html.P("Went to a bar:")
                            ),
                            dbc.Col(
                                dcc.Input(id="bar_input", type="number", min=0, value=0, placeholder= "", style={"text-align":"center"})
                            )
                        ],style={"width":"60%","margin":"auto"}),
                    
                    html.Br(),
                    html.H4("State Percent Positive: ",style={"display":"inline-block"}),
                    dcc.Input(id='state_stat', value='', type='text',style={"display":"inline-block","width":"40%","text-align":"center"},readOnly=True),
                    html.Br(),
                    html.P("The World Health Organization (WHO) recommends the percent positive to stay below 5% for two weeks before governments consider reopening. " +
                    "If your state has a percent positive higher than 5%, you should take greater precautions by minimizing unessential activities. ",style={"display":"inline","padding-right":"5px"}),
                    html.Br(),
                    html.Br(),
                    html.P("The percent positive is the percentage of all coronavirus tests performed that come back positive. If the number of total tests remains too low or " + 
                    "if the number of positive results remains too high for your state, then the percent positive will be high. " + 
                    "A high percent positive value can indicate high transmission within the population or that there are more people with COVID-19 that have not been tested yet.",style={"display":"inline"}),
                    html.Br(),

                    html.Br(),
                    html.H4("County Spread Rate: ",style={"display":"inline-block"}),
                    dcc.Input(id='county_stat', value='', type='text',style={"display":"inline","width":"40%","text-align":"center"},readOnly=True),
                    html.Br(),
                    html.P("Mask usage by county was retrieved from the",style={"display":"inline","padding-right":"5px"}),
                    html.A("NYTimes COVID-19 data: United States.", href="https://github.com/nytimes/covid-19-data/tree/master/mask-use",style={"display":"inline","padding-right":"5px"}),
                    html.P("The NYTimes requested a large scale survey by the firm Dynata to " +
                    "question mask use county by county. These surveys were conducted from 7/2/2020 - 7/14/2020 and received 250,000 responses. ",style={"display":"inline"}),
                    html.Br(),
                    html.Br(),
                    html.P("Based on a Monte Carlo simulation conducted in a paper titled",style={"display":"inline","padding-right":"5px"}), 
                    html.A("“Universal Masking is Urgent in the COVID-19 Pandemic: SEIR and Agent Based Models, Empirical Validation, Policy Recommendations”",href="https://arxiv.org/pdf/2004.13553.pdf",style={"display":"inline"}), 
                    html.P(", it was discovered that if 80% of a population wore masks, it may be more effective than an indefinite lockdown. " + 
                    "There was minimal impact when <50% of the population wore masks. If your county has a mask usage average lower than 80%, you should take greater precautions by " +
                    "minimizing unessential activities.",style={"display":"inline"}),
                    html.Br(),
                    html.Br(),
                    html.P("***Disclaimer: This is a preprint, so it has not been peer-reviewed yet.***"),

                    html.Br(),
                    html.H4("Behaviour Risk: ",style={"display":"inline-block"}),
                    dcc.Input(id='behaviour_stat', value='', type='text',style={"display":"inline-block","width":"40%","text-align":"center"},readOnly=True),
                    html.Br(),
                    html.P("The risks corresponding to each activity was ranked by physicians from the",style={"display":"inline","padding-right":"5px"}),
                    html.A("Texas Medical Association (TMA) COVID-19 Task Force and the TMA Committee on Infectious Diseases.",href="https://www.texmed.org/uploadedFiles/Current/2016_Public_Health/Infectious_Diseases/309193%20Risk%20Assessment%20Chart%20V2_FINAL.pdf",style={"display":"inline","padding-right":"5px"}),
                    html.P("The risk value is based on an assumption that the participants in these activities are still following current recommended " +
                    "safety protocols like mask-wearing and social distancing when possible. The factors determining risk include: whether the activity is solitary, " + 
                    "indoors or outdoors, and the amount of people participating. You should consider minimizing certain activities if you scored between moderate " + 
                    "risk to very high risk. This will lower your infection risk and the risk you transmit to others while presymptomatic or asymptomatic.",style={"display":"inline"}),
                    html.Br(),

                    html.Br(),
                    html.H4("Race Infection and Race Mortality Risk: ",style={"display":"inline-block"}),
                    html.Br(),
                    dcc.Input(id='infection_stat', value='', type='text',style={"display":"inline-block","width":"40%","text-align":"center"},readOnly=True),
                    dcc.Input(id='mortality_stat', value='', type='text',style={"display":"inline-block","width":"40%","text-align":"center"},readOnly=True),
                    html.Br(),
                    html.P("Racial data for COVID-19 was retrieved from the",style={"display":"inline","padding-right":"5px"}),
                    html.A("CDC.",href="https://www.cdc.gov/coronavirus/2019-ncov/covid-data/investigations-discovery/hospitalization-death-by-race-ethnicity.html",style={"display":"inline","padding-right":"5px"}),
                    html.P("The CDC used the infection and mortality rates for White, Non-hispanic persons as the comparison groups.",style={"display":"inline","padding-right":"5px"}),
                    html.Br(),
                    html.Br(),
                    html.P("It is important to note that an increased risk in infection and mortality races other than White, Non-hispanic does not indicate an inherent immune difference between races. According to the peer-reviewed paper",style={"display":"inline","padding-right":"5px"}),
                    html.A("“The Disproportionate Impact of COVID-19 on Racial and Ethnic Minorities in the United States”",href="https://academic.oup.com/cid/advance-article/doi/10.1093/cid/ciaa815/5860249",style={"display":"inline","padding-right":"5px"}),
                    html.P(", the differences in infection and mortality rates can be attributed to “minority communities [being] more likely to experience living and working conditions that predispose them to worse outcomes” " + 
                    "and other “long-standing structural and societal factors that the COVID-19 pandemic has exposed” such as systemic poverty and medical racism.",style={"display":"inline","padding-right":"5px"}),
                    html.Br(),
                    html.Br(),
                    html.P("***Disclaimer: The CDC does not provide data for those of more than one race so please choose one of the races you identify as if you are multiracial.***"),

                    html.Br(),
                    html.H4("Age Mortality Risk: ",style={"display":"inline-block"}),
                    dcc.Input(id='age_stat', value='', type='text',style={"display":"inline-block","width":"40%","text-align":"center"},readOnly=True),
                    html.Br(),
                    html.P("Age data was retrieved from the",style={"display":"inline","padding-right":"5px"}),
                    html.A("CDC.",href="https://www.cdc.gov/coronavirus/2019-ncov/covid-data/investigations-discovery/hospitalization-death-by-age.html",style={"display":"inline","padding-right":"5px"}),
                    html.P("The CDC used the mortality rate for 18-29 year olds as the comparison group.",style={"display":"inline"}),
                    html.Br(),
                    html.Br(),
                    html.P("Although those who are older than 29 have higher mortality rates, the 18-29 age group continues to",style={"display":"inline","padding-right":"5px"}),
                    html.A("hold the highest percentage of all COVID-19 cases.",href="https://covid.cdc.gov/covid-data-tracker/#demographics",style={"display":"inline","padding-right":"5px"}),
                    html.P("This is important to note because it indicates a shared responsibility of 18-29 year olds to minimize their risk of transmitting the virus by social distancing and wearing masks. The paper,",style={"display":"inline","padding-right":"5px"}),
                    html.A("“Why does COVID-19 disproportionately affect older people?”",href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7288963/",style={"display":"inline"}),
                    html.P(", they attribute the disproportionate mortality risk to” molecular differences between young, middle-aged, and older people.",style={"display":"inline"}),
                    html.Br(),

                    html.Br(),
                    html.H4("Sex Mortality Risk: ",style={"display":"inline-block"}),
                    dcc.Input(id='sex_stat', value='', type='text',style={"display":"inline-block","width":"40%","text-align":"center"},readOnly=True),
                    html.Br(),
                    html.P("There has been a higher mortality rate attached to males when compared to females. In the paper,",style={"display":"inline","padding-right":"5px"}),
                    html.A("“Sex differential in COVID-19 mortality varies markedly by age”",href="https://www.thelancet.com/journals/lancet/article/PIIS0140-6736(20)31748-7/fulltext",style={"display":"inline"}),
                    html.P(", men were found to have a 2x higher mortality rate which may be attributed to “lifestyle to differences in chromosomal structure”. They also found differences in mortality rates when looking at sex by age group.”",style={"display":"inline"}),
                    html.Br(),

                    html.Br(),
                    html.H4("Comorbitity Mortality Risks: ",style={"display":"inline-block"}),
                    html.Br(),
                    html.P("This data was retrieved from the CDC and the paper",style={"display":"inline","padding-right":"5px"}),
                    html.A("“Association of cardiovascular disease and 10 other pre-existing comorbidities with COVID-19 mortality: A systematic review and meta-analysis”.",href="https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0238215",style={"display":"inline","padding-right":"5px"}),
                    html.P("The paper analyzed data from more than 65,000 patients from 25 studies worldwide and compared hospitalized COVID-19 patients with these preexisting conditions to COVID-19 hospitalized without preexisting conditions. More research is needed to understand why certain conditions heighten the mortality risk.",style={"display":"inline"}),
                    html.Br(),
                    html.Br(),

                    html.Div(
                        dt.DataTable(
                            id='med_stat',
                            page_current=0,
                            page_size=75,
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
                        ),style={"padding-left":20,"padding-right":20})
                    
                    ],style={"padding":"10px","text-align":"center"})
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
    [Output("state_stat", "value"),
     Output("county_stat", "value"),
     Output("behaviour_stat", "value"),
     Output("mortality_stat", "value"),
     Output("infection_stat", "value"),
     Output("age_stat", "value"),
     Output("sex_stat", "value"),
     Output("med_stat", "data"),
     Output("med_stat", "columns")],
    [Input("sex_input", "value"),
     Input("race_input", "value"),
     Input("age_input", "value"),
     Input("state_input", "value"),
     Input("county_input", "value"),
     Input("med_input", "value"),
     Input("takeout_input", "value"),
     Input("walk_input", "value"),
     Input("library_input", "value"),
     Input("eatOutside_input", "value"),
     Input("walkingTown_input", "value"),
     Input("BBQ_input", "value"),
     Input("beach_input", "value"),
     Input("mall_input", "value"),
     Input("grandpa_input", "value"),
     Input("pool_input", "value"),
     Input("barber_input", "value"),
     Input("eatInside_input", "value"),
     Input("plane_input", "value"),
     Input("buffet_input", "value"),
     Input("gym_input", "value"),
     Input("bar_input", "value")]
)
def risk_analysis(sex,race,age,state,county,med,takeout,walk,lib,eatOut,walkTown,BBQ,beach,mall,grandpa,pool,barber,eatIn,plane,buffet,gym,bar):
    
    if state is None or county is None or race is None or sex is None or med is None:
        return ["Form Not Yet Complete","Form Not Yet Complete","Form Not Yet Complete","Form Not Yet Complete","Form Not Yet Complete","Form Not Yet Complete","Form Not Yet Complete","Form Not Yet Complete",[{"id":"Form Not Yet Complete","name":"Form Not Yet Complete"}]]
    
    code = str(state)[str(state).find("(")+1:str(state).find(")")]
    state_data = dv.loc[(dv['state'] == code) & (dv['timeWeeks'] <= 14)]
    state_data.dropna(subset=['positive', 'totalTestsViral'],inplace=True)
    positives = np.sum(state_data['positive'].to_numpy())
    totalTests = np.sum(state_data['totalTestsViral'].to_numpy())
    state_stat = str(np.round(100 * (positives/totalTests) / 14,2)) + "%"
    #calc doesnt make sense really

    fip_data = master.loc[master['COUNTY'] == county]
    fip = fip_data["FIPS"].values[0]
    always_data = master.loc[master['COUNTYFP'] == fip]
    always = always_data["ALWAYS"].values[0]
    if always >= 0.8:
        county_stat = "Low Community Spread"
    elif always >=0.5 and always < 0.8:
        county_stat = "Risk of Community Spread"
    elif always < 0.5:
        county_stat = "Risk of Pronounced Community Spread"
    else:
        county_stat = "Invalid Data"

    weighted_sum = 0
    activities = [takeout,walk,lib,eatOut,walkTown,BBQ,beach,mall,grandpa,pool,barber,eatIn,plane,buffet,gym,bar]
    weights = master["weightedRisk"]
    weights.dropna(inplace=True)
    weights = weights.values
    for i in range(0,len(activities)):
        weighted_sum += activities[i] * weights[i]
    behaviour_stat = str(np.round(weighted_sum / np.sum(activities),2))
    behaviour_stat += "%"
    #divide by which sum?
    	
    race_data = master.loc[master['RACE'] == race]
    mortality_stat = race_data['mortRateRace'].values[0]
    infection_stat = race_data['infRateRace'].values[0]

    age_data = master['age group (years)'].values
    for i in range(0,len(age_data)):
        if "-" in str(age_data[i]):
            num = age_data[i].strip().split("-")
            fnum = int(num[0])
            snum = int(num[1])
            if(age >= fnum and age < snum):
                break
        else:
            num = int(age_data[i].strip())
            if age > num:
                break
    age_stat = master['mortality rate'].values[i]

    sex_data = master.loc[master['sex'] == sex]
    sex_stat = sex_data["mortRateSex"].values[0]

    med_data = master[master['prexistingCond'].isin(med)]
    med_stat = med_data[['prexistingCond','mortRatePC']]
    med_stat.columns = ['Comorbidity', 'Mortality Note Associated']

    return([state_stat,
            county_stat,
            behaviour_stat,
            mortality_stat,
            infection_stat,
            age_stat,
            sex_stat,
            med_stat.to_dict('records'), [{'id': c, 'name': c} for c in med_stat.columns]])

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
    cl = dv[(dv['timeWeeks'] >= ga[0]) & (dv['timeWeeks'] <= ga[1])]
    
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

            x_new = np.linspace(x[0], x[-1], 1000)
            y_res = f(x)
            y_new = f(x_new)

            f_new = []
            for num in f:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))

            if order == 1:
                equation = "y = " + str(f_new[1]) + "x + " + str(f_new[0])
                residuals = y- y_res
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((y-np.mean(y))**2)
                r_squared = str(np.round(1 - (ss_res / ss_tot),3))

            elif order == 2:
                equation = "y = " + str(f_new[2]) + "x² + " + str(f_new[1]) + "x + " + str(f_new[0])
                r_squared = "Non-Linear"
            elif order == 3:
                equation = "y = " + str(f_new[3]) + "x³ + " + str(f_new[2]) + "x² + " + str(f_new[1]) + "x + " + str(f_new[0])
                r_squared = "Non-Linear"

            trace = go.Scattergl(x = x_new, y = y_new,
            hovertext= "State: " + i
            + "<br />" + equation
            + "<br />R Squared: " + r_squared,
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=i)

            data.append(trace)

        if('Log-Fit' in fit):
            if('Scatter' in fit or "Poly-Fit" in fit):
                showLegend = False
            else:
                showLegend = True

            def logarithmic(x, a, b, c):
                return  a * np.log(b * x) + c
            
            popt, _ = curve_fit(logarithmic, x, y, maxfev = 999999999)

            x_new = np.linspace(x[0], x[-1], 1000)
            y_new = logarithmic(x_new, *popt)

            f_new = []
            for num in popt:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))

            trace = go.Scattergl(x = x_new, y = y_new,
            hovertext= "State: " + i
            + "<br />y = " + str(f_new[0]) + " * log(" + str(f_new[1]) + " * x) + " + str(f_new[2]),
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=i)

            data.append(trace)

        if('Exp-Fit' in fit):
            if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit):
                showLegend = False
            else:
                showLegend = True

            def exponential(x, a, b, c):
                return a * np.exp(-b * x) + c
            
            popt, _ = curve_fit(exponential, x, y, p0=(1, 1e-6, 1), maxfev = 999999999)

            x_new = np.linspace(x[0], x[-1], 1000)
            y_new = exponential(x_new, *popt)

            f_new = []
            for num in popt:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))

            trace = go.Scattergl(x = x_new, y = y_new,
            hovertext= "State: " + i
            + "<br />y = " + str(f_new[0]) + " * e^(" + str(f_new[1]) + " * x) + " + str(f_new[2]),
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=i)

            data.append(trace)

        if('Power-Fit' in fit):
            if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit or "Exp-Fit" in fit):
                showLegend = False
            else:
                showLegend = True

            def power(x, a, N, b):
                return a * np.power(x,N) + b
            
            popt, _ = curve_fit(power, x, y, maxfev = 999999999)

            x_new = np.linspace(x[0], x[-1], 1000)
            y_new = power(x_new, *popt)

            f_new = []
            for num in popt:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))
            
            trace = go.Scattergl(x = x_new, y = y_new,
            hovertext= "State: " + i
            + "<br />y = " + str(f_new[0]) + " * x^(" + str(f_new[1]) + ") + " + str(f_new[2]),
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=i)

            data.append(trace)

    cleaned.dropna(subset=[selected_x, selected_y],axis="rows", inplace=True)
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

    cl = dv[(dv['timeWeeks'] >= ga[0]) & (dv['timeWeeks'] <= ga[1])]

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

            x_new = np.linspace(x[0], x[-1], 1000)
            y_res = f(x)
            y_new = f(x_new)

            f_new = []
            for num in f:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))

            if order == 1:
                equation = "y = " + str(f_new[1]) + "x + " + str(f_new[0])
                residuals = y- y_res
                ss_res = np.sum(residuals**2)
                ss_tot = np.sum((y-np.mean(y))**2)
                r_squared = str(np.round(1 - (ss_res / ss_tot),3))

            elif order == 2:
                equation = "y = " + str(f_new[2]) + "x² + " + str(f_new[1]) + "x + " + str(f_new[0])
                r_squared = "Non-Linear"
            elif order == 3:
                equation = "y = " + str(f_new[3]) + "x³ + " + str(f_new[2]) + "x² + " + str(f_new[1]) + "x + " + str(f_new[0])
                r_squared = "Non-Linear"

            trace = go.Scattergl(x = x_new, y = y_new,
            hovertext= "State: " + i
            + "<br />" + equation
            + "<br />R Squared: " + r_squared,
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=i)

            data.append(trace)

        if('Log-Fit' in fit):
            if('Scatter' in fit or "Poly-Fit" in fit):
                showLegend = False
            else:
                showLegend = True

            def logarithmic(x, a, b, c):
                return  a * np.log(b * x) + c
            
            popt, _ = curve_fit(logarithmic, x, y, maxfev = 999999999)

            x_new = np.linspace(x[0], x[-1], 1000)
            y_new = logarithmic(x_new, *popt)

            f_new = []
            for num in popt:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))

            trace = go.Scattergl(x = x_new, y = y_new,
            hovertext= "State: " + i
            + "<br />y = " + str(f_new[0]) + " * log(" + str(f_new[1]) + " * x) + " + str(f_new[2]),
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=i)

            data.append(trace)

        if('Exp-Fit' in fit):
            if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit):
                showLegend = False
            else:
                showLegend = True

            def exponential(x, a, b, c):
                return a * np.exp(-b * x) + c
            
            popt, _ = curve_fit(exponential, x, y, p0=(1, 1e-6, 1), maxfev = 999999999)

            x_new = np.linspace(x[0], x[-1], 1000)
            y_new = exponential(x_new, *popt)

            f_new = []
            for num in popt:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))

            trace = go.Scattergl(x = x_new, y = y_new,
            hovertext= "State: " + i
            + "<br />y = " + str(f_new[0]) + " * e^(" + str(f_new[1]) + " * x) + " + str(f_new[2]),
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=i)

            data.append(trace)

        if('Power-Fit' in fit):
            if('Scatter' in fit or "Poly-Fit" in fit or "Log-Fit" in fit or "Exp-Fit" in fit):
                showLegend = False
            else:
                showLegend = True

            def power(x, a, N, b):
                return a * np.power(x,N) + b
            
            popt, _ = curve_fit(power, x, y, maxfev = 999999999)

            x_new = np.linspace(x[0], x[-1], 1000)
            y_new = power(x_new, *popt)

            f_new = []
            for num in popt:
                if np.absolute(num) < 10**(1/4) or np.absolute(num) > np.power(10,3):
                    f_new.append(format(num,'.3e'))
                else:
                    f_new.append(np.round(num,3))
            
            trace = go.Scattergl(x = x_new, y = y_new,
            hovertext= "State: " + i
            + "<br />y = " + str(f_new[0]) + " * x^(" + str(f_new[1]) + ") + " + str(f_new[2]),
            hoverinfo='text',mode='lines', line={'color' : name_array.Color.values[0]},
            name=i,showlegend=showLegend,legendgroup=i)

            data.append(trace)

    cleaned.dropna(subset=[selected_x, selected_y],axis="rows", inplace=True)
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