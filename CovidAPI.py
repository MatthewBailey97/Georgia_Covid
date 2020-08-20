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

        
    def setDataPath(self, dataPath):
        """Function takes in path to json file and loads it for use

        Args:
            dataPath (String): filepath to data file
        """
        with open(dataPath,"r+") as file:
            self.localData = json.load(file)


    def requestStateDaily(self, stateAbrv):
        """Requests historical daily data

        Args:
            stateAbrv (String): State Abbreviation for API request E.g. "ga", "ca"

        Returns:
            Json: Returns request data in json format
        """
        return self._requestData(self.baseURL+self.statesApi+stateAbrv.lower()+"/daily.json")
        

    def requestStateCurrent(self, stateAbrv):
        """Requests most recent data values for a state, typically the values of the previous day

        Args:
            stateAbrv (String): State Abbreviation for API request E.g. "ga", "ca"

        Returns:
            Json: Returns request data in json format
        """
        return self._requestData(self.baseURL+self.statesApi+stateAbrv.lower()+"/current.json")
        

    def requestStateDate(self, stateAbrv, date):
        """Requests data values of a specific date for a state

        Args:
            stateAbrv (String): State Abbreviation for API request E.g. "ga", "ca"
            date (String): Date value that is then converted to string of digits E.g. "8/1/2020" to "20200801"

        Returns:
            Json: Returns request data in json format
        """
        hDate = date.strftime("%Y%m%d")
        return self._requestData(self.baseURL+self.statesApi+stateAbrv.lower()+"/"+hDate+".json")

    def requestAllStateDataCurrent(self):

        return self._requestData(self.baseURL+self.statesApi+"/current.json")

    def _requestData(self, url):
        """Handles data request functions for each requst function

        Args:
            url (String): Takes in string value for covidtracking.com api call

        Returns:
            Json: Returns request call in Json format
        """
        req = requests.get(url)
        reqData = req.json()
        return reqData


    def updateData(self, stateAbrv):
        """Keeps locally stored json file updated with most recent data values

        Args:
            stateAbrv (String): State Abbreviation for API request E.g. "ga", "ca"
        """
        dataHold = []
        localDate = self.localData[0]['date']

        newData = self.requestStateDaily(stateAbrv)

        if newData[0]['date'] != localDate:
            for dic in newData: 
                if dic['date'] != localDate:
                    dataHold.append(dic)
                else:
                    break
                    
        updatedData = dataHold + self.localData

        with open("Georgia_Covid.json",'w') as outfile:
            json.dump(updatedData,outfile)