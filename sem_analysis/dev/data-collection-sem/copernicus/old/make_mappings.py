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
    sats_classified = load_json("map_sat_agency.json")
except:
    sats_classified = {}
try:
    agency_classified = load_json("map_agency_country.json")
except:
    agency_classified = {}

all_data = load_json("output.json")

all_agency = []

all_sats = []
for event in all_data:
    for sats in event["pre_event"]:
        all_sats.append(sats)
    for sats in event["post_event"]:
        all_sats.append(sats)




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
        all_agency.append(sats_classified[sat]['agency'])
    except:
        sats_to_classify.append(sat)

# Classification
print("Left to classify:", len(sats_to_classify))
for sat in sats_to_classify:
    print("")
    print("--------")
    print("")
    print(sat)
    inp = input("Operator or 0 bad or 1 to quit: ")
    if check_int(inp):
        if int(inp) == 0:
            new_classification = {sat: {"real": 0, "agency": "na"}}
            sats_classified.update(new_classification)
        if int(inp) == 1:
            break
    else:
        new_classification = {sat: {"real": 1, "agency": str(inp)}}
        sats_classified.update(new_classification)
        all_agency.append(str(inp))





print("")
print("--------")
print("AGENCIES")
print("")





# Remove repititions
agency_unclassified = []
for agency in all_agency:
    if agency not in agency_unclassified:
        agency_unclassified.append(agency)

# Remove already classified
agency_to_classify = []
for agency in agency_unclassified:
    try:
        print("Done -", agency_classified[agency])
    except:
        agency_to_classify.append(agency)

# Classification
print("Left to classify:", len(agency_to_classify))
for agency in agency_to_classify:
    print("")
    print("--------")
    print("")
    print(agency)
    inp = input("Country or 0 bad or 1 to quit: ")
    if check_int(inp):
        if int(inp) == 0:
            new_classification = {agency: {"real": 0, "country": "na"}}
            agency_classified.update(new_classification)
        if int(inp) == 1:
            break
    else:
        new_classification = {agency: {"real": 1, "country": str(inp)}}
        agency_classified.update(new_classification)



save_json("map_sat_agency.json", sats_classified)
save_json("map_agency_country.json", agency_classified)