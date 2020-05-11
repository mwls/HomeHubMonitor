# Program to monitor my Virgin Home Hub
# written by Matthew Smith April 2020

# import modules 
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import datetime
import pause
import pickle
import os
import numpy as np
import speedtest

# select data file
saveDataFile = "D:\\hubData\\hubDataInfo.pkl"

#####################################################################################

# select url for status data
url = "http://192.168.0.1/getRouterStatus?"

# ID key
downstreamID = "1.3.6.1.2.1.10.127.1.1.1.1"
downstreamID2 = "1.3.6.1.2.1.10.127.1.1.4.1"
upstreamID = "1.3.6.1.2.1.10.127.1.1.2.1"
upstreamID2 = "1.3.6.1.4.1.4491.2.1.20.1.2.1"

# time between hub check (minutes)
hubCheckDeltaT = 5.0

# speed check interval (in units of hubCheck)
speedCheckInt = 4

#####################################################################################

# function to check router info
def hubChecker(url, storeData, downstreamID, downstreamID2, upstreamID, upstreamID2):

    # get response from url
    response = requests.get(url)
    
    # get current time
    nowTime = datetime.datetime.now()
    
    # use beautiful sour to parse the text
    soupData = BeautifulSoup(response.text, "html.parser")
    
    # add time to time array
    storeData["time"] = np.append(storeData["time"], nowTime)
    
    
    # get text and split by line
    allData = soupData.text
    allDataLines = allData.splitlines() 
    
    # remove "{" from firstl line
    allDataLines[0] = allDataLines[0][1:]
    
    # loop over each line to extract info
    data = {}
    for line in allDataLines:
        # skip final line
        if line.count("}"):
            continue
        
        # create dictionary store
        key = line.split(":")[0][1:-1]
        value = line.split(":")[1][1:-2]
        
        # save value to dictionary
        data[key] = value
    
    
    ## get downstream information
    # down info
    downInfo = {}
    possibleIDs = [i for i in range(1,37)]
    # possible 24 channels locked in so loop over each one
    for i in range(1,25):
        
        # see if key exists
        if downstreamID + ".1." + str(i) in data.keys():
            # extract necessary values out
            chanID = int(data[downstreamID + ".1." + str(i)])
            chanFreq = float(data[downstreamID + ".2." + str(i)])
            chanMode = int(data[downstreamID + ".4." + str(i)])
            chanPower = float(data[downstreamID + ".6." + str(i)]) / 10.0
                              
            # other data table
            chanPreRS = int(data[downstreamID2 + ".3." + str(i)])
            chanPostRS = int(data[downstreamID2 + ".4." + str(i)])
            chanSNR = float(data[downstreamID2 + ".5." + str(i)]) / 10.0
            
        
            # save this value to the stored arrays
            storeData["downStream"][chanID]["freq"] = np.append(storeData["downStream"][chanID]["freq"], chanFreq)
            storeData["downStream"][chanID]["mode"] = np.append(storeData["downStream"][chanID]["mode"], chanMode)
            storeData["downStream"][chanID]["power"] = np.append(storeData["downStream"][chanID]["power"], chanPower)
            storeData["downStream"][chanID]["preRS"] = np.append(storeData["downStream"][chanID]["preRS"], chanPreRS)
            storeData["downStream"][chanID]["postRS"] = np.append(storeData["downStream"][chanID]["postRS"], chanPostRS)
            storeData["downStream"][chanID]["SNR"] = np.append(storeData["downStream"][chanID]["SNR"], chanSNR)
        
            # pop this chanID from possibleIDS
            possibleIDs.remove(chanID)
    
    # loop over the other possible chanels and add nans
    for chanID in possibleIDs:
        storeData["downStream"][chanID]["freq"] = np.append(storeData["downStream"][chanID]["freq"], np.nan)
        storeData["downStream"][chanID]["mode"] = np.append(storeData["downStream"][chanID]["mode"], np.nan)
        storeData["downStream"][chanID]["power"] = np.append(storeData["downStream"][chanID]["power"], np.nan)
        storeData["downStream"][chanID]["preRS"] = np.append(storeData["downStream"][chanID]["preRS"], np.nan)
        storeData["downStream"][chanID]["postRS"] = np.append(storeData["downStream"][chanID]["postRS"], np.nan)
        storeData["downStream"][chanID]["SNR"] = np.append(storeData["downStream"][chanID]["SNR"], np.nan)
    
    
    ## get upstream infomration
    upInfo = {}
    possibleIDs = [i for i in range(1,6)]
    # possible 5 channels upstream 
    for i in range(1,5):
         # see if key exists
        if upstreamID + ".1." + str(i) in data.keys():
            # extract necessary values out
            chanID = int(data[upstreamID + ".1." + str(i)])
            chanFreq = float(data[upstreamID + ".2." + str(i)])
            chanMode = int(data[upstreamID + ".15." + str(i)])
            chanPower = float(data[upstreamID2 + ".1." + str(i)]) 
            
        
            # save this value to the stored arrays
            storeData["upStream"][chanID]["freq"] = np.append(storeData["upStream"][chanID]["freq"], chanFreq)
            storeData["upStream"][chanID]["mode"] = np.append(storeData["upStream"][chanID]["mode"], chanMode)
            storeData["upStream"][chanID]["power"] = np.append(storeData["upStream"][chanID]["power"], chanPower)
        
            # pop this chanID from possibleIDS
            possibleIDs.remove(chanID)
    
    # loop over the other possible chanels and add nans
    for chanID in possibleIDs:
        storeData["upStream"][chanID]["freq"] = np.append(storeData["upStream"][chanID]["freq"], np.nan)
        storeData["upStream"][chanID]["mode"] = np.append(storeData["upStream"][chanID]["mode"], np.nan)
        storeData["upStream"][chanID]["power"] = np.append(storeData["upStream"][chanID]["power"], np.nan)
    
    return storeData
            
