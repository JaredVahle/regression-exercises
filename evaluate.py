import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pydataset import data
from math import sqrt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

def plot_residual(df,x):
    plt.figure(figsize = (11,5))

    plt.subplot(121)
    plt.scatter(df[x], df.baseline_residual)
    plt.axhline(y = 0, ls = ':')
    plt.xlabel('x')
    plt.ylabel('Residual')
    plt.title('Baseline Residuals')

    plt.subplot(122)
    plt.scatter(df[x], df.residual)
    plt.axhline(y = 0, ls = ':')
    plt.xlabel('x')
    plt.ylabel('Residual')
    plt.title('OLS model residuals')

def get_residual_squared(df):
    df['residual^2'] = df.residual**2
    df['baseline_residual^2'] = df.baseline_residual**2
    return df

def get_sse(df,residual_squared):
    SSE = df[residual_squared].sum()
    print('SSE =', "{:.1f}".format(SSE))
    
    return SSE

def get_mse(df,SSE):
    MSE = SSE/len(df)
    print("MSE = ", "{:.1f}".format(MSE))
    return MSE

def get_rmse(MSE):
    RMSE = sqrt(MSE)
    print("RMSE = ", "{:.1f}".format(RMSE))
    return RMSE

def get_mse2(df,y,yhat):
    MSE2 = mean_squared_error(df[y], df[yhat])
    print("MSE2", MSE2)