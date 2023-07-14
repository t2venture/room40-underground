import pandas as pd
from datetime import datetime, timedelta
import requests
import json
import logging
import os
import matplotlib.pyplot as plt
from numpy import array
from keras.models import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from keras.layers import Bidirectional
from keras.layers import TimeDistributed
from keras.layers.convolutional import Conv1D
from keras.layers.convolutional import MaxPooling1D
from keras.layers import Flatten
from keras.layers import ConvLSTM2D
import keras
import tensorflow as tf
import numpy as np
import sklearn
from sklearn import model_selection
from sklearn.metrics import mean_squared_error
import math
from itertools import islice
import threading
import time

logger = logging.getLogger(__name__)

url = 'https://graphql.cherre.com/graphql'
# Customize these variables.
file_dir = ''  # Must include trailing slash. If left blank, 
# csv will be created in the current directory.
api_email='lukeowentruitt@gmail.com'
api_token = os.getenv("CHERRE_API_TOKEN")
if not api_token:
    raise ValueError("Need to define CHERRE_API_TOKEN environment variable")
auth_header_value = 'Bearer ' + api_token
api_account='Luke Truitt'

dict_poi_nd=dict()
dict_poi_id_poi=dict()
fips='48453'

def get_graphql_request (Query):
    headers = {'content-type': 'application/json', 'X-Auth-Email': api_email, 'Authorization': auth_header_value}
    # This variable replacement requires Python3.6 or higher
    payload = {"query": Query}
    r = requests.request("POST",url, json=payload, headers=headers)
    return r

