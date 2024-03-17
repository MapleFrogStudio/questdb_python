# QuestDB - Timeseries example for trading data
  
Example project to load minute price data from github CSV files.  

# Prerequisites  
[Download QuestDB](https://questdb.io/download/) for windows  
Unzip the files downloaded  
No installation is required.

Note: for simplicity, move the unzipped files to c:\questdb, and create shortcut on your desktop for questdb.exe.  
  
# Running the server on local machine
Run the questdb server by launching: questdb.exe  (or your shortcut).  
Windows will raise an alert,  
Click on the **"More Info"** button,  
Then click on **"Run anyway"**.  
Keep this terminal window opened so the server can run in the background at **"localhost:9000"**  
(See bottom of this file for print screens of windows alert windows)  

# Open the Quest DB Web Console  
Open your browser at
localhost:9000  
This will bring up the web console
![QuestDB Web Console](https://github.com/MapleFrogStudio/questdb_python/blob/main/images/questdbconsole.png "QuestDB Web Console")  

# Create the target database 
To store minute price data, we want a structured time series database that will prevent duplicate entries for a datetime+ticker.  
In the web console, run the following SQL Script
```
CREATE TABLE 'minute' (
  Ticker SYMBOL capacity 256 CACHE,
  Close DOUBLE,
  High DOUBLE,
  Low DOUBLE,
  Open DOUBLE,
  Volume LONG,
  'Adj Close' DOUBLE,
  Datetime TIMESTAMP
) timestamp (Datetime) PARTITION BY DAY WAL
DEDUP UPSERT KEYS(Datetime, Ticker);
```  
This will create a table with Open, High, Low, Close, Volume and 'Adj Close' columns. The Datetime column will be the timestamp required by any timeseries database and the ticker will be a special type of column to manage our duplicates (read the docs on QuestDB for more explanations).

# Install project  
Clone thos project to your local machine.  
Open the project in an IDE (such as VS Code), with a terminal window:
```
python -m venv env
.env\script\activate
pip install -r requirements.txt  
```  
# Running the project  
```
python build_db.py
```

# Configuration  
Script build_db.py has two main functions.  
**main()**  
Loads a csv file from local data folder and sends it to QuestDB  
  
**main2()**  
raw_url : list of links to online csv files (github for example)  
loop : iterates through this list to download, structure data and load to questdb  
***Update this list with your prefered data files***

# Print Screens  
![Windows Alert](https://github.com/MapleFrogStudio/questdb_python/blob/main/images/windows01.png "Windows Alert")  
![Run Anyway](https://github.com/MapleFrogStudio/questdb_python/blob/main/images/windows02.png "Run Anyway")  
![Allow Java](https://github.com/MapleFrogStudio/questdb_python/blob/main/images/javaallow.png "Allow access")  
![QuestDB Running](https://github.com/MapleFrogStudio/questdb_python/blob/main/images/serverrunning.png "Allow access")  
