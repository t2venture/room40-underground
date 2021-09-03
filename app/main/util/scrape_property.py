
from typing import List
import pandas as pd
from datetime import datetime, timedelta
import requests
import json
import logging
import os
import matplotlib.pyplot as plt
from numpy import array


import numpy as np
import sklearn
from sklearn import model_selection
from sklearn.metrics import mean_squared_error
import math


logger = logging.getLogger(__name__)

url = 'https://graphql.cherre.com/graphql'
# Customize these variables.
file_dir = ''  # Must include trailing slash. If left blank, 
# csv will be created in the current directory.
api_email='lukeowentruitt@gmail.com'
api_token ='Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJHcmFwaFFMIFRva2VuIiwibmFtZSI6IiIsImh0dHBzOi8vaGFzdXJhLmlvL2p3dC9jbGFpbXMiOnsieC1oYXN1cmEtYWxsb3dlZC1yb2xlcyI6WyJ0Ml9kZXZlbG9wbWVudCJdLCJ4LWhhc3VyYS1kZWZhdWx0LXJvbGUiOiJ0Ml9kZXZlbG9wbWVudCIsIngtaGFzdXJhLXVzZXItaWQiOiJ0Ml9kZXZlbG9wbWVudCIsIngtaGFzdXJhLW9yZy1pZCI6InQyX2RldmVsb3BtZW50In19.sjHOw5oF3vYb3S_dxhWT7ucJ1qvQccDaHbyjzLkrKQQ'
api_account='Luke Truitt'

def get_graphql_request (Query):
    headers = {'content-type': 'application/json', 'X-Auth-Email': api_email, 'Authorization': api_token}
    # This variable replacement requires Python3.6 or higher
    payload = {"query": Query}
    r = requests.request("POST",url, json=payload, headers=headers)
    return r

def get_graphql_request_variables (Query,Variables):
    headers = {'content-type': 'application/json', 'X-Auth-Email': api_email, 'Authorization': api_token}
    # This variable replacement requires Python3.6 or higher
    payload = {"query": Query, "variables": Variables}
    r = requests.request("POST",url, json=payload, headers=headers)
    return r

def serialize__to_json(cherre, obj):
    """
    Function converts cherre API response to reduced dictionary"""
    if not (isinstance(cherre, requests.models.Response)):
        raise TypeError(
            f"The cherre must be a requests.models.Response, found {type(cherre)}."
        )
    elif not (isinstance(obj, str)):
        raise TypeError(f"The object you are querying must be a str, found {type(obj)}.")
    else:
        if cherre.status_code == 200:
            json_response = json.loads(cherre.content)
            try:
                hits = json_response.get("data").get(obj)
            except AttributeError:
                logger.info(f"No hits found under multimatch for this object query for {obj}.")
                hits = 0
            return hits

def make_eval_df(y_pred,y_true, date):
    y_pred.name='y_pred'
    y_true.name='y_true'
    date.name='date'
    df = pd.concat([y_pred,y_true,date],axis=1)
    for i, row in df.iterrows():
      if i==0:
        df.at[i, 'move_pred']=np.nan
        df.at[i, 'move_true']=np.nan
      else:
        df.at[i, 'move_pred']=df['y_pred'][i]-df['y_pred'][i-1]
        df.at[i, 'move_true']=df['y_true'][i]-df['y_true'][i-1]
    #move_pred.name='move_pred'
    #move_true.name='move_true'
    df['sign_pred'] = df.move_pred.apply(np.sign)
    df['sign_true'] = df.move_true.apply(np.sign)
    df['is_correct'] = 0
    df.loc[df.sign_pred * df.sign_true > 0 ,'is_correct'] = 1 
    df['is_incorrect'] = 0
    df.loc[df.sign_pred * df.sign_true < 0,'is_incorrect'] = 1 
    df['is_predicted'] = df.is_correct + df.is_incorrect
    df['result'] = df.sign_pred * df.move_true
    return df

