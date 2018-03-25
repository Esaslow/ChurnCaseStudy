import pandas as pd
import numpy as np

from datetime import timedelta
import matplotlib.pyplot as plt
from importlib import reload
from src import cleaning as C
from sklearn.preprocessing import StandardScaler

def clean_city(df):

    """
    Input: DataFrame

    New columns, the 'city' column to dummy values
    New column, the 'city' column converted to integers

    Output: DataFrame
    """

    working_df = df.copy()

    # Duplcate, sacrifical 'city' column
    working_df['raw_city'] = working_df['city']

    # Make Dummy Columns
    new_df = pd.get_dummies(working_df, columns=['raw_city'], drop_first=True)

    # Rename dummy columns
    new_df_names = new_df.rename(index=str, \
        columns={"raw_city_King's Landing": "kings_landing",
                 "raw_city_Winterfell": "winterfell"})

    # Create column of city names mapped to numerical categories
    new_df_names['city_categories'] = \
        new_df_names['city'].map({'Astapor':1,
                                  'Winterfell':2,
                                  "King's Landing":3})

    return new_df_names

def add_target(df):
    '''
    INPUTS:
    df = data frame with col for last trip data that has last date as a
    pandas date time object
    -------------------
    OUTPUTS:
    df = data frame with col added called within_last 30 days
    Returns 1 if last ride was greater than 30 days away
    Returns 0 if last ride was less than 30 days
    1 => CHURN
    0 => NO CHURN
    '''
    working_df = df.copy()
    latest = max(working_df['last_trip_date'])
    Last_trip = (latest - working_df['last_trip_date'])
    within_last_30 = (Last_trip > timedelta(days = 30)) * 1
    working_df['within_last_30'] = within_last_30
    working_df['within_last_60'] = working_df['within_last_30']
    working_df.loc[Last_trip > timedelta(days = 60),'within_last_60'] = 2
    return working_df

def read_data(file_path):
    '''
    INPUTS:
    filepath: tells where the data is located in reference to the current
    directory

    OUTPUTS:
    Data frame that has the last trip date parsed for the last ride date
    and the signup date

    '''

    df = pd.read_csv(file_path,parse_dates= ['last_trip_date','signup_date'])
    return df

def clean_rtg_of_driver(df):
    '''
    Cleaning the 'rtg_of_driver' column and creating 3 new columns:
        1. Column where we replace all np.nan to the median.
        2. Column where we replace all np.nan to the mode.
        3. Column where we replace all np.nan to the mean.
        4. Column where we create a scaled version of original
           while replacing all np.nan to median.
    '''

    df_copy = df.copy()

    # Create column replacing np.nan to median.
    median = df_copy.avg_rating_of_driver.median()
    df_copy['avg_rating_of_driver_median'] = df_copy.avg_rating_of_driver.fillna(median)

    # Create column replacing np.nan to mode.
    mode = df_copy.avg_rating_of_driver.mode()[0]
    df_copy['avg_rating_of_driver_mode'] = df_copy.avg_rating_of_driver.fillna(mode)

    # Create column replacing np.nan to mean.
    mean = df_copy.avg_rating_of_driver.mean()
    df_copy['avg_rating_of_driver_mean'] = df_copy.avg_rating_of_driver.fillna(mean)

    # Normalized column based off median
    size = df_copy['avg_rating_of_driver_median'].shape[0]
    scaler = StandardScaler()
    df_copy['avg_rating_of_driver_normalized'] = (scaler.fit_transform(df_copy['avg_rating_of_driver_median']
                                                        .values.reshape(size,1)))

    return df_copy

def cleaning_avg_rating_by_driver(df):


    #make a copy of the dataframe
    df_copy = df.copy()

    # filling in Nans with column median
    rating_by_driver = df_copy['avg_rating_by_driver']
    median = df_copy['avg_rating_by_driver'].median()
    rating_by_driver_median = rating_by_driver.fillna(median)

    #create cleaned column
    df_copy['rating_by_driver_median'] = rating_by_driver_median

    # Normalized column based off median
    size = df_copy['rating_by_driver_median'].shape[0]
    scaler = StandardScaler()

    #scaler.fit
    df_copy['rating_by_driver_median_normalized'] = scaler.fit_transform(df_copy['rating_by_driver_median'].values.reshape(size,1))

    return df_copy



def clean_luxury_user(df):
    working_df = df.copy()
    ludf = working_df['luxury_car_user']
    num_ludf = ludf*1
    working_df['num_Luxury_User'] = num_ludf
    return working_df


def remove_july(df):
    working_df = df.copy()
    working_df = working_df.loc[working_df['last_trip_date'].dt.month != 7,:]

    return working_df

def plot_(df,target,ax):
    ax[0].hist(df.trips_in_first_30_days[target == 0],bins = list(np.linspace(0,20,50)),alpha = .6,label = 'no churn',normed = 1);
    ax[0].hist(df.trips_in_first_30_days[target == 1],bins = list(np.linspace(0,20,50)),alpha = .6,label = '30 day churn',normed = 1);
    ax[0].set_xlim([-1,20])
    ax[0].legend()
    ax[0].set_xlabel('Number of rides in the First 30 days')
    ax[0].set_ylabel('Normalized Count');
    ax[0].grid(alpha = .2,color = 'r',linestyle = '--')
    ax[0].set_title('Number of rides in First 30 days hist')
    ax[1].hist(df.weekday_pct[target == 0],alpha = .6,label = 'no churn',normed = 1);
    ax[1].hist(df.weekday_pct[target == 1],alpha = .6,label = '30 day churn',normed = 1);
    ax[1].set_xlim([-1,110])
    ax[1].legend()
    ax[1].set_xlabel('Week day Percent')
    ax[1].set_title('Weekday Percent hist')
    ax[1].grid(alpha = .2,color = 'r',linestyle = '--')
    ax[2].hist(df.surge_pct[target == 0],alpha = .6,label = 'no churn',normed = 1);
    ax[2].hist(df.surge_pct[target == 1],alpha = .6,label = '30 day churn',normed = 1);
    ax[2].set_xlim([-1,110])
    ax[2].legend()
    ax[2].set_xlabel('Surge Percent')
    ax[2].set_title('Surge Percent hist')
    ax[2].grid(alpha = .2,color = 'r',linestyle = '--')
    ax[3].hist(df.avg_dist[target == 0],bins = list(np.linspace(0,60,40)),alpha = .6,label = 'no churn',normed = 1);
    ax[3].hist(df.avg_dist[target == 1],bins = list(np.linspace(0,60,40)),alpha = .6,label = '30 day churn',normed = 1);
    ax[3].set_xlim([-1,40])
    ax[3].legend()
    ax[3].set_xlabel('Avg Distance')
    ax[3].set_title('Average Distance hist')
    ax[3].grid(alpha = .2,color = 'r',linestyle = '--')
    return ax