#####################################################################################

# run speed test and store
def runSpeedTest(storeData, pingOnly=False):
    
    # run and configure speed test
    s = speedtest.Speedtest()
    s.get_servers()
    s.get_best_server()
    if pingOnly is False:
        s.download()
        s.upload()
    
    # get results
    res = s.results.dict()
    
    # add results to store data
    storeData["speed"]["ping"] = np.append(storeData["speed"]["ping"], res["ping"])
    if pingOnly:
        storeData["speed"]["download"] = np.append(storeData["speed"]["download"], np.nan)
        storeData["speed"]["upload"] = np.append(storeData["speed"]["upload"], np.nan)
    else:
        storeData["speed"]["download"] = np.append(storeData["speed"]["download"], res["download"]/1e6)
        storeData["speed"]["upload"] = np.append(storeData["speed"]["upload"], res["upload"]/1e6)
        
    return storeData

#####################################################################################


# see if pickle file exists, if so load otherwise create blank array
if os.path.isfile(saveDataFile):
    # load in stored data
    fileIn = open(saveDataFile,'rb')
    storeData = pickle.load(fileIn)
    fileIn.close()
    
else:
    # create empty storage arrays
    storeData = {}
    storeData["time"] = []
    storeData["downStream"] = {}
    # assume they could be 36 channels think this is high
    for i in range(1,37):
        storeData["downStream"][i] = {"freq":np.array([]), "mode":np.array([]), "power":np.array([]), "preRS":np.array([]), "postRS":np.array([]), "SNR":np.array([])}
    # add in upstream information (max of 4)
    storeData["upStream"] = {}
    for i in range(1,6):
        storeData["upStream"][i] = {"freq":np.array([]), "power":np.array([]), "mode":np.array([])}
    # add in speed test data
    storeData["speed"] = {"download":np.array([]), "upload":np.array([]), "ping":np.array([])}

speedI = 0
keepProcessing = True
while keepProcessing is True:
    print("Performing Test: ", datetime.datetime.now())
    
    # ask hub for information
    storeData = hubChecker(url, storeData, downstreamID, downstreamID2, upstreamID, upstreamID2)
    
    # see if time to run speedtest
    if speedI == 0:
        try:
            storeData = runSpeedTest(storeData)
        #except speedtest.ConfigRetrievalError:
        #    storeData["speed"]["download"] = np.append(storeData["speed"]["download"], 0.0)
        #    storeData["speed"]["upload"] = np.append(storeData["speed"]["upload"], 0.0)
        #    storeData["speed"]["ping"] = np.append(storeData["speed"]["ping"], np.nan)
        except:
            storeData["speed"]["download"] = np.append(storeData["speed"]["download"], 0.0)
            storeData["speed"]["upload"] = np.append(storeData["speed"]["upload"], 0.0)
            storeData["speed"]["ping"] = np.append(storeData["speed"]["ping"], np.nan)
    else:
        try:
            storeData = runSpeedTest(storeData, pingOnly=True)
        except:
            storeData["speed"]["download"] = np.append(storeData["speed"]["download"], 0.0)
            storeData["speed"]["upload"] = np.append(storeData["speed"]["upload"], 0.0)
            storeData["speed"]["ping"] = np.append(storeData["speed"]["ping"], np.nan)
        
    
    speedI = speedI + 1
    if speedI == speedCheckInt - 1:
        speedI = 0
    
    # save data to file
    fileOut = open(saveDataFile, 'wb')
    pickle.dump(storeData, fileOut)
    fileOut.close()
    
    # update graphs
    
    # pause until required
    pause.minutes(hubCheckDeltaT)
    
    



           
     