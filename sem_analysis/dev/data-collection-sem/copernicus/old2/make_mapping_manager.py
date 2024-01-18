# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import json

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


try:
    sats_classified = load_json("map_manager_country.json")
except:
    sats_classified = {}

all_data = load_json("all_data.json")

events_list = all_data['all_activations']

all_agency = []

all_sats = []
for event in events_list:
    for sat in all_data[event]["ProjectManagement:"]:
        all_sats.append(sat)


# Remove repititions
sats_unclassified = []
for sat in all_sats:
    if sat not in sats_unclassified:
        sats_unclassified.append(sat)

# Remove already classified
sats_to_classify = []
for sat in sats_unclassified:
    try:
        print("Done -", sats_classified[sat])
        all_agency.append(sats_classified[sat]['country'])
    except:
        sats_to_classify.append(sat)

# Classification
print("")
print("Left to classify:", len(sats_to_classify))
for sat in sats_to_classify:
    print("")
    print("--------")
    print("")
    print(sat)
    inp = input("Country or 0 bad or 1 to quit: ")
    if check_int(inp):
        if int(inp) == 0:
            new_classification = {sat: {"real": 0, "country": "na"}}
            sats_classified.update(new_classification)
        if int(inp) == 1:
            break
    else:
        new_classification = {sat: {"real": 1, "country": str(inp)}}
        sats_classified.update(new_classification)
        all_agency.append(str(inp))


save_json("map_manager_country.json", sats_classified)