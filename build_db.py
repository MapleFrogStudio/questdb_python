# SQL TO Create Quest_DB database that prevents duplicates on Datetime+Symbol
# CREATE TABLE 'build' (
#   Ticker SYMBOL capacity 256 CACHE,
#   Close DOUBLE,
#   High DOUBLE,
#   Low DOUBLE,
#   Open DOUBLE,
#   Volume LONG,
#   'Adj Close' DOUBLE,
#   Datetime TIMESTAMP
# ) timestamp (Datetime) PARTITION BY DAY WAL
# DEDUP UPSERT KEYS(Datetime, Ticker);

import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import requests
from questdb.ingress import Sender, IngressError

HOST = 'localhost'
PORT = 9009
TABLE_NAME = 'minute'

def send_data(data_df):
    try:
        with Sender(HOST, PORT) as sender:
            sender.dataframe(
                data_df,
                table_name=TABLE_NAME,  # Table name to insert into.
                symbols=['Ticker'],  # Columns to be inserted as SYMBOL types.
                at='Datetime')  # Column containing the designated timestamps.
    except IngressError as e:
        print(f'QuestDB Error: {e}\n')

def format_data_for_questdb(data_df):
    data_df['Datetime'] = pd.to_datetime(data_df['Datetime'])
    data_df['Open'] = data_df['Open'].astype(float).round(2)
    data_df['High'] = data_df['High'].astype(float).round(2)
    data_df['Low'] = data_df['Low'].astype(float).round(2)
    data_df['Close'] = data_df['Close'].astype(float).round(2)
    data_df['Volume'] = data_df['Volume'].astype(int)   

    if 'Symbol' in data_df.columns:
        data_df = data_df.rename({'Symbol':'Ticker'})

    return data_df 

def main():
    """Laod price data from local csv file..."""
    data_df = pd.read_csv('data/amex1-2024-02-01.csv')
    data_df = format_data_for_questdb(data_df)     
    print(data_df)
    send_data(data_df)

def main2():
    """Load price data from github csv files..."""
    raw_urls = [
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-04.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-05.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-06.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-07.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-08.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-09.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-10.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-11.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-12.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-13.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-14.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-15.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-16.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-17.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-18.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-19.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-20.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-21.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-22.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-23.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-24.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-25.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-26.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-27.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-28.csv',
        'https://raw.githubusercontent.com/MapleFrogStudio/DATA-2024-02/main/amex1-2024-02-29.csv',
    ]
    for url in raw_urls:
        data_df = pd.read_csv(url)
        data_df = format_data_for_questdb(data_df)     
        send_data(data_df) 
        print(f'[Unique Symbols:{len(data_df.Ticker.unique())}],[Records:{len(data_df)}]{url}')



if __name__ == '__main__':
    #main()
    main2()
