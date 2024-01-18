from urllib.request import urlopen
import json
import csv

data = []
disaster_types = ["WF", "VO", "FL", "EQ", "TC", "DR"]


for disaster_type in disaster_types:
    for year in range(2000,2023):
        counter = 0
        fails = 0
        for month in range(1,13):
            if month < 12:
                dates = "fromDate="+str(year)+"-"+f"{month:02d}"+"-"+"01"+"&"+"toDate="+str(year)+"-"+f"{month+1:02d}"+"-"+"01"
            if month == 12:
                dates = "fromDate="+str(year)+"-"+f"{month:02d}"+"-"+"01"+"&"+"toDate="+str(year+1)+"-"+"01"+"-"+"01"

            url = "https://www.gdacs.org/gdacsapi/api/events/geteventlist/SEARCH?"+dates+"&eventlist="+disaster_type+"&country="

            
            try:
                response = urlopen(url)

                data_json = json.loads(response.read())
                

                for i in range(len(data_json['features'])):
                    try:
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
                        counter += 1
                    except:
                        fails += 1
                        print(data_single)
                        continue
                    
            except:
                
                continue

        print("Done --- Disaster Type:", disaster_type, "- Year:", year, "- Total count:", counter, "with",fails,"missed")


filename = 'C:/Algorand/data/all_disasters.csv'
with open(filename, 'w', newline="") as file:
    csvwriter = csv.writer(file)
    csvwriter.writerows(data)