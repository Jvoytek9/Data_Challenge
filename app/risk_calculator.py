from datetime import date, timedelta
import numpy as np
import pandas as pd
np.warnings.filterwarnings('ignore')
#pylint: disable=unused-variable

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dt
import plotly.graph_objs as go

from initialize_data import Return_Data, master

dv = Return_Data()
state_codes = dv["abbr"].values
dv = dv[["date", "State/Territory/Federal Entity","Cases Last 7 Days","Tests Last 7 Days"]]

risk_calculator_html = html.Div([
    dbc.Row([
        dbc.Col(
            dcc.Link('Graphs', href='/graphs',style={'position':'absolute','top':0, 'left':0,"padding":5,"color":"white","font-size":18})
        ,style={'width':'30%'}),
        dbc.Col([
            dcc.Tabs(id="tabs", children=[
                dcc.Tab(label='Risk Calculator', children=[

                    html.Div([
                        html.H3("Risk Calculator",style={"display":"block"}),

                        html.Br(),
                        html.H5("1. Basic Information: ",style={"display":"block"}),

                        dcc.RadioItems(id="sex_input", options=[{'label': i, 'value': i} for i in master["sex"].dropna()],labelStyle={"padding-right":"5px"}),

                        dcc.Input(id="age_input", type="number", placeholder="Enter Age", min=0, debounce=True,style={"text-align":"center","width":"25%"}),

                        dcc.Dropdown(id="race_input", placeholder="Select Race",
                        options= [{'label': i, 'value': i} for i in np.sort(np.unique(master["RACE"].dropna()))]
                        ,style={"width":"50%","margin":"auto"}),

                        dcc.Dropdown(id="state_input", placeholder="Select State",
                        options= [{'label': i, 'value': i} for i in np.sort(np.unique(dv["State/Territory/Federal Entity"] + "(" + state_codes + ")"))]
                        ,style={"width":"50%","margin":"auto"}),

                        dcc.Dropdown(id="county_input", placeholder="Select County",
                        options= [{'label': i, 'value': i} for i in np.sort(np.unique(master["COUNTY"].dropna()))]
                        ,style={"width":"50%","margin":"auto"}),

                        html.Br(),
                        html.Br(),
                        html.P("*The current literature does not provide data for options other than female and male (sex assigned at birth), so there is no data available for intersex. There is also no data available for those who are non-cisgendered."),
                        html.P("**The CDC does not provide data for those of more than one race so please choose one of the races you identify as if you are multiracial."),
                        html.Br(),
                        html.Br(),
                        html.H5("2. Preexisting Conditions: "),
                        html.Br(),

                        dcc.Checklist(id = 'med_input',
                        options= [{'label': sc, 'value': sc} for sc in np.sort(list(dict.fromkeys(master['prexistingCond'].dropna())))] + [{'label': 'None of the above', 'value': 'None of the above'}],
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
                        html.H3("Results:",style={"text-decoration":"underline"}),
                        html.Br(),

                        html.H4("State Percent Positive: ",style={"display":"inline-block"}),
                        dcc.Input(id='state_stat', value='', type='text',style={"display":"inline-block","width":"40%","text-align":"center"},readOnly=True),
                        html.Br(),
                        html.P("This percent positive statistic is the average percentage of all coronavirus tests performed that come back positive in the past 14 days. If the number of total tests remains too low or " +
                        "if the number of positive results remains too high for your state, then the percent positive will be high. " +
                        "A high percent positive value can indicate high transmission within the population or that there are more people with COVID-19 that have not been tested yet.",style={"display":"inline"}),
                        html.Br(),
                        html.Br(),
                        html.P("The World Health Organization (WHO) recommends the percent positive to stay at" ,style={"display":"inline","padding-right":"5px"}),
                        html.A("5% or lower for at least 14 days", href="https://coronavirus.jhu.edu/testing/testing-positivity",style={"display":"inline","padding-right":"5px"}),
                        html.P("before governments consider reopening. If your state has a percent positive higher than 5%, you should take greater precautions by minimizing unessential activities. ",style={"display":"inline","padding-right":"5px"}),
                        html.P("THE COVID TRACKING PROJECT HAS CEASED UPDATING. It says 0 because we are switching databases. Please bear with us!"),
                        html.Br(),

                        html.Br(),
                        html.Br(),
                        html.H4("County Spread Rate: ",style={"display":"inline-block"}),
                        dcc.Input(id='county_stat', value='', type='text',style={"display":"inline","width":"40%","text-align":"center"},readOnly=True),
                        html.Br(),
                        html.P("This statistic is measured by the reported mask usage in your county. This data was retrieved from the",style={"display":"inline","padding-right":"5px"}),
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
                        html.P("***This is a preprint, so it has not been peer-reviewed yet."),

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
                        html.Br(),
                        html.H4("Age Mortality Risk: ",style={"display":"inline-block"}),
                        dcc.Input(id='age_stat', value='', type='text',style={"display":"inline-block","width":"40%","text-align":"center"},readOnly=True),
                        html.Br(),
                        html.P("Age data was retrieved from the",style={"display":"inline","padding-right":"5px"}),
                        html.A("CDC.",href="https://www.cdc.gov/coronavirus/2019-ncov/covid-data/investigations-discovery/hospitalization-death-by-age.html",style={"display":"inline","padding-right":"5px"}),
                        html.P("The CDC used the mortality rate for 5-17 year olds as the comparison group.",style={"display":"inline"}),
                        html.Br(),
                        html.Br(),
                        html.P("The paper,",style={"display":"inline","padding-right":"5px"}),
                        html.A("“Why does COVID-19 disproportionately affect older people?”",href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7288963/",style={"display":"inline"}),
                        html.P(", attributes the disproportionate mortality risk to “molecular differences between young, middle-aged, and older people”.",style={"display":"inline"}),
                        html.Br(),

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

                    ],style={"padding":"30px","text-align":"center"})
                ]),
                dcc.Tab(label='About', children=[
                    html.Div([
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
                                    dbc.CardImg(src="/assets/Maltepes.jpg", top=True,style={"height":"25vh","width":"100%"}),
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
                            html.P("We added a variable, timeWeeks, which is the time-elapsed(units:weeks) from when the COVID track project started recording data to today. All data displayed in this site taken from the Covid Tracking Project.", style={"display":"inline-block"})
                        ],style={"font-size":23,"padding-left":30,"padding-right":30,"text-align":"center"})
                    ],style={'height':'100vh'})
                ])
            ]),
        ],style={"backgroundColor":"white"},width=6),
        dbc.Col(style={'width':'30%'})
    ],style={'backgroundColor': '#9E1B34',"height":"100%"},no_gutters=True)
])

