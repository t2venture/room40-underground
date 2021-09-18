import pandas as pd
from datetime import datetime, timedelta
import requests
import json
import logging
import os
import matplotlib.pyplot as plt
from numpy import array
import math
import numpy as np

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
def make_query(Query, obj):
    raw_data=get_graphql_request(Query)
    ans=serialize__to_json(raw_data, obj)
    return ans

def make_query_variables(Query, Variables, obj):
    raw_data=get_graphql_request_variables(Query, Variables)
    ans=serialize__to_json(raw_data, obj)
    return ans

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

def get_demog_total(geog_id):
    Obj_Input="usa_demographics"
    js_output=make_query(census_geog_query(geog_id),Obj_Input)
    return js_output

def get_total_pop(i):
  try:
    total = i['population_age_00_04_count'] + i['population_age_05_09_count'] + i['population_age_10_14_count'] + i['population_age_15_19_count'] + i['population_age_20_24_count'] + i['population_age_25_29_count'] + i['population_age_30_34_count'] + i['population_age_35_39_count'] + i['population_age_40_44_count'] + i['population_age_45_49_count'] + i['population_age_50_54_count'] + i['population_age_55_59_count'] + i['population_age_60_64_count'] + i['population_age_65_69_count'] + i['population_age_70_74_count'] + i['population_age_75_79_count'] + i['population_age_80_84_count'] + i['population_age_over_85_count']
    age = (2 * i['population_age_00_04_count']) + (7 * i['population_age_05_09_count']) + (12 * i['population_age_10_14_count']) + (17 * i['population_age_15_19_count']) + (22 * i['population_age_20_24_count']) + (27 * i['population_age_25_29_count']) + (32 * i['population_age_30_34_count']) + (37 * i['population_age_35_39_count']) + (42 * i['population_age_40_44_count']) + (47 * i['population_age_45_49_count']) + (52 * i['population_age_50_54_count']) + (57 * i['population_age_55_59_count']) + (62 * i['population_age_60_64_count']) + (67 * i['population_age_65_69_count']) + (72 * i['population_age_70_74_count']) + (77 * i['population_age_75_79_count']) + (82 * i['population_age_80_84_count']) + (90 * i['population_age_over_85_count'])
  except TypeError:
    total=None
    age=None
    avg_age=None
    return total, avg_age
  if total==0:
    avg_age=0
  else:
    avg_age = age/total
  return total, avg_age

def get_race_stats(i, pop_1990, pop_2000, curr_count_pop, pop_2026):
  white = {1990: i['race_white_1990_count'], 2000: i['race_white_2000_count'], 2021: i['race_white_count'], 2026: i['race_white_projected_5_year_count']}
  black = {1990: i['race_black_1990_count'], 2000: i['race_black_2000_count'], 2021: i['race_black_count'], 2026: i['race_black_projected_5_year_count']}
  asian = {1990: i['race_asian_1990_count'], 2000: i['race_asian_2000_count'], 2021: i['race_asian_count'], 2026: i['race_asian_projected_5_year_count']}
  try:
    other_1990 = pop_1990 - white[1990] - black[1990] - asian[1990]
  except TypeError:
    other_1990=None
  try:
    other_2000 = pop_2000 - white[2000] - black[2000] - asian[2000]
  except TypeError:
    other_2000=None
  try:
    other_2021 = curr_count_pop - white[2021] - black[2021] - asian[2021]
  except TypeError:
    other_2021=None
  try:
    other_2026 = pop_2026 - white[2026] - black[2026] - asian[2026]
  except TypeError:
    other_2026=None
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


def summarize_stats(geog_id):
    data=get_demog_total(geog_id)
    total_pop=0
    for i in data:
        if i['year']==2021:
            curr_county_pop, curr_avg_age = get_total_pop(i)

            age_stats = get_age_stats(i, curr_avg_age)

            pop_stats = get_pop_stats(i, curr_county_pop)

            hh_stats = get_household_stats(i)

            race_stats = get_race_stats(i, pop_stats[1990], pop_stats[2000], pop_stats[2021], pop_stats[2026])

            education_stats = get_education_stats(i)

            income = i['median_household_income']
            try:
                total_pop = total_pop + curr_county_pop
            except TypeError:
                total_pop=None
            vars = {'pop': curr_county_pop, 'age': age_stats, 'pop': pop_stats, 'hh': hh_stats, 'race': race_stats, 'education': education_stats, 'income': income}
            return vars
