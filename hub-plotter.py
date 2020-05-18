# Program to monitor my Virgin Home Hub
# written by Matthew Smith April 2020

# import modules
import os 
import pickle
import numpy as np
import matplotlib.pyplot as plt

# select data file
dataFile = "D:\\hubData\\hubDataInfo.pkl"



#####################################################################################

# downstream power levels
standardDownLevels = {"acceptable":[-6, 10], "optimal":[-3,8]}

# downstream SNR levels
standardDownSNR = {"acceptable":34, "optimal":34.5}

# upstream power levels
standardUpLevels = {"acceptable":[31,51], "optimal":[38,48]}

# expected internetspeed
expectedSpeed = {"download":100, "upload":10}

#####################################################################################


# get data
filein = open(dataFile,'rb')
data = pickle.load(filein)
filein.close()

# extract wanted informaation
time = data['time']

# select down points from ping data
downPoints = np.where(np.isnan(data["speed"]["ping"]) == True)

## see if the program missed out parts
# calculate median time between points
deltaT = time[1:] - time[:-1]
medianDeltaT = np.median(deltaT)
splitPoints = np.where(deltaT > 2.0*medianDeltaT)[0]
splitPoints = np.append(np.array([-1]), splitPoints)
splitPoints = np.append(splitPoints+1, len(time))


fig = plt.figure(figsize=(16,12))



f8 = plt.axes([0.54,0.765,0.45,0.225])
for i in range(1,len(splitPoints)):
    plt.gca().set_prop_cycle(None)
    for key in data["downStream"]:
        f8.plot(time[splitPoints[i-1]:splitPoints[i]], data["downStream"][key]["SNR"][splitPoints[i-1]:splitPoints[i]])
f8.set_ylabel("Downstream SNR (dB)")
f8.minorticks_on()
f8.tick_params(axis='both', direction='in', which='both')
f8.tick_params(top=True, right=True, which='both')
f8.tick_params(labelbottom='off')
xlims = f8.get_xlim()
for i in range(0,2):
    f8.plot([xlims[0], xlims[1]], [standardDownSNR["acceptable"], standardDownSNR["acceptable"]], '--', color='red')
    f8.plot([xlims[0], xlims[1]], [standardDownSNR["optimal"], standardDownSNR["optimal"]], '--', color='green')
f8.set_xlim(xlims[0], xlims[1])

f1 = plt.axes([0.04,0.06,0.45,0.225])
# calculate pre-RS values in each bin
for i in range(1,len(splitPoints)):
    plt.gca().set_prop_cycle(None)
    for key in data["downStream"]:   
        xpoints = np.array([])
        ypoints = np.array([])
        for j in range(splitPoints[i-1]+1, splitPoints[i]):
            if data["downStream"][key]["preRS"][j] - data["downStream"][key]["preRS"][j-1] < 0:
                preRS = data["downStream"][key]["preRS"][j] / ((time[j] - time[j-1]).total_seconds()/60.)
            else:
                preRS = (data["downStream"][key]["preRS"][j] - data["downStream"][key]["preRS"][j-1]) / ((time[j] - time[j-1]).total_seconds()/60.)
            xpoints = np.append(xpoints, time[j-1])
            ypoints = np.append(ypoints, preRS)
            xpoints = np.append(xpoints, time[j])
            ypoints = np.append(ypoints, preRS)
        f1.plot(xpoints, ypoints)
f1.set_yscale('log')
f1.set_ylabel("Pre-RS Errors (per min)")
f1.minorticks_on()
f1.tick_params(axis='both', direction='in', which='both')
f1.tick_params(top=True, right=True, which='both')
f1.set_xlabel("Time")
for label2 in f1.get_xticklabels():
    label2.set_ha("right")
    label2.set_rotation(30)

f2 = plt.axes([0.04,0.295,0.45,0.225])
# calculate pre-RS values in each bin
for i in range(1,len(splitPoints)):
    plt.gca().set_prop_cycle(None)
    for key in data["downStream"]:   
        xpoints = np.array([])
        ypoints = np.array([])
        for j in range(splitPoints[i-1]+1, splitPoints[i]):
            if data["downStream"][key]["postRS"][j] - data["downStream"][key]["postRS"][j-1] < 0:
                preRS = data["downStream"][key]["postRS"][j]/ ((time[j] - time[j-1]).total_seconds()/60.)
            else:
                preRS = (data["downStream"][key]["postRS"][j] - data["downStream"][key]["postRS"][j-1])/ ((time[j] - time[j-1]).total_seconds()/60.)
            xpoints = np.append(xpoints, time[j-1])
            ypoints = np.append(ypoints, preRS)
            xpoints = np.append(xpoints, time[j])
            ypoints = np.append(ypoints, preRS)
        f2.plot(xpoints, ypoints)
f2.set_yscale('log')
f2.set_ylabel("Post-RS Errors (per min)")
f2.minorticks_on()
f2.tick_params(axis='both', direction='in', which='both')
f2.tick_params(top=True, right=True, which='both')
f2.tick_params(labelbottom='off')

