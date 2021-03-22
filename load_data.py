import time
import pandas as pd
import numpy as np
import calendar as cl
import os

DATA_CITY = { 'All' : 'all',
              'Chicago': 'chicago.csv',
              'New york': 'new_york_city.csv',
              'Washington': 'washington.csv' }

DATA_Month = {
    0: 'All', 
    1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun',
    7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}

DATA_Day = ['All'] + [d[0:3] for d in cl.day_name]


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Read data from csv file that represent the city 
    print("Loading {} city database to view {} month(s) and {} day(s).".format(city,month.lower(),day),end="")
    df = pd.read_csv("{}\\bikeshare-2\\{}".format(os.getcwd(),DATA_CITY['Chicago']),parse_dates=['Start Time','End Time'])
    print(".",end="")
    df['Month'] = [m[0:3] for m in df['Start Time'].dt.month_name()]
    print(".",end="")
    df['Day'] = [d[0:3] for d in df['Start Time'].dt.day_name()]
    print(".",end="")
    df['Start Hour'] = df['Start Time'].dt.hour
    print(".",end="")
    # Load Special
    df = df[(df.Day == (df.Day if day.lower()== 'all' else day)) & (df.Month == (df.Month if month.lower()=="all" else month))]    
    print(".")
    
    return df

get_filters = ('Chicago', 'All', 'Sat')

load_data(*get_filters)