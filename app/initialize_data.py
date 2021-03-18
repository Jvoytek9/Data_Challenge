import os
import math
import requests

import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine

import numpy as np
import pymysql
import pandas as pd
np.warnings.filterwarnings('ignore')
from color import color
#pylint: disable=unused-variable

basedir = os.path.abspath(os.path.dirname(__file__))
master = pd.read_csv(basedir + '/data/master.csv')

#helper function, to convert the ajax url I mined into usable data.
def convert_to_dataframe(url,ID):
  txt = requests.get(url).json()
  return(pd.DataFrame(txt[ID]))

#retrieving the vaccination data first, so the date last stored can be compared to the new dates retrieved lower in code.
dv = convert_to_dataframe("https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=vaccination_data","vaccination_data")

#dv.to_csv(basedir+"/sample.csv",index=False)

#everything below is not used
dv.drop(["ShortName","Census2019", "date_type", "Administered_Dose1_Recip_18Plus", "Administered_Dose1_Recip_18PlusPop_Pct", 
"Administered_Dose2_Recip_18Plus", "Administered_Dose2_Recip_18PlusPop_Pct", "Distributed_Per_100k_18Plus", 
"Administered_18Plus", "Admin_Per_100k_18Plus","Distributed_Unk_Manuf","Administered_Unk_Manuf", "Series_Complete_Moderna",	"Series_Complete_Pfizer",	"Series_Complete_Janssen",	"Series_Complete_Unk_Manuf",	
"Series_Complete_Moderna_18Plus",	"Series_Complete_Pfizer_18Plus",	"Series_Complete_Janssen_18Plus",	"Series_Complete_Unk_Manuf_18Plus",	"Series_Complete_Moderna_65Plus",	
"Series_Complete_Pfizer_65Plus",	"Series_Complete_Janssen_65Plus",	"Series_Complete_Unk_Manuf_65Plus",	"Series_Complete_Yes", 
"Series_Complete_Pop_Pct",	"Series_Complete_18Plus", "Series_Complete_18PlusPop_Pct", "Series_Complete_65Plus", "Series_Complete_65PlusPop_Pct", 
"Administered_Fed_LTC",	"Administered_Fed_LTC_Dose1",	"Administered_Fed_LTC_Dose2",	"Series_Complete_FedLTC",
"Distributed_Per_100k_65Plus"],axis=1,inplace=True)


#everything below is used. Same pattern is found in following datasets.
dv.columns = ["date","abbr","State/Territory/Federal Entity","Doses Distributed","Doses Administered",
"Distributed per 100K","Administered per 100K", "Administered Moderna", "Administered Pfizer", "Administered J&J",
"Administered Dose 1", "Administered Dose 1 Pop. Percent",	"Administered Dose 2 Pop. Percent", 
"Administered Dose 1 Age 65+", "Administered Dose 1 Age 65+ Pop. Percent", "Administered 65+", "Administered 65+ per 100k", "Administered Dose 2", 
"Distributed Moderna", "Distributed Pfizer", "Distributed J&J"]

#below shifts around the order, placing administered dose 2 in spot 13, so it lines up better in the graph dropdowns
dv.insert(13, "Administered Dose 2", dv.pop("Administered Dose 2"))

try: #want to make sure I can reach the sql server.
  connection = mysql.connector.connect(user='Josh', password='Paperfly12!', host='127.0.0.1', database='Covid_Data')

except mysql.connector.Error as err: #errors for debugging if I can't reach the sql server

  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Wrong username or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)

