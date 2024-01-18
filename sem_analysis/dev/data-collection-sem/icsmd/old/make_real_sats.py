# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import csv
import json

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output


def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)
    

try:
    all_sats = load_json("map_sat_to_agency.json")
except:
    all_sats = []

all_data = load_json("output.json")

sats = []
for event in all_data:
    for sat in event["Satellites"]:
        sats.append(sat)

sats_uniq = []
for sat in sats:
    val = True
    for sat_o in sats_uniq:
        if sat == sat_o:
            val = False
            break
    if val:
        sats_uniq.append(sat)

sat_list = []
for sat in all_sats:
    sat_list.append(sat["sat_input"])
for sat in sats_uniq:
    if sat in sat_list:
        continue
    else:
        print("")
        print("--------")
        print(len(sats_uniq)-len(sat_list))
        print("")
        print(sat)
        inp = input("Operator or 0 bad or 1 to quit: ")
        try:
            if int(inp) == 0:
                data = {"sat_input": sat, "real": 0, "country": "na"}
                all_sats.append(data)
            if int(inp) == 1:
                break
        except:
            data = {"sat_input": sat, "real": 1, "country": str(inp)}
            all_sats.append(data)

save_json("map_sat_to_agency.json", all_sats)
