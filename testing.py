#%%
import CovidAPI as ca
import requests, json

# %%
url = "https://api.covidtracking.com/v1/states/daily.json"
req = requests.get(url)
reqData = req.json()


# %%
with open("US_States_Covid.json",'w') as outfile:
            json.dump(reqData,outfile)

# %%
traffic = json.load(open("US_States_Covid.json"))

# %%
someitem = traffic[0].keys()


# %%
print(someitem)

# %%
