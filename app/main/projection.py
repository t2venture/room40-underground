# -*- coding: utf-8 -*-


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

def neighborhood_list_query_asc_48209_austin():
    QI='''query MyQuery($previous_id: numeric!) {
    usa_avm(where: {tax_assessor__tax_assessor_id: {_and: {fips_code: {_eq: "48209"}, city: {_eq: "AUSTIN"}, tax_assessor_id: {_gt: $previous_id}}}}, distinct_on: tax_assessor_id, order_by: {tax_assessor_id: asc}, limit: 100) {
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
    }
    }
    }'''
    return QI

def return_austin_houses():
  data_diff_demog=[]
  #Non-Empty Initialization
  last_id=1544919
  while (1):
    QI=neighborhood_list_query_asc_48209_austin()
    VI={"previous_id":last_id}
    OI="usa_avm"
    data_diff=make_query_variables(QI, VI, OI)
    if (not data_diff):
      break
    data_diff_demog=data_diff_demog+data_diff
    last_id=data_diff[len(data_diff)-1]['tax_assessor_id']
    return data_diff_demog

