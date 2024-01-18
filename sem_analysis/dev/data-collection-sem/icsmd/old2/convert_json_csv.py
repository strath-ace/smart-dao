# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import os
import json
import csv

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def csv_output(file_name, data_send):
    '''
    Open a csv and add the sent data
    '''
    with open(file_name, "w") as f:
        for item in data_send:
            csv.writer(f).writerow(item)
    f.close()

all_data = load_json("useful_data.json")

all_events = all_data['all_activations']
all_events = [eval(i) for i in all_events]
all_events = sorted(all_events)
all_events = [str(i) for i in all_events]

data_out = []

data_out.append([
        'event_id',
        'event_date',
        'activation_date',
        'sat_data_date',
        'publish_data',
        'country_of_activation_location',
        'country_of_activation_hdi',
        'country_of_sat_location',
        'country_of_sat_hdi',
        'country_of_manager_location',
        'country_of_manager_hdi'
    ])

for event in all_events:
    try:
        data = all_data[event]
        data_out.append([
            event,
            'na',
            data['activation_date'],
            data['sat_data_date'],
            'na',
            data['country_of_activation']['location'],
            data['country_of_activation']['hdi'],
            data['country_of_sat']['location'],
            data['country_of_sat']['hdi'],
            data['country_of_manager']['location'],
            data['country_of_manager']['hdi']
        ])
    except:
        continue

csv_output("icsmd_data.csv", data_out)