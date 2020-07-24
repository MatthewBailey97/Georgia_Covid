import requests, json
from datetime import date, datetime, timedelta
import os
import numpy as np
import pandas as pd

class CovidAPI:
    localData = ''
    baseURL = "https://covidtracking.com"
    USApi = "/api/v1/us/"
    statesApi = "/api/v1/states/"
    localDaily = ''
    localCurrent = ''
    localDay = ''

    #def __init__(self):
        
    def setDataPath(self, dataPath):
        #self.localData = pd.read_json(dataPath)
        with open(dataPath,"r+") as file:
            self.localData = json.load(file)

    #StateAbrv = State Abbreviation E.g. "ga", "ca"
    def requestStateDaily(self, stateAbrv):
        return self._requestData(self.baseURL+self.statesApi+stateAbrv.lower()+"/daily.json")
        

    #StateAbrv = State Abbreviation E.g. "ga", "ca"
    def requestStateCurrent(self, stateAbrv):
        return self._requestData(self.baseURL+self.statesApi+stateAbrv.lower()+"/current.json")
        

    def requestStateDate(self, stateAbrv, date):
        hDate = date.strftime("%Y%m%d")
        return self._requestData(self.baseURL+self.statesApi+stateAbrv.lower()+"/"+hDate+".json")

    def _requestData(self, url):
        req = requests.get(url)
        reqData = req.json()
        return reqData


    #Update locally stored JSON file
    def updateData(self, stateAbrv):
        dataHold = []
        localDate = self.localData[0]['date']

        newData = self.requestStateDaily(stateAbrv)

        #newData_Date = newData[0]['date']
        if newData[0]['date'] != localDate:
            for dic in newData: 
                if dic['date'] != localDate:
                    dataHold.append(dic)
                else:
                    break
                    
        updatedData = dataHold + self.localData

        with open("data/Georgia_Covid.json",'w') as outfile:
            json.dump(updatedData,outfile)
        
        #print(dataHold)
        #print(type(dataHold)
        #print(dataHold[0])
        #print(dataHold[-1])