def calc_scorecard(df):
    scorecard = pd.Series(dtype='float64')
    # building block metrics
    scorecard.loc['accuracy'] = df.is_correct.sum()*1. / (df.is_predicted.sum()*1.)*100
    scorecard.loc['edge'] = df.result.mean()
    scorecard.loc['noise'] = df.move_pred.diff().abs().mean()
    scorecard.loc['move_true_chg'] = df.move_true.abs().mean()
    scorecard.loc['move_pred_chg'] = df.move_pred.abs().mean()
    scorecard.loc['prediction_calibration'] = scorecard.loc['move_pred_chg']/scorecard.loc['move_true_chg']
    scorecard.loc['capture_ratio'] = scorecard.loc['edge']/scorecard.loc['move_true_chg']*100
    scorecard.loc['edge_long'] = df[df.sign_pred == 1].result.mean()  - df.move_true.mean()
    scorecard.loc['edge_short'] = df[df.sign_pred == -1].result.mean()  - df.move_true.mean()
    scorecard.loc['edge_win'] = df[df.is_correct == 1].result.mean()  - df.move_true.mean()
    scorecard.loc['edge_lose'] = df[df.is_incorrect == 1].result.mean()  - df.move_true.mean()
    return scorecard

def make_query(Query, obj):
    raw_data=get_graphql_request(Query)
    ans=serialize__to_json(raw_data, obj)
    return ans

def make_query_variables(Query, Variables, obj):
    raw_data=get_graphql_request_variables(Query, Variables)
    ans=serialize__to_json(raw_data, obj)
    return ans
### THESE ARE TO BE USED BY ALL FUNCTIONS
### FROM HERE OTHER FUNCTIONS START
def list_houses_fips_city(fips, city):
  ans='''query MyQuery($previous_id: numeric!) {
  tax_assessor(where: {_and: {fips_code: {_eq: "'''+fips+'''"}, city: {_eq: "'''+city+'''"}, tax_assessor_id: {_gt: $previous_id}}}, distinct_on: tax_assessor_id, order_by: {tax_assessor_id: asc}, limit: 100) {
    tax_assessor_id
    address
    building_sq_ft
    gross_sq_ft
    latitude
    longitude
    units_count
    property_use_standardized_code
    bed_count
    bath_count
    zip
    tax_assessor_usa_neighborhood_boundary__bridge {
      usa_neighborhood_boundary__geography_id {
        geography_id
        geography_code
        boundary_id
        area
      }
    }
  }
  }'''
  return ans

def unique_fips_query(city, state):
  ans='''query MyQuery {
  tax_assessor(distinct_on: fips_code, where: {_and: {city: {_eq: "'''+city+'''"}, state: {_eq: "'''+state+'''"}}}) {
    fips_code
  }
  }'''
  return ans

def calculate_fips_dict():
  dict_of_fips=dict()
  #VARIABLE TO CHANGE
  cities=[("CHATTANOOGA", "TN"), ("CHATTANOOGA", "GA"), ("AUSTIN", "TX")]
  for city in cities:
    dict_of_fips[city[0]]=[]
  for city in cities:
    QI=unique_fips_query(city[0], city[1])
    OI="tax_assessor"
    data_cherre=make_query(QI, OI)
    dict_of_fips[city[0]]=dict_of_fips[city[0]]+data_cherre
  return dict_of_fips

def return_raw_propertys():
  dict_of_fips=calculate_fips_dict()
  dict_of_propertys_in_fips_city=dict()
  for city_name in dict_of_fips.keys():
    fips_list=dict_of_fips[city_name]
    for fips_map in fips_list:
      fips_number=fips_map["fips_code"]
      data_diff_houses=[]
      previous_id=1
      while(1):
        QI=list_houses_fips_city(fips_number, city_name) 
        VI={"previous_id": previous_id}
        OI="tax_assessor"
        data_diff=make_query_variables(QI, VI, OI)
        if not data_diff:
          break
        data_diff_houses=data_diff_houses+data_diff
        previous_id=data_diff[len(data_diff)-1]['tax_assessor_id']
        ###THIS IS FOR TESTING REMOVE THE 200 LIMIT WHEN DEPLOYING
        if len(data_diff_houses)>=300:
          break
      dict_of_propertys_in_fips_city[fips_number]=data_diff_houses
  return dict_of_propertys_in_fips_city

