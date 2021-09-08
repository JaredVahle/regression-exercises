import env
import os
import pandas as pd

def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def get_telco_data():
    filename = "zillow.csv"

    if os.path.isfile("zillow.csv"):
        return pd.read_csv("zillow.csv")
    else:
        # read the SQL query into a dataframe
        df = pd.read_sql('''
SELECT bedroomcnt,bathroomcnt,calculatedfinishedsquarefeet,taxvaluedollarcnt,yearbuilt,taxamount,fips
FROM properties_2017
WHERE propertylandusetypeid = 261;
''', get_connection("zillow"))

        # Write that dataframe to disk for later. Called "caching" the data for later.
        df.to_csv("zillow.csv")

        # Return the dataframe to the calling code
        return df 

def rename_zillow_cols(df):
    '''
    This takes in the zillow dataframe and renames the columns
    making them more readable.
    '''
    df.rename(columns = {"bedroomcnt":"bedroom_count",
                       "bathroomcnt":"bathroom_count",
                         "taxvaluedollarcnt":"tax_value_dollar_count",
                       "calculatedfinishedsquarefeet":"calculated_finished_square_feet",
                       "yearbuilt":"year_built",
                       "taxamount":"tax_amount"},inplace = True)
    return df

def remove_outliers(df, k, col_list):
    ''' remove outliers from a list of columns in a dataframe 
        and return that dataframe
    '''
    
    for col in col_list:

        q1, q3 = df[col].quantile([.25, .75])  # get quartiles
        
        iqr = q3 - q1   # calculate interquartile range
        
        upper_bound = q3 + k * iqr   # get upper bound
        lower_bound = q1 - k * iqr   # get lower bound

        # return dataframe without outliers
        
        df = df[(df[col] > lower_bound) & (df[col] < upper_bound)]
        
    return df

def wrangle_zillow():
    # reads in our zillow csv into a pandas dataframe
    df = pd.read_csv('zillow.csv')
    # uses our function to rename the columns for readability
    rename_zillow_cols(df)
    # Replaces the 0.0 with the most freqent occuring bedroom/bathroom count
    df.bedroom_count.replace(to_replace = [0.0],value = [3],inplace = True)
    df.bathroom_count.replace(to_replace = [0.0],value = [2],inplace = True)
    # fills the na values with the most freqent occuring bedroom/bathroom count
    df.bedroom_count.fillna(3,inplace = True)
    df.bathroom_count.fillna(2,inplace = True)
    # Drops all values that are still null
    df = df.dropna()
    df.drop(columns = ["Unnamed: 0"],inplace = True)
    df.fips = df.fips.astype("object")
    df.year_built = df.year_built.astype("object")

    # removes all the outliers that are out of the quartile range for the list of values given.
    df = remove_outliers(df, 1.5, ['bedroom_count', 'bathroom_count', 'area', 'tax_value', 'tax_amount'])

    # Splitting the data into train validate and test
    train_validate, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train_validate, test_size=.3, random_state=123)

    return train, validate, test