# Virgin Home Hub 3.0 Connection Monitorer 

This repository is a python program designed to monitor your Virgin Media connection to help diagnose any connection issues. Note that this is no substitute to phoning Virgin/booking an engineer and getting official help, but is just a tool to help gather information for you (& Virgin) to better diagnose any problems you may be having (note this is completly unofficial, but just something I developed when I was having intermittant issues). The script will monitor the Downstream Power levels, Upstream Power levels, number of Pre-RS and Post-RS errors in the time since the last sampling, Downstream SNR, and also use the speedtest package to test ping, download/upload speeds. Note this has only been tested on the Hub 3.0, and probably won't work on other equipment. The script also does not require any personal details (like passwords), but just uses the information under 'Check router status' on the routers "http://192.168.0.1/" page.

###### How to Use

In this repoistory are two scripts:
- **hub-monitorer.py:** run this python script in a terminal, and it collects the connection information at a pre-set time interval, and updates a python pickle file with the information (just leave running for as long as you want)
- **hub-plotter.py:** this script takes the pickle file created by 'hub-monitorer' and plots it as a nice graph.
