from django.db import models
from selenium import webdriver
import pandas as pd
import time
import json
import datetime

# Create your models here.
class tashuCrawler:
    def currentStatusCrawler():
        url = "https://www.tashu.or.kr/userpage/station/mapStatus.jsp?flg=main"
        # execute chrome incogino mode
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        driver = webdriver.Chrome("linux_chrome_driver/chromedriver", chrome_options=chrome_options)

        ## connect to tashu web server
        driver.get(url)
        stationStatus = []
        #jsSourcecode = ("var strData;"+
        #	"strData = GDownloadUrl('/mapAction.do?process=statusMapView',"+
        #	" function(data, responseCode) {return data;}); ")

        jsSourcecode = ("var strData;"+
        "GDownloadUrl('/mapAction.do?process=statusMapView',"+
        "function(data, response){ dataDiv = document.createElement('div');"+
        "dataDiv.setAttribute('id', 'dataDiv');dataDiv.innerHTML = data;"+
        "document.body.appendChild(dataDiv);}); ")

        data = driver.execute_script(jsSourcecode)

        time.sleep(10)
        dataDIV = driver.find_element_by_id('dataDiv')
        dataTxt = dataDIV.text

        return dataTxt

    def parseData(data):
        jsonData = json.loads(data)
        stationData = jsonData['markers']
        returnDF = pd.DataFrame()

        currentDateTime = datetime.datetime.now()
        currentDateTime = datetime.datetime(currentDateTime.year, currentDateTime.month, currentDateTime.day, currentDateTime.hour)

        for station in stationData:
            stationNum = int(station['kiosk_no'])
            cntRackTotal = 0
            cntRentable = 0

            if stationNum > 0 and stationNum < 145:
                cntRackTotal = int(station['cntRackTotal'])
                cntRentable = int(station['cntRentable'])
                kiosk_no = int(station['kiosk_no'])
                returnDF = returnDF.append({'currentDateTime':currentDateTime, 'kiosk_no':stationNum, 'currentRentable':cntRentable, 'currentRackTotal':cntRackTotal},ignore_index=True)

        return returnDF
