#%%
import requests, json
import sqlite3
import pandas as pd
# %%
db = sqlite3.connect('US_Covid.db')
c = db.cursor()
# %%
url = "https://api.covidtracking.com/v1/states/daily.json"
req = requests.get(url)
reqData = req.json()
# %%
holdFrame = pd.DataFrame.from_dict(reqData)
# %%
print(holdFrame.head)
# %%
holdFrame = holdFrame.dropna(axis='columns', how='all')
holdFrame = holdFrame.loc[:, (holdFrame != 0).any(axis=0)]
#%%
c.execute("SELECT date FROM US_covid ORDER BY date DESC LIMIT 1;")
lastDate = c.fetchone()[0]
print(lastDate)
#%%
newDataFrame = holdFrame[holdFrame['date'] > lastDate]
#%%
print(newDataFrame.head)
# %%
newDataFrame.to_sql('Update_DB',db,if_exists='replace',index=False)
# %%
#c.execute("SELECT date FROM US_covid LIMIT 1;")
#tester= c.fetchone()[0]
#print(tester)
# %%
#holdFrame.to_sql('US_covid',db,if_exists='replace',index=False)
# %%
#c.execute("SELECT DISTINCT state, dataQualityGrade FROM US_covid  WHERE dataQualityGrade LIKE'A%' GROUP BY state;")
#goodState = c.fetchall()
#print(goodState)

# %%
testingFrame = pd.read_sql_query("SELECT * FROM US_covid",db)

# %%
testingFrame.to_sql('Test_Frame',db,if_exists='replace',index=False)
# %%
c.execute("""
INSERT INTO Test_Frame
SELECT *
FROM Update_DB

""")
#%%
c.execute("DROP TABLE Test_Frame")
# %%
c.execute("""
INSERT INTO US_covid
SELECT * FROM US_covid
UNION
SELECT * FROM Update_DB

""")
unionTest = c.fetchall()
print(unionTest)
# %%
