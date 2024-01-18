# Orbital Consensus Propagation Research

## About
-  Look at the topography of the network at any given time and compare this to how a p2p consensus mechanism works
- Measure centralisation in such a space network (if communications go through larger communication relay satellites
- By modelling orbits and their satellites how long does a new message from different satellites take to have consensus found on it
-  Paper about connection times and what the satellite network actually looks like with intermittent connection

Things to vary and measure
- Change range of communication
- Speed of communication (data transfer speeds)
- change which constellations are considered
- how often everyone connects
- how this would allow consensus 
- create a fake satellite orbit first like 2body problem then test of real satellite positions

## How to use

1. Get `active.txt` from [Celestrak](https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle) by right clicking on page and save page as. Save this file in root directory of the repository.
2. Enter into one of the directories, data_cluster, data_icsmd, data_oneweb, data_leo.
3. To build the dataset run (this may take some time depending on the number of satellites in constellation):
```
python3 builder/app.py
```
4. To graph the data generated run:
```
python3 display/graph.py
```
