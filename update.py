import requests, json
import sqlite3
import pandas as pd

#Create Database Connection and Cursor
db = sqlite3.connect('US_Covid.db')
c = db.cursor()

#Retrieve covid Data
url = "https://api.covidtracking.com/v1/states/daily.json"
req = requests.get(url)
reqData = req.json()

#Read data into Pandas DataFrame and drop empty columns
holdFrame = pd.DataFrame.from_dict(reqData)
holdFrame = holdFrame.dropna(axis='columns', how='all')
holdFrame = holdFrame.loc[:, (holdFrame != 0).any(axis=0)]

#Retrieve most recent record date 
c.execute("SELECT date FROM US_covid ORDER BY date DESC LIMIT 1;")
lastDate = c.fetchone()[0]

#Slice holdFrame and retrieve all records after lastDate
newDataFrame = holdFrame[holdFrame['date'] > lastDate]
newDataFrame.to_sql('Update_DB',db,if_exists='replace',index=False)

c.execute("""
INSERT INTO US_covid
SELECT * FROM US_covid
UNION
SELECT * FROM Update_DB

""")
db.commit()
c.close()