#THIS PARSES GRAPHQL DICT INTO OUR SCHEMA FORM
def return_list_property(data_diff_demog):
  List_Property=[]
  dict_of_fips=calculate_fips_dict()
  dict_of_propertys_in_fips_city=return_raw_propertys()
  for city in dict_of_fips.keys():
    for fips_dict in dict_of_fips[city]:
      fips=fips_dict['fips_code']
      for i in dict_of_propertys_in_fips_city[fips]:
        if not i['latitude']:
          continue
        if not i['longitude']:
          continue
        if not i['property_use_standardized_code']:
          continue
        if i['property_use_standardized_code']!="385":
          continue
        if not i['bed_count']:
          continue
        if not i['building_sq_ft']:
          continue
        '''
        if(i['bed_count']<3 or i['bed_count']>3):
          continue
        '''
        if(i['building_sq_ft'] > 2300 or i['building_sq_ft'] < 1700):
          continue
    
        MajorCity=city
        UsageCode=i['property_use_standardized_code']
        Address=i['address']
        Building_Sq_Ft=i['building_sq_ft']
        Gross_Sq_Ft=i['gross_sq_ft']
        Latitude=i['latitude']
        Longitude=i['longitude']
        Street=strip_housenumber_street(Address)[1]
        HouseNumber=strip_housenumber_street(Address)[0]
        Dict={"majorcity": MajorCity, "address": Address, "building_sq_ft": Building_Sq_Ft, 
        "gross_sq_ft": Gross_Sq_Ft, "latitude": Latitude, "longitude": Longitude,
        "street": Street, "housenumber": HouseNumber, "usage_code": UsageCode}
        List_Property.append(Dict)
  return List_Property

def strip_housenumber_street(addr):
  if not addr:
    return ('','')
  if ' ' not in addr:
    return ('', addr)
  st=addr.split(' ')
  starray=tuple(st[1:])
  ans=' '.join(starray)
  return (st[0], ans)

def census_geog_query(id):
  QI='''query MyQuery {
  usa_demographics(where: {geography_id: {_eq: "'''+id+'''"}}) {
    year
    age_ave_projected_10_year
    age_ave_projected_5_year
    education_associate_degree_count
    education_bachelors_degree_count
    education_2000_bachelor_count
    education_2000_associate_count
    education_1990_college_count
    household_1990_count
    household_2000_count
    household_projected_5_year_count
    household_count
    household_projected_10_year_count
    median_age_projected_10_year
    median_age_projected_5_year
    median_household_income
    population_1990_count
    population_2000_count
    population_2010_count
    population_5_year_forecast
    population_10_year_forecast
    population_median_age
    race_white_1990_count
    race_white_2000_count
    race_white_count
    race_white_projected_5_year_count
    race_other_1990_count
    race_other_2000_count
    race_other_count
    race_other_projected_5_year_count
    race_black_1990_count
    race_black_2000_count
    race_black_count
    race_black_projected_5_year_count
    race_asian_1990_count
    race_asian_2000_count
    race_asian_count
    race_asian_projected_5_year_count
    population_age_00_04_count
    population_age_05_09_count
    population_age_10_14_count
    population_age_15_19_count
    population_age_25_29_count
    population_age_20_24_count
    population_age_30_34_count
    population_age_35_39_count
    population_age_45_49_count
    population_age_40_44_count
    population_age_50_54_count
    population_age_55_59_count
    population_age_60_64_count
    population_age_65_69_count
    population_age_70_74_count
    population_age_75_79_count
    population_age_80_84_count
    population_age_over_85_count
  }
  }'''
  return QI

def get_total_pop(i):
  total = i['population_age_00_04_count'] + i['population_age_05_09_count'] + i['population_age_10_14_count'] + i['population_age_15_19_count'] + i['population_age_20_24_count'] + i['population_age_25_29_count'] + i['population_age_30_34_count'] + i['population_age_35_39_count'] + i['population_age_40_44_count'] + i['population_age_45_49_count'] + i['population_age_50_54_count'] + i['population_age_55_59_count'] + i['population_age_60_64_count'] + i['population_age_65_69_count'] + i['population_age_70_74_count'] + i['population_age_75_79_count'] + i['population_age_80_84_count'] + i['population_age_over_85_count']
  age = (2 * i['population_age_00_04_count']) + (7 * i['population_age_05_09_count']) + (12 * i['population_age_10_14_count']) + (17 * i['population_age_15_19_count']) + (22 * i['population_age_20_24_count']) + (27 * i['population_age_25_29_count']) + (32 * i['population_age_30_34_count']) + (37 * i['population_age_35_39_count']) + (42 * i['population_age_40_44_count']) + (47 * i['population_age_45_49_count']) + (52 * i['population_age_50_54_count']) + (57 * i['population_age_55_59_count']) + (62 * i['population_age_60_64_count']) + (67 * i['population_age_65_69_count']) + (72 * i['population_age_70_74_count']) + (77 * i['population_age_75_79_count']) + (82 * i['population_age_80_84_count']) + (90 * i['population_age_over_85_count'])
  if total==0:
    avg_age=0
  else:
    avg_age = age/total
  return total, avg_age

