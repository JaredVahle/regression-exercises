import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats



def months_to_years(df):
    '''
    Takes in a dataframe of the telco churn data and returns a dataframe that contains a new
    column tenure in years that translated the tenure column to year format.
    '''
    df["tenure_in_years"] = df.tenure / 12
    return df



def plot_variable_pairs(train):
    column = "senior_citizen"
    for col in train.columns:
        sns.lmplot(x = column,y =col, data = train,fit_reg = True)
        plt.show()
        column = col

