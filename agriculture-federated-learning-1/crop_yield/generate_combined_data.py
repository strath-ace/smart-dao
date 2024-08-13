import numpy as np
import os
import csv
import json

def csv_input(file_name):
    with open(file_name, 'r', encoding=' mac_roman') as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row) 
    f.close()
    return output

def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)

def load_json(file_name):
    with open(file_name, 'r', encoding=' mac_roman') as f:
        output = json.load(f)
    return output

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)

years = np.arange(2000,2023+1,dtype=int)
print(years)

# Load data (and remove header)
data_yield = csv_input(save_location+"/yield_data.csv")[1:]
data_yield = np.array(data_yield)

import pandas as pd
# file_errors_location = 'C:\\Users\\atheelm\\Documents\\python excel mission\\errors1.xlsx'
df = pd.read_excel(save_location+"/dataset.xlsx",na_filter=False)
# df.loc[df == 'N/A'] = np.nan
# df.replace('N/A', pd.NA)
data_yield = df.to_numpy()
data_yield = data_yield[1:]


# Split into locations and yields
data_location = np.array(data_yield[:,0])
data_yield = np.array(data_yield[:,1:])
# print(data_yield)
# Remove all estimates of data
new_data_yield = []
for i, year in enumerate(years):
    bad = data_yield[:,(2*i)+1] != ""
    data_yield[bad,2*i] = ":"
    new_data_yield.append(data_yield[:,2*i])
data_yield = np.array(new_data_yield)

# Convert to floats
data_yield[data_yield == ":"] = np.nan
data_yield = np.array(data_yield, dtype=float)
data_yield = np.swapaxes(data_yield, 0,1)

NUTS_INPUT = ["(NUTS 2003)", "(NUTS 2006)", "(NUTS 2010)", "(NUTS 2013)","(NUTS 2016)", "(NUTS 2021)", "(statistical region 2016)"]
NUTS_MAP = [2003,2006,2010,2013,2016,2021, 2016]
# Detect nuts version
adder = []
new_names = []
for i, loc in enumerate(data_location):
    found = False
    for j, into in enumerate(NUTS_INPUT):
        if into in loc:
            adder.append(NUTS_MAP[j])
            new_names.append(loc.replace(into, ""))
            found = True
    if not found:
        adder.append(0)
        new_names.append(loc)
data_location = np.array(new_names)
nuts_possible = np.array(adder)



# Remove
for i in range(len(data_location)):
    data_location[i] = data_location[i].strip()
bad_regions = ["Extra-Regio NUTS 1",
               "Extra-Regio NUTS 2",
               "European Union (EU6-1958, EU9-1973, EU10-1981, EU12-1986, EU15-1995, EU25-2004, EU27-2007, EU28-2013, EU27-2020)",
               "European Union - 27 countries (from 2020)",
               "European Union - 28 countries (2013-2020)"]
for i in bad_regions:
    data_yield = data_yield[data_location != i]
    nuts_possible = nuts_possible[data_location != i]
    data_location = data_location[data_location != i]




NUTS_YEARS = [2003,2006,2010,2013,2016,2021]

nuts_files = ["NUTS_RG_10M_2003_3035.geojson",
              "NUTS_RG_10M_2006_3035.geojson",
              "NUTS_RG_10M_2010_3035.geojson",
              "NUTS_RG_10M_2013_3035.geojson",
              "NUTS_RG_10M_2016_3035.geojson",
              "NUTS_RG_10M_2021_3035.geojson"]

data_nuts_loc = []
data_geo = []
for nuts in nuts_files:
    nuts_name_li = []
    geo_li = []
    temp_json = load_json(save_location+"/"+nuts)
    temp_json = temp_json["features"]
    for feature in temp_json:
        try:
            nuts_name = feature["properties"]["NAME_LATN"]
        except:
            nuts_name = feature["properties"]["NUTS_NAME"]
        nuts_name_li.append(nuts_name)
        geo = feature["geometry"]["coordinates"]
        geo_li.append(geo)
    data_nuts_loc.append(nuts_name_li)
    data_geo.append(geo_li)



# print(data_geo)

for i in range(len(data_nuts_loc)):
    print(len(data_nuts_loc[i]))

mapped_geo = []
for i, loc in enumerate(data_location):
    found = False
    if nuts_possible[i] != 0:
        for j in range(len(NUTS_YEARS)):
            if nuts_possible[i] == NUTS_YEARS[j]:
                if loc in data_nuts_loc[j]:
                    for k in range(len(data_nuts_loc[j])):
                        if data_nuts_loc[j][k] == loc:
                            mapped_geo.append(data_geo[j][k])
                            found = True
                            break
                break
    if not found:
        found = False
        for j in range(len(NUTS_YEARS)):
            if loc in data_nuts_loc[j]:
                for k in range(len(data_nuts_loc[j])):
                    if data_nuts_loc[j][k] == loc:
                        mapped_geo.append(data_geo[j][k])
                        found = True
                        break
            if found:
                break
        if not found:
            mapped_geo.append("no")
            # print("BAD -", [loc])


print("Location Name", np.shape(data_location))
print("Yield Data", np.shape(data_yield))
print("GEO Data", len(mapped_geo))

final_array = []
for i in range(len(data_location)):
    if mapped_geo[i] != "no":
        # print(data_yield[i,:])
        temp = [data_location[i]]
        for x in data_yield[i,:]:
            temp.append(x)
            # print(x)
        temp.append(mapped_geo[i])
        final_array.append(temp)

df = pd.DataFrame(final_array, columns=["Location Name", *(np.array(years,dtype=str).tolist()), "Geo"])
df.to_excel(save_location+"/clean_data.xlsx")



# Convert for display
from geojson import Polygon
import random

outgeo = []
for i in range(len(mapped_geo)):
    if mapped_geo[i] != "no":
        outgeo.append({
                "type": "Feature",
                "geometry":Polygon(mapped_geo[i]),
                "properties": {
                    "prop0": int(np.sum(np.logical_not(np.isnan(data_yield[i]))))
                }
            })


extra_stuff = {
    "type": "FeatureCollection",
    "features": outgeo,
    "crs":{
        "type":"name",
        "properties":{"name":"urn:ogc:def:crs:EPSG::3035"}
    }
}

save_json(save_location+"/geo_out.geojson", extra_stuff)