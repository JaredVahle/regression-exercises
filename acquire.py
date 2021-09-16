import env
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'



def get_telco_data():
    filename = "telco_churn.csv"

    if os.path.isfile("telco_churn.csv"):
        return pd.read_csv("telco_churn.csv")
    else:
        # read the SQL query into a dataframe
        df = pd.read_sql('''
SELECT *
FROM customers
JOIN contract_types ON contract_types.contract_type_id = customers.contract_type_id
JOIN internet_service_types ON internet_service_types.internet_service_type_id = customers.internet_service_type_id
JOIN payment_types ON payment_types.payment_type_id = customers.payment_type_id;
''', get_connection("telco_churn"))

        # Write that dataframe to disk for later. Called "caching" the data for later.
        df.to_csv("telco_churn.csv")

        # Return the dataframe to the calling code
        return df 

def clean_telco(df):
    df.total_charges.replace(to_replace = {" ":"0"}, inplace = True)
    df.total_charges = df.total_charges.astype("float")
    df["auto_pay"] = df.payment_type.str.contains("auto")
    df["auto_pay"] = df.auto_pay.replace(to_replace = [True,False],value = [1,0])
    dummy_df = pd.get_dummies(df[['gender', 'payment_type',"internet_service_type","contract_type"]])
    dummy_df.columns = [col.lower().replace(" ","_") for col in dummy_df]
    
    df["partner"] = df.partner.replace(to_replace = ["Yes","No"],value = [1,0])
    df["dependents"] = df.dependents.replace(to_replace = ["Yes","No"],value = [1,0])
    df["churn"] = df.churn.replace(to_replace = ["Yes","No"],value = [1,0])
    df["multiple_lines"] = df.paperless_billing.replace(to_replace = ["Yes","No","No phone service"],value = [1,0,0])
    df["paperless_billing"] = df.paperless_billing.replace(to_replace = ["Yes","No","No internet service"],value = [1,0,0])
    df["tech_support"] = df.tech_support.replace(to_replace = ["Yes","No","No internet service"],value = [1,0,0])
    df["device_protection"] = df.device_protection.replace(to_replace = ["Yes","No","No internet service"],value = [1,0,0])
    df["online_backup"] = df.online_backup.replace(to_replace = ["Yes","No","No internet service"],value = [1,0,0])
    df["online_security"] = df.online_security.replace(to_replace = ["Yes","No","No internet service"],value = [1,0,0])
    df["streaming_tv"] = df.streaming_tv.replace(to_replace = ["Yes","No","No internet service"],value = [1,0,0])
    df["streaming_movies"] = df.streaming_movies.replace(to_replace = ["Yes","No","No internet service"],value = [1,0,0])
    df["phone_service"] = df.phone_service.replace(to_replace = ["Yes","No","No internet service"],value = [1,0,0])
    df["multiple_lines"] = df.multiple_lines.replace(to_replace = ["Yes","No","No phone service"],value = [1,0,0])
    df["add_ons"] =  df.online_security + df.online_backup + df.device_protection + df.tech_support + df.streaming_tv + df.streaming_movies
    df.drop(columns = ["customer_id",
                       "gender",
                       "payment_type",
                       "internet_service_type",
                       "contract_type",
                   'internet_service_type_id',
                   "contract_type_id",
                   "payment_type_id",
                  "contract_type_id.1",
                   "internet_service_type_id.1",
                   "payment_type_id.1",
                   "Unnamed: 0"],inplace = True)
    return pd.concat([df, dummy_df], axis=1)

def split_telco_data(df):
    """
    splits the data in train validate and test 
    """
    train, test = train_test_split(df, test_size = 0.2, random_state = 123, stratify = df.churn)
    train, validate = train_test_split(train, test_size=.25, random_state=123, stratify=train.churn)
    
    return train, validate, test

def get_mall_data():
    filename = "mall.csv"

    if os.path.isfile("mall.csv"):
        return pd.read_csv("mall.csv")
    else:
        # read the SQL query into a dataframe
        df = pd.read_sql('''
SELECT *
FROM customers;
''', get_connection("mall_customers"))
        # Write that dataframe to disk for later. Called "caching" the data for later.
        df.to_csv("mall.csv")

        # Return the dataframe to the calling code
        return df

def new_zillow_data():
    '''
    Returns zillow into a dataframe
    '''
    sql_query = '''select * from properties_2017
    join predictions_2017 using(parcelid)
    where transactiondate between "2017-05-01" and "2017-08-31"
    and propertylandusetypeid in (260, 261, 262, 263, 264, 265, 266, 273, 275, 276, 279)'''
    df = pd.read_sql(sql_query, get_connection('zillow'))
    return df 

def get_zillow_data():
    '''get connection, returns zillow into a dataframe and creates a csv for us'''
    if os.path.isfile('zillow.csv'):
        df = pd.read_csv('zillow.csv', index_col=0)
    else:
        df = new_zillow_data()
        df.to_csv('zillow.csv')
    return df
    
    
    
    
def clean_zillow(df):
    '''
    this function takes in an unclean zillow df and does the following:
    - keeps only columns we need for the project
    - renames columns
    - drops nulls
    '''
    #selecting the features
    features = ['calculatedfinishedsquarefeet', 'bathroomcnt', 'bedroomcnt', 'taxvaluedollarcnt','yearbuilt','taxamount','fips']
    df = df[features]

    
    #rename columns
    df = df.rename(columns={
                            'calculatedfinishedsquarefeet': 'sqft',
                            'bathroomcnt': 'bathroomss',
                            'bedroomcnt': 'bedrooms',
                            'taxvaluedollarcnt':'tax_value',
                            'yearbuilt':'year_built',
                            'taxamount': 'tax_amount'
        
    })

    #drop nulls
    df = df.dropna()
    
    return df