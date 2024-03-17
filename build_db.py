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
    return data_df 

def main():
    data_df = pd.read_csv('data/amex1-2024-02-01.csv')
    data_df = format_data_for_questdb(data_df)     
    print(data_df)
    send_data(data_df)


if __name__ == '__main__':
    main()



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