f3 = plt.axes([0.04,0.53,0.45,0.225])
for i in range(0,2):
    f3.plot([xlims[0], xlims[1]], [standardUpLevels["acceptable"][i], standardUpLevels["acceptable"][i]], '--', color='red')
    f3.plot([xlims[0], xlims[1]], [standardUpLevels["optimal"][i], standardUpLevels["optimal"][i]], '--', color='green')
for i in range(1,len(splitPoints)):
    plt.gca().set_prop_cycle(None)
    for key in data["upStream"]:
        f3.plot(time[splitPoints[i-1]:splitPoints[i]], data["upStream"][key]["power"][splitPoints[i-1]:splitPoints[i]])
f3.set_ylabel("Upstream Power (dBmV)")
f3.minorticks_on()
f3.tick_params(axis='both', direction='in', which='both')
f3.tick_params(top=True, right=True, which='both')
f3.tick_params(labelbottom='off')



f4 = plt.axes([0.04,0.765,0.45,0.225])
for i in range(0,2):
    f4.plot([xlims[0], xlims[1]], [standardDownLevels["acceptable"][i], standardDownLevels["acceptable"][i]], '--', color='red')
    f4.plot([xlims[0], xlims[1]], [standardDownLevels["optimal"][i], standardDownLevels["optimal"][i]], '--', color='green')
for i in range(1,len(splitPoints)):
    plt.gca().set_prop_cycle(None)
    for key in data["downStream"]:
        f4.plot(time[splitPoints[i-1]:splitPoints[i]], data["downStream"][key]["power"][splitPoints[i-1]:splitPoints[i]])
f4.set_ylabel("Downstream Power (dBmV)")
f4.minorticks_on()
f4.tick_params(axis='both', direction='in', which='both')
f4.tick_params(top=True, right=True, which='both')
f4.tick_params(labelbottom='off')






f5 = plt.axes([0.54,0.06,0.45,0.225])
for i in range(1,len(splitPoints)):
    plt.gca().set_prop_cycle(None)
    maxSel = np.where((np.isnan(data["speed"]["ping"][splitPoints[i-1]:splitPoints[i]]) == False) & (data["speed"]["ping"][splitPoints[i-1]:splitPoints[i]] > 200))
    plotPoints =  data["speed"]["ping"][splitPoints[i-1]:splitPoints[i]]
    plotPoints[maxSel] = 200
    f5.plot(time[splitPoints[i-1]:splitPoints[i]], plotPoints)
f5.set_ylabel("Ping (ms)")
f5.minorticks_on()
f5.tick_params(axis='both', direction='in', which='both')
f5.tick_params(top=True, right=True, which='both')
f5.set_xlabel("Time")
for label in f5.get_xticklabels():
    label.set_ha("right")
    label.set_rotation(30)
ylims = f5.get_ylim()
if ylims[1] > 200:
    f5.set_ylim(ylims[0], 200)


f6 = plt.axes([0.54,0.295,0.45,0.225])
for i in range(0,2):
    f6.plot([xlims[0], xlims[1]], [0.0,0.0], '--', color='red')
    f6.plot([xlims[0], xlims[1]], [expectedSpeed["upload"], expectedSpeed["upload"]], '--', color='green')
for i in range(1,len(splitPoints)):
    plt.gca().set_prop_cycle(None)
    sel = np.where(np.isnan(data["speed"]["upload"][splitPoints[i-1]:splitPoints[i]]) == False)
    f6.plot(time[splitPoints[i-1]:splitPoints[i]][sel], data["speed"]["upload"][splitPoints[i-1]:splitPoints[i]][sel])
f6.set_ylabel("Upload Speed (mbps)")
f6.minorticks_on()
f6.tick_params(axis='both', direction='in', which='both')
f6.tick_params(top=True, right=True, which='both')
f6.tick_params(labelbottom='off')


f7 = plt.axes([0.54,0.53,0.45,0.225])
for i in range(0,2):
    f7.plot([xlims[0], xlims[1]], [0.0,0.0], '--', color='red')
    f7.plot([xlims[0], xlims[1]], [expectedSpeed["download"], expectedSpeed["download"]], '--', color='green')
for i in range(1,len(splitPoints)):
    plt.gca().set_prop_cycle(None)
    sel = np.where(np.isnan(data["speed"]["download"][splitPoints[i-1]:splitPoints[i]]) == False)
    f7.plot(time[splitPoints[i-1]:splitPoints[i]][sel], data["speed"]["download"][splitPoints[i-1]:splitPoints[i]][sel])
f7.set_ylabel("Download Speed (mbps)")
f7.minorticks_on()
f7.tick_params(axis='both', direction='in', which='both')
f7.tick_params(top=True, right=True, which='both')
f7.tick_params(labelbottom='off')





f1.set_xlim(xlims[0], xlims[1])
f2.set_xlim(xlims[0], xlims[1])
f3.set_xlim(xlims[0], xlims[1])
f4.set_xlim(xlims[0], xlims[1])
f5.set_xlim(xlims[0], xlims[1])
f6.set_xlim(xlims[0], xlims[1])
f7.set_xlim(xlims[0], xlims[1])
f8.set_xlim(xlims[0], xlims[1])

plt.show()
