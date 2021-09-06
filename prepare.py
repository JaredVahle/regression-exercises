import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import sklearn.preprocessing
from sklearn.model_selection import train_test_split

def scale_telco_data(train,validate,test):
    scaler = sklearn.preprocessing.StandardScaler()
    scaler.fit(train[["monthly_charges","total_charges"]])

    train = scaler.transform(train[["monthly_charges","total_charges"]])
    validate = scaler.transform(validate[["monthly_charges","total_charges"]])
    test = scaler.transform(test[["monthly_charges","total_charges"]])
    
    return train,validate,test