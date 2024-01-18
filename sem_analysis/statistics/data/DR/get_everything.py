from urllib.request import urlopen
import json
import csv

data = []
disaster_types = ["WF", "VO", "FL", "EQ", "TC", "DR"]

path = 'C:/Algorand/data/DR/'
output_file = 'combined.csv'


from os import listdir
from os.path import isfile, join
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]

print(onlyfiles)

for i in range(len(onlyfiles)):
    if onlyfiles[i] == 'get_everything.py' or onlyfiles[i] == output_file:
        continue
    else:
        response = open(path+onlyfiles[i])
        data_json = json.loads(response.read())


        for i in range(len(data_json['features'])):
            data_single = data_json['features'][i]
            data.append([data_single['properties']['eventid'],
                            data_single['properties']['name'],
                            data_single['properties']['eventtype'],
                            data_single['geometry']['coordinates'][0],
                            data_single['geometry']['coordinates'][1],
                            data_single['properties']['fromdate'],
                            data_single['properties']['todate'],
                            data_single['properties']['alertlevel'],
                            data_single['properties']['alertscore'],
                            data_single['properties']['episodealertscore'],
                            data_single['properties']['country'],
            ])

filename = path+output_file
with open(filename, 'w', newline="") as file:
    csvwriter = csv.writer(file)
    csvwriter.writerows(data)