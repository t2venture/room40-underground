from app.main.util.preprocessing import *
from typing import List
import pandas as pd
from datetime import datetime, timedelta
import requests
import json
import logging
import os
import matplotlib.pyplot as plt
from numpy import array
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import Bidirectional
from tensorflow.keras.layers import TimeDistributed
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import ConvLSTM2D
import tensorflow as tf
import numpy as np
import sklearn
from sklearn import model_selection
from sklearn.metrics import mean_squared_error
import math

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
      building_sq_ft
      gross_sq_ft
    }
    }
    }'''
    return QI

## THIS RETURNS 5523 PROPERTYS IN AUSTIN, 48209
def return_austin_propertys():
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

#THIS PARSES GRAPHQL DICT INTO OUR SCHEMA FORM
def return_list_property(data_diff_demog):
  List_Property=[]
  for i in data_diff_demog:
    MajorCity='Austin'
    Address=i['tax_assessor__tax_assessor_id']['address']
    Building_Sq_Ft=i['tax_assessor__tax_assessor_id']['building_sq_ft']
    Gross_Sq_Ft=i['tax_assessor__tax_assessor_id']['gross_sq_ft']
    Dict={"majorcity": MajorCity, "address": Address, "building_sq_ft": Building_Sq_Ft, "gross_sq_ft": Gross_Sq_Ft}
    List_Property.append(Dict)
  return List_Property