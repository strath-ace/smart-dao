# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import json
from bs4 import BeautifulSoup

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def save_json(file_name, data):
    """
    Save json data to file
    """
    with open(file_name,'w') as f:
        json.dump(data, f)

json_out = []
json_in = load_json("responses_usgs.json")
#print(json_in["datasets"][1])
json_in = json_in["datasets"][0]["data"]
for i in range(len(json_in)):
    json_out.append(round(json_in[i]["x"]*60))

save_json("clean_usgs.json", json_out)

