# Virgin Home Hub 3.0 Connection Monitorer 

This repository is a python program designed to monitor your Virgin Media connection to help diagnose any connection issues. Note that this is no substitute to phoning Virgin/booking an engineer and getting official help, but is just a tool to help gather information for you (& Virgin) to better diagnose any problems you may be having (note this is completly unofficial, but just something I developed when I was having intermittant issues). The script will monitor the Downstream Power levels, Upstream Power levels, number of Pre-RS and Post-RS errors in the time since the last sampling, Downstream SNR, and also use the speedtest package to test ping, download/upload speeds. Note this has only been tested on the Hub 3.0, and probably won't work on other equipment. The script also does not require any personal details (like passwords), but just uses the information under 'Check router status' on the routers "http://192.168.0.1/" page.

###### How to Use

In this repoistory are two scripts:
- **hub-monitorer.py:** run this python script in a terminal, and it collects the connection information at a pre-set time interval, and updates a python pickle file with the information (just leave running for as long as you want)
- **hub-plotter.py:** this script takes the pickle file created by 'hub-monitorer' and plots it as a nice graph.

To use 'hub-monitorer.py' only really requires you to edit one line, with your favourite text editor go to line 17 and change the "saveDataFile" variable to where-ever you want the pickle file to be saved. By default the program records the connection every 5 minutes, and does a speedtest (using the speedtest package/speedtest.net) every 4 measurements (i.e., every 20 minutes). Both these variables can be adjusted on line 31 and 34, respectively. The program should be run with Python3, you will need the dependencies listed below.

To use 'hub-plotter.py' you just need to edit line 11 to point to your pickle file from the 'hub-monitorer' script. However, you may wish to change lines 18-27 for what you believe is the optimum/acceptable levels, and the expected speed of your connection.

### Example Output
Good Connection                     |  Problematic Connection (before fix)
:----------------------------------:|:----------------------------------:
![](https://github.com/mwls/HomeHubMonitorer/blon/master/good3.png) |  ![](https://github.com/mwls/HomeHubMonitorer/blob/master/problemConnection.png)

### Dependices 
