# QuestDB - Timeseries example for trading data
  
Example project to load minute price data from github CSV files.  

# Prerequisites  
[Download QuestDB](https://questdb.io/download/) for windows  
Unzip the files downloaded  
No installation is required.

Note: for simplicity, move the unzipped files to c:\questdb, and create shortcut on your desktop for questdb.exe.  
  
# Running the server on local machine
Run the questdb server by launching: questdb.exe  (or your shortcut).  
Windows will raise an alert, clock More Info and run anyway.  
Keep this terminal window opened so the server can be accessed through "localhost:9000"  
(See bottom of this file for print screens)  

# Open the Quest DB Web Console  
Open your browser at
localhost:9000  
This will bring up the web console
![QuestDB Web Console](https://github.com/MapleFrogStudio/questdb_python/blob/main/images/questdbconsole.png "QuestDB Web Console")  
  
# Install project  
Project in an IDE (such as VS Code), open a terminal window
```
python -m venv env
.env\script\activate
pip install -r requirements.txt  
```  
# Running the project  
```
python build_db.py
```

# Print Screens  
![Windows Alert](https://github.com/MapleFrogStudio/questdb_python/blob/main/images/windows01.png "Windows Alert")  
![Run Anyway](https://github.com/MapleFrogStudio/questdb_python/blob/main/images/windows02.png "Run Anyway")  
![Allow Java](https://github.com/MapleFrogStudio/questdb_python/blob/main/images/javaallow.png "Allow access")  
![QuestDB Running](https://github.com/MapleFrogStudio/questdb_python/blob/main/images/serverrunning.png "Allow access")  
