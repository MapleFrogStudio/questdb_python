import sys
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import pandas as pd
import time
from datetime import datetime
from questdb.ingress import Sender, IngressError


HOST = 'localhost'
PORT = 9009
TABLE_NAME = 'data01'

def display_help():
    print(f'\n------------------ Build Quest DB - Help --------------------')
    print("Loading csv minute files from 'MapleFrogStudio' & 'PoivronJaune' github repos.")
    print("Please configure env variables as follows (using your specific installation values):")
    print("     QUESTDB_HOST    = '192.168.1.41'")
    print("     QUESTDB_API     = 9000")
    print("     QUESTDB_INGRESS = 9009")
    print("     QUESTDB_STATUS  = 9003")

def show_current_config():
    print(f'\n--------------------- Current Configuration --------------------')
    print(f'INGRESS PORT -> http://{HOST}:{PORT}, TARGET TABLE:{TABLE_NAME}')
    input('ENTER To start loading, CTRL-C to Quit')

def display_start_time():
    print(f'\n---------------------- Program Start ------------------------')
    start_datetime = datetime.now()
    current_tool = os.path.basename(__file__)
    print(f'{current_tool}: Start program {start_datetime.date().strftime("%Y-%m-%d")} at {start_datetime.time().strftime("%H:%M:%S")}')
    return start_datetime

def display_end_time(start_datetime):
    print(f'\n---------------------- Program End ---------------------------')
    end_datetime = datetime.now()
    current_tool = os.path.basename(__file__)
    print(f'{current_tool}: End program {end_datetime.date().strftime("%Y-%m-%d")} at {end_datetime.time().strftime("%H:%M:%S")}')
    time_difference = end_datetime - start_datetime
    print("Execution duration:", time_difference.days, "days,", 
                                 time_difference.seconds // 3600, "hours,",
                                 (time_difference.seconds // 60) % 60, "minutes,",
                                 time_difference.seconds % 60, "seconds")    

def check_health():
    print(f'\n------------------- QUest DB Health Check --------------------')
    res = requests.get(f'http://{HOST}:{STATUS}')
    print(f'{res.text}')

def send_data(data_df):
    host = HOST
    port = PORT
    db = TABLE_NAME

    print(f'DEBUG: {data_df.columns}')
    print(data_df)

    try:
        with Sender(host, port) as sender:
            sender.dataframe(
                data_df,
                table_name='build',  # Table name to insert into.
                symbols=['Symbol'],  # Columns to be inserted as SYMBOL types.
                at='Datetime')  # Column containing the designated timestamps.
    except IngressError as e:
        print(f'Got error: {e}\n')

def format_data_for_questdb(data_df):
    data_df['Datetime'] = pd.to_datetime(data_df['Datetime'])
    data_df['Open'] = data_df['Open'].astype(float).round(2)
    data_df['High'] = data_df['High'].astype(float).round(2)
    data_df['Low'] = data_df['Low'].astype(float).round(2)
    data_df['Close'] = data_df['Close'].astype(float).round(2)
    data_df['Volume'] = data_df['Volume'].astype(int)   
    return data_df 

def main():
    print(f'\n--------------- MAIN DB Build program running ----------------')
    owner = 'MapleFrogStudio'
    repo = 'DATA-2023-03'
    g = Github(owner=owner, repository=repo)
    json_list = g.repo_content(folder='/')
    files = g.select_files(json_list, starts_with='')

    for index, raw_url in enumerate(files[0:1]):
        data_df = g.load_ohlcv_csv(raw_url)
        data_df = format_data_for_questdb(data_df)     
        print(f"{index+1}/{len(files)} [Symbols:{len(data_df.Symbol.unique())}, Rows:{len(data_df)}]: {raw_url}")
        send_data(data_df)

    # Load repo files
    # loop through file to load them
    # save them to QuestDB

if __name__ == '__main__':
    display_help()
    show_current_config()
    start = display_start_time()
    check_health()
    
    main()
    
    display_end_time(start)



# SQL TO Create Quest_DB database that prevents duplicates on Datetime+Symbol
    
# CREATE TABLE 'build' (
#   Symbol SYMBOL capacity 256 CACHE,
#   Close DOUBLE,
#   High DOUBLE,
#   Low DOUBLE,
#   Open DOUBLE,
#   Volume LONG,
#   'Adj Close' DOUBLE,
#   Datetime TIMESTAMP
# ) timestamp (Datetime) PARTITION BY DAY WAL
# DEDUP UPSERT KEYS(Datetime, Symbol);