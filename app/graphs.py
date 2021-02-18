import numpy as np
from scipy.optimize import curve_fit
import pandas as pd
np.warnings.filterwarnings('ignore')
#pylint: disable=unbalanced-tuple-unpacking
#pylint: disable=unused-variable

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
import plotly.graph_objs as go

from initialize_data import Return_Data, intervals, master, state_codes, names

dv = Return_Data()

Graph_Height = 605

graphs_html = dbc.Row([
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
                            id='normalize2',
                            options=[{'label': i, 'value': i} for i in ['Normalize X','Normalize Y']],
                            value=[],
                            labelStyle={"padding-right":"10px","margin":"auto","padding-bottom":"10px"}
                        )
                    ,style={"margin":"auto"}),

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

                ],style={"display":"none"}),
            ],style={"text-align":"center", "margin-left": "auto", "margin-right": "auto", "width": "80%", "backgroundColor": 'white', "border-radius":3,"position":"relative"}),


        ],id="compare_dropdown",style={"display":"None"}),

        html.Div([html.H1("Data Challenge")],
            style={'text-align':"center", "margin-right":"auto","margin-left":"auto", 'color':"white","width": "80%","padding-top":"15%"}),

        html.Div([
            html.Div(
                dcc.RadioItems(
                    id='addComp',
                    options=[{'label': i, 'value': i} for i in ['No Compare','Compare']],
                    value='No Compare',
                    labelStyle={"padding-right":"10px","margin":"auto","padding-bottom":"10px","color":"white"}
                )
            ,style={"margin":"auto"}),

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
                        dcc.Checklist(
                            id='normalize',
                            options=[{'label': i, 'value': i} for i in ['Normalize X','Normalize Y']],
                            value=[],
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

                ],style={"display":"none"}),
            ],style={"text-align":"center", "margin-left": "auto", "margin-right": "auto", "width": "80%", "backgroundColor": 'white', "border-radius":3,"position":"relative"}),

        ],style={'text-align':"center","margin-left": "auto", "margin-right": "auto", "width": "100%"}),

        dcc.Link('Calculator', href='/',style={'position':'absolute','top':0, 'left':0,"padding":5,"color":"white","font-size":18})

    ],style={'backgroundColor': '#9E1B34','width':'20%'}),

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
                    ,style={"width":"50%"}),

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
                    ,id="compare_graph_2D",style={"display":"None","width":"50%"})
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
                        ),style={"padding-left":20,"padding-right":20,"width":"50%"}
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
                    ,style={"display":"None","width":"50%"},id="compare_table_2D")
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
    ],width=10)
],no_gutters=True,style={"height":"100vh"})

