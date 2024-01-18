import ctypes
import json
import ephem
from datetime import datetime, timedelta
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
import time
from pytictoc import TicToc

# To acquire this file you can go to
# https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle
input_file = "../../active.txt"


# Create save location if not already exist
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)
save_location_upper = save_location
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)) ,"data", "all_conns")
if not os.path.exists(save_location):
    os.makedirs(save_location)

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)

def clean_file_name(dirty):
    dirty = dirty.replace("_", " ")
    dirty = dirty.replace("-", " ")
    dirty = dirty.replace("(", " ")
    dirty = dirty.replace(")", " ")
    dirty = dirty.replace("/", " ")
    dirty = dirty.replace("*", " ")
    dirty = dirty.strip()
    dirty = dirty.replace("  ", "_")
    dirty = dirty.replace(" ", "_")
    dirty = dirty.replace("_", "")

    return dirty

# Import sats to calculate for
try:
    #sats = load_json(save_location_upper+"/sats_used.json")
    f = open(save_location_upper+"/"+input_file, 'r')
    content = f.read()
    f.close()
except:
    raise Exception(save_location_upper+"/"+input_file, "does not exist") 

# Seperate sat list into individual sats
content = content.split("\n")
all_sats = []
for i in range(0,len(content)-(len(content)%3),3):
    all_sats.append({
        "name": clean_file_name(content[i]),
        "line1": content[i+1],
        "line2": content[i+2]
    })


# Create config file if not exist
try:
    config = load_json(save_location_upper+"/all_conns_config.json")
except:
    config = {
        "timesteps_computed": [

        ]
    }


def round_seconds(obj: datetime) -> datetime:
    if obj.microsecond >= 500_000:
        obj += timedelta(seconds=1)
    return obj.replace(microsecond=0)



# Get only leo satellites from all sats
leo_sats = []
timer = round_seconds(datetime.now())
for sat in all_sats:
    tle_rec = ephem.readtle(sat["name"], sat["line1"], sat["line2"]);
    save_file_name = clean_file_name(sat["name"])
    tle_rec.compute(timer)
    if tle_rec.n >= 11.25 and tle_rec.e < 0.25:
        leo_sats.append(sat)

save_json(save_location_upper+"/leo_sats_parsed.json", leo_sats)