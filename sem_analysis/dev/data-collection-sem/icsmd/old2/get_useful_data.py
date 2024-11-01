# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import os
import json
import csv

MAX_NUM = 99999999999999999999

bin_map = ['theformeryugoslav', '201619:39utc', 'falklandislands', 'antillesislands', "lebanonandsyria"]
mapping = [
    'iran,islamicrepublic',
    'plurinationalstateofbolivia',
    "micronesia,federatedstatesof",
    "bolivia,plurinationalstateof",
    "russianfederation",
    "republicofsouthkorea",
    "iran,islamicrepublicof",
    "syrianarabrepublic",
    "bolivia,plurinationalstate",
    "venezuela,bolivarianrepublicof",
    "unitedstatesofamerica",
    "unitedstates"
    ]
mapping_to = [
    'iran',
    'bolivia',
    "micronesia",
    "bolivia",
    "russia",
    "southkorea",
    "iran",
    "syria",
    "bolivia",
    "venezuala",
    "us",
    "us"
    ]

with open("hdi.csv", "r") as f:
        read_obj = csv.reader(f)
        HDI_DATA = []
        for row in read_obj:
            try:
                temp = []
                for item in row:
                    temp.append(eval(row))
                HDI_DATA.append(temp)
            except:
                try:
                    HDI_DATA.append(eval(row))
                except:
                    try:
                        HDI_DATA.append(row)
                    except:
                        HDI_DATA = row    
f.close()

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)

def check_int(input):
    """
    Check if input string is a integer
    """
    try:
        int(input)
        is_int = 1
    except:
        is_int = 0
    return is_int


def divide_by_digits(data, chari):
    temp = []
    output = []
    for i in range(len(data)):
        if data[i] in chari:
            output.append("".join(temp).split())
            temp = []
        else:
            temp.append(data[i])
        if i == len(data)-1:
            output.append("".join(temp).split())
    return output

def hdi(country_list):
    added = 0
    for country in country_list:
        country = country.lower()
        country = country.replace(" ", "")
        for data in HDI_DATA:
            if data[0].lower().replace(" ", "") == country:
                #print(data[1])
                added += float(data[1])
    if added == 0 and len(country_list) > 0:
        print(country_list)
    if len(country_list) > 0:
        return added/len(country_list)
    else:
        return 0


local_data_file = os.path.join(os.path.expanduser('~'), "local-data")

old_path = os.path.join(local_data_file, "all-icsmd-data", "all_data.json")
new_path = os.path.join(local_data_file, "all-icsmd-data", "useful_data.json")


map_sat_agency = load_json('map_sat_agency.json')
map_agency_country = load_json('map_agency_country.json')
map_manager_country = load_json('map_manager_country.json')

all_data = load_json(old_path)

events_list = all_data['all_activations']
all_ids = []

output_json = {}

for event_code in events_list:
    event = all_data[event_code]
    id = event["ActivationID:"][0]
    all_ids.append(id)

    # Get minimum satellite data time after activation
    min_date = MAX_NUM
    for dates in event['Acquired:']:
        if dates < min_date and dates > event["DateofCharterActivation:"][0]:
            min_date = dates

    # Convert satellite sources to country
    divider = ['/']
    sources = []
    for source in event['Source:']:
        if "/" in source:
            for x in divide_by_digits(source, divider):
                sources.append(x)
        else:
            sources.append(source)
    source_countries = []
    for source in sources:
        if map_sat_agency[source]['real']:
            if "/" in map_sat_agency[source]['agency']:
                for x in divide_by_digits(map_sat_agency[source]['agency'], divider):
                    if map_agency_country[x[0]]['real']:
                        source_countries.append(map_agency_country[x[0]]['country'])
            else:
                if map_agency_country[map_sat_agency[source]['agency']]['real']:
                    source_countries.append(map_agency_country[map_sat_agency[source]['agency']]['country'])
    temp = []
    for x in source_countries:
        if x not in temp:
            temp.append(x)
    source_countries = temp

    # Convert managers to country
    manager_countries = []
    for manager in event["ProjectManagement:"]:
        if map_manager_country[manager]['real']:
            manager_countries.append(map_manager_country[manager]['country'])
    temp = []
    for x in manager_countries:
        if x not in temp:
            temp.append(x)
    manager_countries = temp

    

    if min_date != MAX_NUM:

        location = ""
        
        for i in range(len(event["LocationofEvent:"][0])-1, 0, -1):
            if event["LocationofEvent:"][0][i] == "/":
                location = event["LocationofEvent:"][0][i+1:].lower()
                break
            if i == 1:
                location = event["LocationofEvent:"][0].lower()
        location = location.replace("&", "and")
        if location in bin_map:
            location = ""
        if location in mapping:
            for i in range(len(mapping)):
                if location == mapping[i]:
                    location = mapping_to[i]
                    break

        country_of_activation = {
            'location': [location], 
            'hdi': hdi([location])
            }
        
        country_of_sat = {
            'location': source_countries, 
            'hdi': hdi(source_countries)
            }
        
        country_of_manager = {
            'location': manager_countries, 
            'hdi': hdi(manager_countries)
            }
    
        event_json = {
            'activation_date': event["DateofCharterActivation:"][0],
            'sat_data_date': min_date,
            'country_of_activation': country_of_activation,
            'country_of_sat': country_of_sat,
            'country_of_manager': country_of_manager
        }


        output_json.update({id: event_json})


output_json.update({'all_activations': all_ids})

save_json(new_path, output_json)
save_json("useful_data.json", output_json)