def get_graphql_request_variables (Query,Variables):
    headers = {'content-type': 'application/json', 'X-Auth-Email': api_email, 'Authorization': auth_header_value}
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
    airport_distance
    closest_major_city
    education_graduate_degree_count
    education_high_school_graduate_count
    education_less_than_9_count
    education_some_college_count
    education_some_high_school_count
    education_total_population_count
    median_household_income_25_44
    median_household_income_45_64
    median_household_income_5_year_forecast
    median_household_income_over_65
    median_household_income_under_25
    population_2000_count
    population_2010_count
    population_5_year_forecast
    population_5_year_forecast_high
    population_5_year_forecast_low
    population_age_00_04_count
    population_age_05_09_count
    population_age_10_14_count
    population_age_15_19_count
    population_age_20_24_count
    population_age_25_29_count
    population_age_30_34_count
    population_age_35_39_count
    population_age_40_44_count
    population_age_45_49_count
    population_age_50_54_count
    population_age_55_59_count
    population_age_60_64_count
    population_age_65_69_count
    population_age_70_74_count
    population_age_75_79_count
    population_age_80_84_count
    population_age_over_85_count
    population_density
    population_diff_2000_percent
    population_diff_2010_percent
    race_asian_2000_count
    race_asian_count
    race_asian_projected_5_year_count
    race_black_2000_count
    race_black_count
    race_black_projected_5_year_count
    race_hispanic_count
    race_hispanic_projected_5_year_count
    race_other_count
    race_other_projected_5_year_count
    race_total_population_count
    race_white_2000_count
    race_white_count
    race_white_projected_5_year_count
  }
  }'''
  return QI

def link_poi_and_neighborhood(neighborhood_id):
  string='''query MyQuery($prev_poi_id: numeric!){
  usa_points_of_interest_usa_neighborhood_boundary(where: {_and: {neighborhood_id: {_eq: "'''+neighborhood_id+'''"}, poi_id: {_gt: $prev_poi_id}}}) {
    cherre_input_address
    neighborhood_id
    poi_id
  }
  }

    '''
  return string

def geography_id_list_county_id(county_id):
  QI='''query MyQuery($prev_geography_id: String!) {
  usa_demographics(where: {_and: {county_code_5: {_eq: "'''+county_id+'''"}, geography_id: {_gt: $prev_geography_id}}}, distinct_on: geography_id, order_by: {geography_id: asc}) {
    geography_id
    geography_code
    geography_name
   }
  }'''
  return QI

#Non-Empty Initialization
def initialize_data_geog_demog():
	last_geog_id="C0"
	data_geog_demog=[]
	while (1):
  		QI=geography_id_list_county_id('48453')
		#CHANGE THIS ACCORDINGLy
  		VI={"prev_geography_id": last_geog_id}
  		OI="usa_demographics"
  		data_geog=make_query_variables(QI, VI, OI)
  		if (not data_geog):
			  break
  		data_geog_demog=data_geog_demog+data_geog
  		last_geog_id=data_geog[len(data_geog)-1]['geography_id']
	return data_geog_demog

def initialize_neighborhoods():
	data_geog_demog=initialize_data_geog_demog()
	data_geog_demog_nd=[]
	for i in data_geog_demog:
		if 'ND' in i['geography_id']:
			data_geog_demog_nd.append(i)
	return data_geog_demog_nd

from itertools import islice

def chunkdict(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield {k:data[k] for k in islice(it, SIZE)}

def chunklist(data, SIZE=10000):
    it = iter(data)
    for i in range(0, len(data), SIZE):
        yield data[i:i + SIZE]

def initialize_geog_dicts():
	list_of_geog_dicts=[]
	data_geog_demog_nd=initialize_neighborhoods()
	for item in chunklist(data_geog_demog_nd, 20):
		list_of_geog_dicts.append(item)
	return list_of_geog_dicts


def wrapper_nd_poi_scraper(chunk_dictionary, thread_id):
  for i in chunk_dictionary:
    data_link_poi=[]
    last_poi_id=1
    while(1):
      g_id=i['geography_id']
      OI="usa_points_of_interest_usa_neighborhood_boundary"
      VI={"prev_poi_id":last_poi_id}
      QI=link_poi_and_neighborhood(g_id)
      data_link=make_query_variables(QI, VI, OI)
      if not data_link:
        break
      data_link_poi=data_link_poi+data_link
      last_poi_id=data_link[len(data_link)-1]['poi_id']
      #####print (thread_id, len(data_link_poi), last_poi_id, i["geography_name"])
    dict_poi_nd[i['geography_id']]=data_link_poi

def run_thread_query_geog_dicts():
	list_of_ndpoi_threads=[]
	list_of_geog_dicts=initialize_geog_dicts()
	for i in range(len(list_of_geog_dicts)):
		list_of_ndpoi_threads.append(threading.Thread(target=wrapper_nd_poi_scraper, args=(list_of_geog_dicts[i],i,)))
	for i in range(len(list_of_ndpoi_threads)):
		list_of_ndpoi_threads[i].start()
	for i in range(len(list_of_ndpoi_threads)):
		list_of_ndpoi_threads[i].join()


def info_on_poi(poi_id):
  string='''query MyQuery {
  usa_points_of_interest(where: {poi_id: {_eq: "'''+poi_id+'''"}}) {
    business_name
    category
    line_of_business
    industry
    latitude
    longitude
    street
    one_line_address
    zip
  }
  }'''
  return string

def initialize_list_of_poi_nd_poi():
	run_thread_query_geog_dicts()
	list_of_nd_poi_dicts=[]
	for item in chunkdict(dict_poi_nd, 20):
		list_of_nd_poi_dicts.append(item)
	return list_of_nd_poi_dicts

def poi_query_wrapper(chunk_of_dictionary, thread_id):
  for i in chunk_of_dictionary.keys():
    arr=chunk_of_dictionary[i]
    for poi in arr:
      poi_id=poi['poi_id']
      str_poi_id=str(poi_id)
      QI=info_on_poi(str_poi_id)
      OI="usa_points_of_interest"
      data_poi=make_query(QI, OI)
      #######print (thread_id, poi_id, len(dict_poi_id_poi))
      if data_poi:
	      dict_poi_id_poi[poi_id]=data_poi[0]
      else:
        pass

def run_thread_query_poi_id():
	list_of_nd_poi_dicts=initialize_list_of_poi_nd_poi()
	list_of_poi_threads=[]
	for i in range(len(list_of_nd_poi_dicts)):
		list_of_poi_threads.append(threading.Thread(target=poi_query_wrapper, args=(list_of_nd_poi_dicts[i],i,)))
	for i in range(len(list_of_poi_threads)):
		list_of_poi_threads[i].start()
	for i in range(len(list_of_poi_threads)):
		list_of_poi_threads[i].join()


def initialize_tuple_lat_long_poi():
	run_thread_query_poi_id()
	tuple_of_lat_long_poi=[]
	for i in dict_poi_id_poi.values():
		tuple_of_lat_long_poi.append((i['latitude'], i['longitude']))
		return tuple_of_lat_long_poi

def neighborhood_list_query_asc_austin(fips):
    QI='''query MyQuery($previous_id: numeric!) {
    usa_avm(where: {tax_assessor__tax_assessor_id: {_and: {fips_code: {_eq: "'''+fips+'''"}, city: {_eq: "AUSTIN"}, tax_assessor_id: {_gt: $previous_id}}}}, distinct_on: tax_assessor_id, order_by: {tax_assessor_id: asc}, limit: 100) {
    tax_assessor_id
    tax_assessor__tax_assessor_id {
      parcel_boundary__tax_assessor_id {
        fips_code
      }
      tax_assessor_usa_neighborhood_boundary__bridge {
        usa_neighborhood_boundary__geography_id {
          geography_id
          geography_code
          boundary_id
          area
        }
      }
      address
      building_sq_ft
      gross_sq_ft
      latitude
      longitude
    }
    }
    }'''
    return QI


def initialize_diff_demog():
	data_diff_demog=[]
	#Non-Empty Initialization
	last_id=1
	while (1):
		QI=neighborhood_list_query_asc_austin("48453")
		VI={"previous_id":last_id}
		OI="usa_avm"
		data_diff=make_query_variables(QI, VI, OI)
		if (not data_diff):
			break
		data_diff_demog=data_diff_demog+data_diff
  		####print (len(data_diff_demog))
  		last_id=data_diff[len(data_diff)-1]['tax_assessor_id']
	return data_diff_demog

def initialize_tuple_lat_long_houses():
	data_diff_demog=initialize_diff_demog()
	tuple_of_lat_long_houses=[]
	for i in data_diff_demog:
		tuple_of_lat_long_houses.append((i['tax_assessor__tax_assessor_id']['latitude'], i['tax_assessor__tax_assessor_id']['longitude']))
	return tuple_of_lat_long_houses

def dist_euc(tuple1, tuple2):
  return math.sqrt((tuple1[0]-tuple2[0])**2 + (tuple1[1]-tuple2[1])**2)

def return_list_of_raw_scores():
	list_of_raw_scores=[]
	tuple_lat_long_poi=initialize_tuple_lat_long_poi()
	tuple_lat_long_houses=initialize_tuple_lat_long_houses()
	for x in tuple_lat_long_houses:
		ans=0
		for i in tuple_lat_long_poi:
			ans+=dist_euc(i, x)
		ans/=len(tuple_lat_long_poi)
		list_of_raw_scores.append(ans)
	return list_of_raw_scores

def return_list_of_lasso_location_scores():
	list_of_raw_scores=return_list_of_raw_scores()
	lasso_location_array=[]
	maxscore=max(list_of_raw_scores)
	minscore=min(list_of_raw_scores)
	for i in list_of_raw_scores:
		ans=50+((i-minscore)/(maxscore-minscore)*50)
		lasso_location_array.append(ans)
	return lasso_location_array


def run_location_score(fips_code):
	global fips
	fips=fips_code
	return return_list_of_lasso_location_scores()



