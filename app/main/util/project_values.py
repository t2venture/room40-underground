from random import randrange
from pandas import Series
from matplotlib import pyplot
from statsmodels.tsa.seasonal import seasonal_decompose
import datetime
import pandas as pd
from pandas import read_csv
from pandas import DataFrame
import statsmodels
from matplotlib import pyplot
from statsmodels.tsa.stattools import adfuller
from numpy import log
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.arima_model import ARIMA
import numpy as np

def project_arima(addr, train_list_of_med_val, test_list_of_med_val):
    X=train_list_of_med_val[0]+test_list_of_med_val[0]
    df=pd.DataFrame(X, columns=['value'])
    model = ARIMA(df.value, order=(1, 0, 0)) 
    fitted=model.fit(disp=-1)
    fc1yr=fitted.forecast(12)[0]
    model = ARIMA(df.value, order=(1, 0, 0))
    fitted=model.fit(disp=-1)
    fc2yr=fitted.forecast(24)[0]
    return fc1yr, fc2yr


def forecast_accuracy(forecast, actual):
    mape = np.mean(np.abs(forecast - actual)/np.abs(actual))  # MAPE
    me = np.mean(forecast - actual)             # ME
    mae = np.mean(np.abs(forecast - actual))    # MAE
    mpe = np.mean((forecast - actual)/actual)   # MPE
    rmse = np.mean((forecast - actual)**2)**.5  # RMSE
    corr = np.corrcoef(forecast, actual)[0,1]   # corr
    mins = np.amin(np.hstack([forecast[:,None], 
                              actual[:,None]]), axis=1)
    maxs = np.amax(np.hstack([forecast[:,None], 
                              actual[:,None]]), axis=1)
    minmax = 1 - np.mean(mins/maxs)             # minmax
    return({'mape':mape, 'me':me, 'mae': mae, 
            'mpe': mpe, 'rmse':rmse, 
            'corr':corr, 'minmax':minmax})