def register_graphs_callbacks(app):
        
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
        Input('normalize', 'value'),
        Input("bestfit", "value"),
        Input("input_fit", "value"),
        Input('gasses', 'value'),
        Input('surfactants', 'value')],
    )
    def update_comp1_2D(selected_x, selected_y, comp, normalize, fit, order, ga, sur):
        cl = dv[(dv['timeWeeks'] >= ga[0]) & (dv['timeWeeks'] <= ga[1])]

        codes = []
        for element in sur:
            code = element[element.find("(")+1:element.find(")")]
            codes.append(code)
        cleaned = cl[cl["state"].isin(codes)]

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
                    if "Normalize X" in normalize:
                        if max(x) == min(x):
                            x = np.full_like(x, 0.5)
                        else:
                            x = (x-min(x))/(max(x)-min(x))
                        x[x == 0] = 0.001

                    if "Normalize Y" in normalize:
                        if max(y) == min(y):
                            y = np.full_like(y, 0.5)
                        else:
                            y = (y-min(y))/(max(y)-min(y))
                        y[y == 0] = 0.001
                else:
                    continue
            else:
                continue

            if('Scatter' in fit):
                trace = go.Scattergl(x=x,y=y,
                hovertext= "Date Recorded: " + name_array.date
                + "<br />State: " + i,
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
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                if order == 1:
                    equation = "y = {a}x + {b}".format(a=f_new[0],b=f_new[1])
                    residuals = y- y_res
                    ss_res = np.sum(residuals**2)
                    ss_tot = np.sum((y-np.mean(y))**2)
                    r_squared = str(np.round(1 - (ss_res / ss_tot),3))

                elif order == 2:
                    equation = "y = {a}x² + {b}x + {c}".format(a=f_new[0],b=f_new[1],c=f_new[2])
                    r_squared = "Non-Linear"
                elif order == 3:
                    equation = "y = {a}x³ + {b}x² + {c}x + {d}".format(a=f_new[0],b=f_new[1],c=f_new[2],d=f_new[3])
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
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertext= "State: " + i
                + "<br />" +
                "y = {a} * log({b} * x) + {c}".format(a=f_new[0],b=f_new[1],c=f_new[2]),
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
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertext= "State: " + i
                + "<br />" +
                "y = {a} * e<sup>({b} * x)</sup> + {c}".format(a=f_new[0],b=f_new[1],c=f_new[2]),
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
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertext= "State: " + i
                + "<br />" +
                "y = {a} * x<sup>{N}</sup> + {c}".format(a=f_new[0],N=f_new[1],c=f_new[2]),
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
        Input('normalize2', 'value'),
        Input("bestfit2", "value"),
        Input("input_fit2", "value"),
        Input('gasses2', 'value'),
        Input('surfactants2', 'value')],
    )
    def update_comp2_2D(selected_x, selected_y, comp, normalize, fit, order, ga, sur):
        if comp == "No Compare":
            return [{},[],[]]

        cl = dv[(dv['timeWeeks'] >= ga[0]) & (dv['timeWeeks'] <= ga[1])]

        codes = []
        for element in sur:
            code = element[element.find("(")+1:element.find(")")]
            codes.append(code)
        cleaned = cl[cl["state"].isin(codes)]

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
                    if "Normalize X" in normalize:
                        if max(x) == min(x):
                            x = np.full_like(x, 0.5)
                        else:
                            x = (x-min(x))/(max(x)-min(x))
                        x[x == 0] = 0.001

                    if "Normalize Y" in normalize:
                        if max(y) == min(y):
                            y = np.full_like(y, 0.5)
                        else:
                            y = (y-min(y))/(max(y)-min(y))
                        y[y == 0] = 0.001
                else:
                    continue
            else:
                continue

            if('Scatter' in fit):
                trace = go.Scattergl(x=x,y=y,
                hovertext= "Date Recorded: " + name_array.date
                + "<br />State: " + i,
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
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                if order == 1:
                    equation = "y = {a}x + {b}".format(a=f_new[0],b=f_new[1])
                    residuals = y- y_res
                    ss_res = np.sum(residuals**2)
                    ss_tot = np.sum((y-np.mean(y))**2)
                    r_squared = str(np.round(1 - (ss_res / ss_tot),3))

                elif order == 2:
                    equation = "y = {a}x² + {b}x + {c}".format(a=f_new[0],b=f_new[1],c=f_new[2])
                    r_squared = "Non-Linear"
                elif order == 3:
                    equation = "y = {a}x³ + {b}x² + {c}x + {d}".format(a=f_new[0],b=f_new[1],c=f_new[2],d=f_new[3])
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
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertext= "State: " + i
                + "<br />" +
                "y = {a} * log({b} * x) + {c}".format(a=f_new[0],b=f_new[1],c=f_new[2]),
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
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertext= "State: " + i
                + "<br />" +
                "y = {a} * e<sup>({b} * x)</sup> + {c}".format(a=f_new[0],b=f_new[1],c=f_new[2]),
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
                    if np.absolute(num) <= 0.000999 or np.absolute(num) > np.power(10,4):
                        f_new.append(format(num,'.3e'))
                    else:
                        f_new.append(np.round(num,3))

                trace = go.Scattergl(x = x_new, y = y_new,
                hovertext= "State: " + i
                + "<br />" +
                "y = {a} * x<sup>{N}</sup> + {c}".format(a=f_new[0],N=f_new[1],c=f_new[2]),
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

def Create_Graphs():
    return graphs_html