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
    SELECT date, hospitalizedCumulative
    FROM CA_covid
    


    """)
results = c.fetchmany(10)




#%%
print(type(results))
print(type(results[0]))
print(results)
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