else: #assuming all was good and sql database connected

  # Create SQLAlchemy engine to connect to MySQL Database, allows for converting to pandas dataframes easily
  engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(host='localhost', db='covid_data', user='Josh', pw='Paperfly12!'))

  cursor = connection.cursor()
  cursor.execute("Select date from compiled_data ORDER BY date DESC LIMIT 1") #for finding the most recent date in the current sql database
  for date in cursor.fetchall():
    if date[0] != dv.date.values[-1]: #if the most recent date in the sql database != the most recent CDC data

      #Gathering the case and death data together            
      cases_and_deaths = convert_to_dataframe("https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=US_MAP_DATA",'US_MAP_DATA')
      cases_and_deaths.drop(["tot_cases_last_24_hours","tot_death_last_24_hours","id","Seven_day_cum_new_cases_per_100k","Seven_day_cum_new_deaths_per_100k"],axis=1,inplace=True)

      cases_and_deaths.columns = ["abbr","Total Cases","Confirmed Cases","Probable Cases","Cases Last 7 Days","Deaths Last 7 Days"
      ,"Case Rate per 100K Last 7 Days","Death Rate per 100K Last 7 Days",
      "Total Deaths","Confirmed Deaths","Probable Deaths","Death Rate per 100K","Case Rate per 100K",
      "fips","State/Territory"]

      cases_and_deaths.drop(['abbr','fips'],axis=1,inplace=True)

      #moving state info, for efficient merging later on
      cases_and_deaths.insert(0, "State/Territory", cases_and_deaths.pop("State/Territory"))

      #Gathering the test data together. Also provides percent positives for risk calc.
      #Not used, but populated
      #total_positive_test_results_reported, total_positive_test_results_reported_7_day_count_change, total_positive_test_results_reported_30_day_count_change
      tests = convert_to_dataframe("https://covid.cdc.gov/covid-data-tracker/COVIDData/getAjaxData?id=US_MAP_TESTING",'US_MAP_TESTING')
      
      percent_positives = tests[["date","name","total_positive_test_results_reported", "total_positive_test_results_reported_7_day_count_change", 
      "total_positive_test_results_reported_30_day_count_change","percent_positive_7_day_range","percent_positive_30_day_range","percent_positive_total_range"]].copy()
      
      percent_positives.columns = ["date","State/Territory/Federal Entity","total_positive_test_results_reported", 
      "total_positive_test_results_reported_7_day_count_change", "total_positive_test_results_reported_30_day_count_change",
      "Percent Positive 7 Days","Percent Positive 30 Days","Percent Positive All time"]

      tests.drop(["id","percent_positive_7_day","percent_positive_30_day","percent_positive_total","total_positive_test_results_reported",
      'percent_positive_7_day', 'percent_positive_30_day','percent_positive_total', 'total_positive_test_results_reported','total_positive_test_results_reported_7_day_count_change', 
      'total_positive_test_results_reported_30_day_count_change','percent_positive_7_day_range', 'percent_positive_30_day_range','percent_positive_total_range'],axis=1,inplace=True)

      tests.columns = ["abbr","date","fips","State","Tests per 100K Last 7 Days","Tests Last 7 Days",
      "Tests per 100K Last 30 Days","Tests Last 30 Days","Tests per 100K","Total Tests"]
      tests.drop(['date','abbr'],axis=1,inplace=True)

      #Merging the 3 datasets above together relative to the state, so it is one big database
      dv = pd.merge(dv, cases_and_deaths, left_on='State/Territory/Federal Entity', right_on='State/Territory', how='left')
      dv = pd.merge(dv, tests, left_on='State/Territory/Federal Entity', right_on='State', how='left')
      dv.drop(['State','State/Territory'], axis=1, inplace=True)

      #moving the location of fips in the master dataset, to allow for easy filtering later
      dv.insert(1, "fips", dv.pop("fips"))
      dv = dv.replace({'null': None})

      # Convert master dataframe to sql table called compiled_data.
      dv.to_sql('compiled_data', engine, index=False, if_exists='append')
      percent_positives.to_sql('percent_positives', engine, index=False, if_exists='replace')

      print("SQL Databases Updated.")

  # table will be returned as a dataframe. This is the master dataset from sql.
  dv = pd.read_sql_table('compiled_data', engine)
  percent_positives = pd.read_sql_table('percent_positives', engine)
  dv[dv.columns[4:]] = dv[dv.columns[4:]].apply(pd.to_numeric)
  
  # converts date to correct format, for homogeneity
  dv['date'] = pd.to_datetime(dv['date'])
  dv['date'] = dv['date'].dt.strftime('%Y-%m-%d')

  # finding the days elapsed and making a new column, so this data can be plotted. Basically our time axis
  dv['Days Elapsed'] = (pd.Timestamp.now().normalize() - pd.to_datetime(dv['date'])) / np.timedelta64(1, 'D')
  dv['Days Elapsed'] /= 1
  dv['Days Elapsed'] = dv['Days Elapsed'].values[::-1]

  # below will be used to implement a ranged slider, so users can select dates of interest from new time column found above
  # max_time = dv['timeWeeks'].iat[0]
  # max_time = math.ceil(max_time)
  # interval = int(math.ceil(max_time/10))

  # intervals = [0]
  # for i in range(1,interval+1):
  #     intervals.append(i*10)

  #assigning a unique color to each state, so the color is constant at all times
  dv['Color'] = "any"
  abbreviations = dv.abbr.unique()
  
  color_index = 0
  for i in abbreviations:
      dv.loc[dv.abbr == i, 'Color'] = color[color_index]
      color_index += 1
  #print(dv[dv["State/Territory/Federal Entity"] == "Alaska"]) #check for colors you do not like
  
  def Return_Data():
      return([dv,percent_positives])

  connection.close()