#%%
import json
import sqlite3
import pandas as pd

#%%
# Connect to database
db = sqlite3.connect('US_Covid.db')

# %%
c = db.cursor()

#%%

c.execute("""
    SELECT *
    FROM US_covid

""")
rez = c.fetchmany(20)
print(rez)

#%%
c.execute("""
    DROP TABLE US_covid
""")
#%%
db.commit()

#%%
import requests

#%%
# Database reset part: 1
url = "https://api.covidtracking.com/v1/states/daily.json"
req = requests.get(url)
reqData = req.json()

holdFrame = pd.DataFrame.from_dict(reqData)

holdFrame.to_sql('Update_DB', db, if_exists='replace', index=False)

#%%
# Database reset part: 2
c.execute("""
    CREATE TABLE US_Covid AS
    SELECT date, state, positive, negative, hospitalizedCurrently, hospitalizedCumulative, dataQualityGrade, death, hospitalized, positiveIncrease, negativeIncrease, total, deathIncrease, hospitalizedIncrease
    FROM Update_DB
""")

#%%
c.execute(""" 
    SELECT date, state, positiveIncrease
    FROM US_covid
    WHERE state == 'GA'
    ORDER BY date DESC;
    """)
results = c.fetchmany(5)
print(results)

#%%
c.execute(""" 
    SELECT date, state, positiveIncrease
    FROM US_covid
    WHERE state == 'GA' AND date == '20200918'
    ORDER BY date DESC;
    """)
checker = c.fetchall()
print(checker)


#%%
#c.execute("""
 #   DELETE FROM US_covid
  #  WHERE date == 20200918

#""")
#db.commit()

#%%
traffic = json.load(open("US_States_Covid.json"))
#%%
c.execute("""DROP TABLE us_covid;

    """)

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
states_covid.to_sql('us_covid',db,if_exists='append',index=False)

# %%
colNames = states_covid.columns

# %%
print(colNames)

# %%
c.execute("""SELECT state, positive
    FROM us_covid
    WHERE positive > 100000
    """)
dog = c.fetchmany(10)

for tooth in dog:
    print(tooth)
# %%
c.execute("""SELECT DISTINCT state
    FROM us_covid

""")
states = c.fetchall()

# %%
print(type(states))
print(type(states[0]))
print(states)


# %%
hold = []
for state in states:
    for st in state:
        hold.append(st)
print(hold)

# %%
print(len(hold))
print(hold)

# %%
print(hold[0])
print("This state: ", hold[0])

#%%
for i in hold:
    tableQuery = "CREATE TABLE %s_covid AS SELECT * FROM us_covid WHERE state == '%s'" % (i,i)
    c.execute(tableQuery)

# %%
c.execute("""
    SELECT *

    """)
