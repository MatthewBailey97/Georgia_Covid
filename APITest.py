#%%
import CovidAPI as ca
from datetime import date, datetime, timedelta

#%%
newRun = ca.CovidAPI()

#%%
newRun.setDataPath("Georgia_Covid.json")

#%%
newRun.updateData("ga")

#%%
print(type(newRun.localData))

#%%
print(type(newRun.localData[0]))
#%%
print(newRun.localData[0]['date'])

#%%
currentData = newRun.requestStateCurrent("ga")

#%%
currentData

#%%
tdy = datetime.today()
tdy

#%%
testDate = 20200708
#%%
print(tdy-datetime.strptime(str(testDate),"%Y%m%d"))#datetime.strptime(str(currentData['date']),"%Y%m%d"))

#%%
