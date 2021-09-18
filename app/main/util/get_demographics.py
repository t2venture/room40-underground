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