def get_race_stats(i, pop_1990, pop_2000, curr_count_pop, pop_2026):
  white = {1990: i['race_white_1990_count'], 2000: i['race_white_2000_count'], 2021: i['race_white_count'], 2026: i['race_white_projected_5_year_count']}
  black = {1990: i['race_black_1990_count'], 2000: i['race_black_2000_count'], 2021: i['race_black_count'], 2026: i['race_black_projected_5_year_count']}
  asian = {1990: i['race_asian_1990_count'], 2000: i['race_asian_2000_count'], 2021: i['race_asian_count'], 2026: i['race_asian_projected_5_year_count']}

  other_1990 = pop_1990 - white[1990] - black[1990] - asian[1990]
  other_2000 = pop_2000 - white[2000] - black[2000] - asian[2000]
  other_2021 = curr_count_pop - white[2021] - black[2021] - asian[2021]
  other_2026 = pop_2026 - white[2026] - black[2026] - asian[2026]

  other = {1990: other_1990, 2000: other_2000, 2021: other_2021, 2026: other_2026}
  
  return {'white': white, 'black': black, 'asian': asian, 'other': other}

def get_education_stats(i):

  curr_college = i['education_associate_degree_count'] + i['education_bachelors_degree_count']
  college_2000 = i['education_2000_associate_count'] + i['education_2000_bachelor_count']
  college_1990 = i['education_1990_college_count']
  
  college = {1990: college_1990, 2000: college_2000, 2021: curr_college}

  return college

def get_pop_stats(i, curr_count_pop):

  pop_2010 = i['population_2010_count']
  pop_2000 = i['population_2000_count']
  pop_1990 = i['population_1990_count']
  pop_2026 = i['population_5_year_forecast']
  pop_2031 = i['population_10_year_forecast']

  pop = {1990: pop_1990, 2000: pop_2000, 2010: pop_2010, 2021: curr_count_pop, 2026: pop_2026, 2031: pop_2031}

  return pop

def get_age_stats(i, curr_avg_age):

  age = {2021: i['population_median_age'], 2026: i['age_ave_projected_5_year'], 2031: i['age_ave_projected_10_year']}

  return age

def get_household_stats(i):
  hh_1990 = i['household_1990_count']
  hh_2000 = i['household_2000_count']
  hh_2021 = i['household_count']
  hh_2026 = i['household_projected_5_year_count']
  hh_2031 = i['household_projected_10_year_count']
  
  hh = {1990: hh_1990, 2000: hh_2000, 2021: hh_2021, 2026: hh_2026, 2031: hh_2031}

  return hh
'''
def summarize_demographics():
  total_pop = 0
  vars = dict()
  #####
  for j in dict_of_geog_demog_year.keys():
    data = dict_of_geog_demog_year[j]
    for i in data:
      if i['year']==2021:
        curr_county_pop, curr_avg_age = get_total_pop(i)

        age_stats = get_age_stats(i, curr_avg_age)

        pop_stats = get_pop_stats(i, curr_county_pop)

        hh_stats = get_household_stats(i)

        race_stats = get_race_stats(i, pop_stats[1990], pop_stats[2000], pop_stats[2021], pop_stats[2026])

        education_stats = get_education_stats(i)

        income = i['median_household_income']

        total_pop = total_pop + curr_county_pop

        vars[j] = {'pop': curr_county_pop, 'age': age_stats, 'pop': pop_stats, 'hh': hh_stats, 'race': race_stats, 'education': education_stats, 'income': income}
'''   