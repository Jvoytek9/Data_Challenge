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

from initialize_data import Return_Data, master, abbreviations, intervals

dv = Return_Data()

state_codes = dv["abbr"].values

Graph_Height = 605

graphs_html = dbc.Row([
    dbc.Col([
        html.Div([html.H1("Kassandra Database")],
            style={'text-align':"center", "margin-right":"auto","margin-left":"auto", 'color':"white","width": "80%","padding-top":"20%"}),

        html.Div([
            html.Div([html.H1("Graph 2")],style={'text-align':"center", "margin-left":"auto","margin-right":"auto", 'color':"white"}),
            dbc.Row([
                dbc.Col(html.H6("X: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-xaxis2", placeholder = "Select x-axis", value = "Weeks Elapsed",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[4:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),

            dbc.Row([
                dbc.Col(html.H6("Y: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-yaxis2", placeholder = "Select y-axis", value = "New Deaths",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[4:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),

            html.Div([
                dbc.Row([
                    dcc.RadioItems(
                        id='toggle2',
                        options=[{'label': i, 'value': i} for i in ['Show Less','Show More']],
                        value='Show Less',
                        labelStyle={"padding-right":"10px","margin":"auto"},
                        style={"text-align":"center","margin":"auto"}
                    ),
                ],style={'text-align':"center","margin-left": "auto", "margin-right": "auto"}),

                html.Div(id='controls-container2', children=[

                html.Hr(),

                html.H5("Configurations:"),

                html.Hr(),

                html.Details([
                    html.Summary("Data Formatting"),
                    html.Div(
                        dcc.Checklist(
                            id='normalize2',
                            options=[{'label': i, 'value': i} for i in ['Normalize X','Normalize Y','Aggregate Y']],
                            value=[],
                            labelStyle={"padding-right":"10px","margin":"auto","padding-bottom":"10px"}
                        )
                    ,style={"margin":"auto"})
                ]),

                html.Hr(),

                html.Details([
                    html.Summary("Data Fitting"),
                    html.Div(
                        dcc.Checklist(
                            id = 'bestfit2',
                            options= [{'label': i, 'value': i} for i in ['Scatter','Line','Poly-Fit','Log-Fit','Exp-Fit',"Power-Fit"]],
                            value = ['Scatter',"Line"],
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
                    ])
                ]),

                html.Hr(),

                html.H5("Filter By:"),

                html.Hr(),

                html.Details([
                    html.Summary("Time-Elapsed(Weeks)"),

                    html.Div([
                        html.Div([
                            html.P(id = "dates_used2",
                            children=["init"])
                        ],style={"text-decoration": "underline","font-style": "italic"}),

                        dcc.RangeSlider(
                            id="datePicker2",
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
                            dbc.Button('Select All', id='selectAllStates2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='removeAllStates2', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'selectStates2',
                        options= [{'label': state, 'value': state} for state in np.sort(np.unique(dv["State/Territory/Federal Entity"] + "(" + state_codes + ")"))],
                        value = np.unique(dv["State/Territory/Federal Entity"] + "(" + state_codes + ")"),
                        labelStyle={'display': 'block'}
                    ),
                ]),

                html.Hr(),

                ],style={"display":"none"}),
            ],style={"text-align":"center", "margin-left": "auto", "margin-right": "auto", "width": "80%", "backgroundColor": 'white', "border-radius":3,"position":"relative"}),
        ],id="compare_dropdown",style={"display":"None"}),

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
                html.Div(dcc.Dropdown(id="select-xaxis", placeholder = "Select x-axis", value = "Weeks Elapsed",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[4:-1]], clearable=False),
                style={"width":"90%","border":"1px solid white"}),
            ],style={"background-color":"white","border-radius":"3px","border":"1px solid #cccccc","margin-left": "auto", "margin-right": "auto", "width": "80%","height":"10%"},no_gutters=True),

            dbc.Row([
                dbc.Col(html.H6("Y: "),style={"margin":"auto","width":"10%","height":"100%"}),
                html.Div(dcc.Dropdown(id="select-yaxis", placeholder = "Select y-axis", value = "New Cases",
                options=[{'label': i.title(), 'value': i} for i in dv.columns[4:-1]], clearable=False),
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

                    html.H5("Configurations:"),

                    html.Hr(),

                    html.Details([
                        html.Summary("Data Formatting"),
                        html.Div(
                            dcc.Checklist(
                                id='normalize',
                                options=[{'label': i, 'value': i} for i in ['Normalize X','Normalize Y','Aggregate Y']],
                                value=[],
                                labelStyle={"padding-right":"10px","margin":"auto","padding-bottom":"10px"}
                            )
                        ,style={"margin":"auto"})
                    ]),

                    html.Hr(),

                    html.Details([
                        html.Summary("Data Fitting"),
                        html.Div(
                            dcc.Checklist(
                                id = 'bestfit',
                                options= [{'label': i, 'value': i} for i in ['Scatter','Line','Poly-Fit','Log-Fit','Exp-Fit',"Power-Fit"]],
                                value = ['Scatter',"Line"],
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
                        ])
                    ]),

                html.Hr(),

                html.H5("Filter By:"),

                html.Hr(),
                
                html.Details([
                    html.Summary("Time-Elapsed(Weeks)"),

                    html.Div([
                        html.Div([
                            html.P(id = "dates_used",
                            children=["init"])
                        ],style={"text-decoration": "underline","font-style": "italic"}),

                        dcc.RangeSlider(
                            id="datePicker",
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
                            dbc.Button('Select All', id='selectAllStates', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-right":"5px"}),

                        dbc.Col(
                            dbc.Button('Deselect All', id='removeAllStates', n_clicks=0,size="sm",block=True,outline=True,color="dark")
                        ,style={"padding-left":"5px"}),
                    ],style={"margin":"auto","padding-top":"10px","padding-left":"10px","padding-right":"10px"},no_gutters=True),

                    dcc.Checklist(
                        id = 'selectStates',
                        options= [{'label': state, 'value': state} for state in np.sort(np.unique(dv["State/Territory/Federal Entity"] + "(" + state_codes + ")"))],
                        value = np.unique(dv["State/Territory/Federal Entity"] + "(" + state_codes + ")"),
                        labelStyle={'display': 'block'}
                    ),
                ]),

                html.Hr(),

                ],style={"display":"none"}),
            ],style={"text-align":"center", "margin-left": "auto", "margin-right": "auto", "width": "80%", "backgroundColor": 'white', "border-radius":3,"position":"relative"}),
        ],style={'text-align':"center","margin-left": "auto", "margin-right": "auto", "width": "100%"}),

        dcc.Link('Calculator', href='/',style={'position':'absolute','top':0, 'left':0,"padding":5,"color":"white","font-size":18})
    ],style={'backgroundColor': '#9E1B34'}),

    dbc.Col([
        dcc.Tabs(id="tabs", children=[
            dcc.Tab(label='2-Dimensions', children=[
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            dcc.Graph(id="comp1_2D_graph",
                            config = {'toImageButtonOptions':
                            {'width': None,
                            'height': None,
                            'format': 'png',
                            'filename': '2D_Plot_Comp1'}
                            })
                        ]),

                        html.Div(
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
                            )
                        ,style={"width":"95%","margin":"auto"})
                    ]),

                    dbc.Col([
                        html.Div([
                            dcc.Graph(id="comp2_2D_graph",
                                config = {'toImageButtonOptions':
                                {'width': None,
                                'height': None,
                                'format': 'png',
                                'filename': '2D_Plot_Comp2'}
                            })
                        ]),

                        html.Div(
                            dt.DataTable(
                                id='comp2_2D_table',
                                page_current=0,
                                page_size=75,
                                columns=[{'id': c, 'name': c} for c in dv.columns[1:-1]],
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
                        ,style={"width":"95%","margin":"auto"})
                    ],id="compare_graph_table_2D",style={"display":"None"})
                ],no_gutters=True),
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
        [Output('selectStates', 'value')],
        [Input('selectAllStates', 'n_clicks'),
        Input('removeAllStates', 'n_clicks')],
        [State('selectStates', 'value'),
        State('selectStates', 'options')]
    )
    def select_deselect_all_surfactants(selectAllStates,removeAllStates,state_values,state_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'selectAllStates.n_clicks':
            return([[value['value'] for value in state_options]])
        elif changed_id == 'removeAllStates.n_clicks':
            return([[]])
        else:
            return([state_values])

    @app.callback(
        [Output('selectStates2', 'value')],
        [Input('selectAllStates2', 'n_clicks'),
        Input('removeAllStates2', 'n_clicks')],
        [State('selectStates2', 'value'),
        State('selectStates2', 'options')]
    )
    def select_deselect_all_states2(selectAllStates,removeAllStates,state_values,state_options):
        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if changed_id == 'selectAllStates2.n_clicks':
            return([[value['value'] for value in state_options]])
        elif changed_id == 'removeAllStates2.n_clicks':
            return([[]])
        else:
            return([state_values])


    @app.callback(
        [Output('compare_dropdown', 'style'),
        Output('compare_graph_table_2D', 'style'),
        Output('toggle2', 'style')],
        [Input('addComp', 'value')])
    def toggle_compare_container(compare_value):
        if compare_value == 'Compare':
            return [{'display': 'block',"position":"absolute","top":"50%","margin-right":"auto","margin-left":"auto","width":"100%","text-align":"center"},
                    {'display': 'block'},
                    {"text-align":"center","margin":"auto","backgroundColor": 'white', "border-radius":3,"width":"80%"}]
        else:
            return [{'display': 'none'},
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
        [Output("dates_used", "children"),
        Output("comp1_2D_graph", "figure"),
        Output("comp1_2D_table", "data"),
        Output("comp1_2D_table", "columns")],
        [Input("select-xaxis", "value"),
        Input("select-yaxis", "value"),
        Input('addComp', 'value'),
        Input('datePicker', 'value'),
        Input('normalize', 'value'),
        Input("bestfit", "value"),
        Input("input_fit", "value"),
        Input('selectStates', 'value')],
    )
    def update_comp1_2D(selected_x, selected_y, comp, date_range, normalize, fit, order, selected_states):
        time_sorted = dv[(dv['Weeks Elapsed'] >= date_range[0]) & (dv['Weeks Elapsed'] <= date_range[1])]
        codes = []
        for element in selected_states:
            code = element[element.find("(")+1:element.find(")")]
            codes.append(code)
        cleaned = time_sorted[time_sorted.abbr.isin(codes)]

        if(cleaned["date"].empty):
            dates_used = "No Data"
        else:
            dates_used = str(cleaned["date"].iat[0]) + " ↔ " + str(cleaned["date"].iat[-1])

        data = []
        for i in abbreviations:
            name_array = cleaned[cleaned.abbr == i]

            if len(name_array[selected_x].values) > 2 and len(name_array[selected_y].values) > 2 and not (name_array[selected_x] == 0).all() and not (name_array[selected_y] == 0).all():
                
                name_array = name_array.dropna(subset=[selected_x, selected_y],axis="rows")
                name_array.reset_index(drop=True)
                name_array.sort_values(by=selected_x, inplace=True)

                if('Aggregate Y' in normalize):
                    #namearray find all x repeats, take the average of the associated y values, replace y values with average and remove all repeats but first
                    cats = np.unique(name_array[selected_x].values)
                    for j in cats:
                        rows_cat = name_array[name_array[selected_x] == j]
                        first_row = rows_cat.iloc[[0],:]

                        avg = rows_cat[selected_y].mean()
                        first_row[selected_y] = avg

                        name_array = name_array[name_array[selected_x] != j]
                        name_array = name_array.append(first_row,ignore_index=True)

                if len(name_array[selected_x]) >= 1:
                    x = np.array(name_array[selected_x])
                    y = np.array(name_array[selected_y])
                    if "Normalize X" in normalize:
                        if max(x) == min(x):
                            continue
                        else:
                            x = (x-min(x))/(max(x)-min(x))
                        x[x == 0] = 0.001

                    if "Normalize Y" in normalize:
                        if max(y) == min(y):
                            continue
                        else:
                            y = (y-min(y))/(max(y)-min(y))
                        y[y == 0] = 0.001
                else:
                    continue
            else:
                continue

            if('Scatter' in fit):
                if('Line' in fit):
                    trace = go.Scattergl(x=x,y=y,
                    hovertemplate= "Date Recorded: " + name_array.date
                    + "<br />State: " + name_array["State/Territory/Federal Entity"],
                    mode='lines+markers', line={'color' : name_array.Color.values[0]}, marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
                    name=i,legendgroup=i)

                else:
                    trace = go.Scattergl(x=x,y=y,
                    hovertemplate= "Date Recorded: " + name_array.date
                    + "<br />State: " + name_array["State/Territory/Federal Entity"],
                    mode='markers', marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
                    name=i,legendgroup=i)

            elif('Line' in fit):
                trace = go.Scattergl(x=x,y=y,
                hovertemplate= "Date Recorded: " + name_array.date
                + "<br />State: " + name_array["State/Territory/Federal Entity"],
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,legendgroup=i)

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
        cleaned = cleaned[["date","State/Territory/Federal Entity",selected_x,selected_y]]

        return [dates_used,
        {
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
            height=Graph_Height)
        },cleaned.to_dict('records'), [{'id': c, 'name': c} for c in cleaned.columns]]

    @app.callback(
        [Output("dates_used2", "children"),
        Output("comp2_2D_graph", "figure"),
        Output("comp2_2D_table", "data"),
        Output("comp2_2D_table", "columns")],
        [Input("select-xaxis2", "value"),
        Input("select-yaxis2", "value"),
        Input('addComp', 'value'),
        Input('datePicker2', 'value'),
        Input('normalize2', 'value'),
        Input("bestfit2", "value"),
        Input("input_fit2", "value"),
        Input('selectStates2', 'value')],
    )
    def update_comp2_2D(selected_x, selected_y, comp, date_range, normalize, fit, order, selected_states):
        if comp == "No Compare":
            return ["No Data",{},[],[]]

        time_sorted = dv[(dv['Weeks Elapsed'] >= date_range[0]) & (dv['Weeks Elapsed'] <= date_range[1])]

        codes = []
        for element in selected_states:
            code = element[element.find("(")+1:element.find(")")]
            codes.append(code)
        cleaned = time_sorted[time_sorted.abbr.isin(codes)]

        if(cleaned.empty):
            dates_used = "No Data"
            return ["No Data",{},[],[]]
        else:
            dates_used = str(cleaned["date"].iat[0]) + " ↔ " + str(cleaned["date"].iat[-1])

        data = []
        for i in abbreviations:
            name_array = cleaned[cleaned.abbr == i]

            if len(name_array[selected_x].values) > 2 and len(name_array[selected_y].values) > 2 and not (name_array[selected_x] == 0).all() and not (name_array[selected_y] == 0).all():
                
                name_array = name_array.dropna(subset=[selected_x, selected_y],axis="rows")
                name_array.reset_index(drop=True)
                name_array.sort_values(by=selected_x, inplace=True)

                if('Aggregate Y' in normalize):
                    cats = np.unique(name_array[selected_x].values)
                    for j in cats:
                        rows_cat = name_array[name_array[selected_x] == j]
                        first_row = rows_cat.iloc[[0],:]

                        avg = rows_cat[selected_y].mean()
                        first_row[selected_y] = avg

                        name_array = name_array[name_array[selected_x] != j]
                        name_array = name_array.append(first_row,ignore_index=True)

                if len(name_array[selected_x]) >= 1:
                    x = np.array(name_array[selected_x])
                    y = np.array(name_array[selected_y])
                    if "Normalize X" in normalize:
                        if max(x) == min(x):
                            continue
                        else:
                            x = (x-min(x))/(max(x)-min(x))
                        x[x == 0] = 0.001

                    if "Normalize Y" in normalize:
                        if max(y) == min(y):
                            continue
                        else:
                            y = (y-min(y))/(max(y)-min(y))
                        y[y == 0] = 0.001
                else:
                    continue
            else:
                continue

            if('Scatter' in fit):
                if('Line' in fit):
                    trace = go.Scattergl(x=x,y=y,
                    hovertemplate= "Date Recorded: " + name_array.date
                    + "<br />State: " + name_array["State/Territory/Federal Entity"],
                    mode='lines+markers', line={'color' : name_array.Color.values[0]}, marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
                    name=i,legendgroup=i)

                else:
                    trace = go.Scattergl(x=x,y=y,
                    hovertemplate= "Date Recorded: " + name_array.date
                    + "<br />State: " + name_array["State/Territory/Federal Entity"],
                    mode='markers', marker={'size': 10, 'opacity': 0.8, 'color' : name_array.Color},
                    name=i,legendgroup=i)

            elif('Line' in fit):
                trace = go.Scattergl(x=x,y=y,
                hovertemplate= "Date Recorded: " + name_array.date
                + "<br />State: " + name_array["State/Territory/Federal Entity"],
                mode='lines', line={'color' : name_array.Color.values[0]},
                name=i,legendgroup=i)

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
        cleaned = cleaned[["date","State/Territory/Federal Entity",selected_x,selected_y]]

        return [dates_used,
        {
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
                height=Graph_Height)
        },cleaned.to_dict('records'), [{'id': c, 'name': c} for c in cleaned.columns]]

def Create_Graphs():
    return graphs_html