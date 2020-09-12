#%%
import requests, json
import sqlite3
import pandas as pd


#%%
# Connect to database
db = sqlite3.connect('US_Covid.db')

#%%
c = db.cursor()
# %%
url = "https://api.covidtracking.com/v1/states/daily.json"
req = requests.get(url)
reqData = req.json()

#%%
print(type(reqData))

#%%
testFrame = pd.DataFrame.from_dict(reqData)

#%%
print(testFrame.shape)

#

#%%
df = pd.read_json

#%%
dataHold = []

#%%
c.execute("SELECT date FROM GA_Covid")
lastDate = c.fetchone()[0]
print(lastDate)

#%%
print(reqData[0]['date'])

#%%
#recentDate = reqData[0]['date']
for dic in reqData:
    if dic['date'] != lastDate:
        dataHold.append(dic)
    else:
        break

#%%
print(dataHold)

#%%
df = pd.DataFrame(dataHold)

#%%
print(df.head)
#%%
df = df.dropna(axis='columns', how='all')
df = df.loc[:, (df != 0).any(axis=0)]
#%%
print(df.to_sql("us_covid",db,if_exists='append', index=False))


#%%
print()

#%%
c.execute(""" 
    SELECT totalTestEncountersViral
    FROM us_covid
    """)
results = c.fetchmany(10)




#%%
print(type(results))
print(type(results[0]))
print(results)


# %%
import pandas as pd

# %%
states_covid = pd.read_json("US_States_Covid.json")

# %%
print(states_covid.columns)

#%%
states_covid = states_covid.dropna(axis='columns', how='all')
states_covid = states_covid.loc[:, (states_covid != 0).any(axis=0)]

# %%
states_covid.to_sql('US_covid',db,if_exists='replace',index=False)

# %%
colNames = states_covid.columns
