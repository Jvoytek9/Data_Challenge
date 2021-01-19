import os
from datetime import date
import math
import numpy as np
import pandas as pd
np.warnings.filterwarnings('ignore')
from color import color
#pylint: disable=unused-variable

basedir = os.path.abspath(os.path.dirname(__file__))

state_codes = pd.read_csv(basedir+'/data/states.csv')
master = pd.read_csv(basedir+'/data/master.csv')
dv=pd.read_csv('https://covidtracking.com/data/download/all-states-history.csv')

dv = dv.drop('positiveScore', 1)
dv = dv.replace({'#REF!': np.nan})
dv[['date', 'state', 'dataQualityGrade']] = dv[['date', 'state', 'dataQualityGrade']].fillna(value="Not Defined")

dv['timeWeeks'] = (pd.Timestamp.now().normalize() - pd.to_datetime(dv['date'])) / np.timedelta64(1, 'D')
dv['timeWeeks'] /= 7
dv['timeWeeks'] = dv['timeWeeks'].values[::-1]
max_time = dv['timeWeeks'].iat[0]
max_time = math.ceil(max_time)
interval = int(math.ceil(max_time/10))

intervals = [0]
for i in range(1,interval+1):
    intervals.append(i*10)

dv['Color'] = "any"
names = list(dict.fromkeys(dv['state']))

color_index = 0
for i in names:
    dv.loc[dv.state == i, 'Color'] = color[color_index]
    color_index += 1
#print(dv[dv.State == "Kruss 2019"]) #check for colors you do not like

def Return_Data():
    return dv