def register_risk_callbacks(app):
    @app.callback(
        Output('county_input', 'options'),
        [Input('state_input', 'value')],
        [State('county_input', 'options')])
    def update_counties(state,county):
        if not state:
            return county

        code = str(state)[str(state).find("(")+1:str(state).find(")")]
        states_data = master.loc[master['STATE'] == code]
        counties = states_data['COUNTY'].dropna()
        options= [{'label': i, 'value': i} for i in np.sort(list(dict.fromkeys(counties)))]
        return options

    options= [{'label': i, 'value': i} for i in np.sort(np.unique(dv["State/Territory/Federal Entity"] + "(" + state_codes + ")"))]

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
        state = str(state)[0:str(state).find("(")]
        state_percents = dv[["date", "State/Territory/Federal Entity", "Cases Last 7 Days", "Tests Last 7 Days"]]
        state_percents = state_percents[state_percents['State/Territory/Federal Entity'] == state].dropna().reset_index(drop=True)
        
        one_week_ago = date.today() - timedelta(weeks=1)
        formatted_one_week = one_week_ago.strftime("%Y-%m-%d")
        
        if(state_percents['date'].empty):
            state_stat = "Not enough data"
        else:
            if state_percents['date'].str.contains(formatted_one_week).any():
                state_stat = ((state_percents["Cases Last 7 Days"].iat[-1] + state_percents[state_percents["date"] == formatted_one_week]["Cases Last 7 Days"].iat[-1]) / 2) / ((state_percents["Tests Last 7 Days"].iat[-1] + state_percents[state_percents["date"] == formatted_one_week]["Tests Last 7 Days"].iat[-1]) / 2)
                state_stat = str(np.round(state_stat * 100,2)) + "%"
            else:
                formatted_one_week = min(pd.to_datetime(state_percents['date']), key=lambda x: abs(x - pd.to_datetime(one_week_ago))).strftime("%Y-%m-%d")
                state_stat = ((state_percents["Cases Last 7 Days"].iat[-1] + state_percents[state_percents["date"] == formatted_one_week]["Cases Last 7 Days"].iat[-1]) / 2) / ((state_percents["Tests Last 7 Days"].iat[-1] + state_percents[state_percents["date"] == formatted_one_week]["Tests Last 7 Days"].iat[-1]) / 2)
                state_stat = str(np.round(state_stat * 100,2)) + "%"

        fip_data = master.loc[master['COUNTY'] == county]
        if fip_data.empty:
            county_stat = "Not enough data"
        else:
            fip = fip_data["FIPS"].values[0]
            always_data = master.loc[master['COUNTYFP'] == fip]
            always = always_data["ALWAYS"].values[0]
            if always >= 0.8:
                county_stat = "lower risk of community spread"
            elif always >=0.5 and always < 0.8:
                county_stat = "higher risk of community spread"
            elif always < 0.5:
                county_stat = "most pronounced community spread"
            else:
                county_stat = "Invalid Data"

        weighted_sum = 0
        activities = np.array([takeout,walk,lib,eatOut,walkTown,BBQ,beach,mall,grandpa,pool,barber,eatIn,plane,buffet,gym,bar])
        if not activities.any():
            behaviour_stat = "Not enough data"
        else:
            weights = master["weightedRisk"]
            weights.dropna(inplace=True)
            weights = weights.values
            for i in range(0,len(activities)):
                weighted_sum += activities[i] * weights[i]
            behaviour = np.round(weighted_sum / np.sum(weights),2)
            interval_data = master["weightedAvgInteveral"]
            interval_data.dropna(inplace=True)
            interval_data = interval_data.values
            for i in range(0,len(interval_data)):
                ranges = str(interval_data[i]).strip().split(">")
                low = float(ranges[0])
                high = float(ranges[1])
                if behaviour >= low and behaviour < high:
                    break
            behaviour_stat = str(master["riskString"].values[i])

        race_data = master.loc[master['RACE'] == race]
        if race_data['mortRateRace'].empty:
            mortality_stat = "Not enough data"
        else:
            mortality_stat = race_data['mortRateRace'].values[0]

        if race_data['infRateRace'].empty:
            infection_stat = "Not enough data"
        else:
            infection_stat = race_data['infRateRace'].values[0]

        age_data = master['age group (years)']
        if age is None:
            age_stat = "Not enough data"
        else:
            for i in range(0,len(age_data.values)):
                if ">" in str(age_data[i]):
                    num = age_data[i].strip().split(">")
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
        if sex_data.empty:
            sex_stat = "Not enough data"
        else:
            sex_stat = sex_data["mortRateSex"].values[0]

        if med is None:
            med_stat = pd.DataFrame(columns = ['Comorbidity', 'Mortality Risk Note Associated'])
        else:    
            med_data = master[master['prexistingCond'].isin(med)]
            med_stat = med_data[['prexistingCond','mortRatePC']]
            med_stat.columns = ['Comorbidity', 'Mortality Risk Note Associated']

        return([state_stat,
                county_stat,
                behaviour_stat,
                mortality_stat,
                infection_stat,
                age_stat,
                sex_stat,
                med_stat.to_dict('records'), [{'id': c, 'name': c} for c in med_stat.columns]])

def Create_Calculator():
    return risk_calculator_html