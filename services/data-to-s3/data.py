import pandas as pd

def main():
    # Read New York Times COVID-19 Dataset from Github
    nytimes_df = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us.csv')

    # Convert datatype to date
    nytimes_df['date'] = pd.to_datetime(nytimes_df['date'])

    # Read John Hopkins COVID-19 dateset from Github
    jhopkins_df = pd.read_csv('https://raw.githubusercontent.com/datasets/covid-19/master/data/time-series-19-covid-combined.csv')

    # Delete 'Province/State', 'Confirmed' & 'Deaths' columns
    jhopkins_df = jhopkins_df.drop(['Province/State', 'Confirmed', 'Deaths'], axis=1)

    # Filter row where 'Country/Region' equal to 'US'
    jhopkins_df = jhopkins_df[jhopkins_df['Country/Region'] == 'US']

    # Delete 'Country/Region' column
    jhopkins_df = jhopkins_df.drop(['Country/Region'], axis=1)

    # Rename 'Date' to 'date' & 'Recovered' to 'recovered'
    jhopkins_df = jhopkins_df.rename(columns={'Date': 'date', 'Recovered': 'recovered'})

    # Convert data type to date
    jhopkins_df['date'] = pd.to_datetime(jhopkins_df['date'])
    
    # Convert data type to int
    jhopkins_df['recovered'] = jhopkins_df['recovered'].astype('int64')

    # Merge dataframes using date index
    df = pd.merge(nytimes_df, jhopkins_df, on ='date')

    return df