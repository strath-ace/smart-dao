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


### Notice - Calculates positions for day in past and future for input TLE data
### Author - Robert Cowlishaw (0x365)


# Opens go code
library = ctypes.cdll.LoadLibrary("./connected.so")
from_json = library.fromJSON
from_json.argtypes = [ctypes.c_char_p]


# To acquire this file you can go to
# https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle
input_file = "../active.txt"


# Create save location if not already exist
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", "data2")
if not os.path.exists(save_location):
    os.makedirs(save_location)
save_location_upper = save_location
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)),".." ,"data2", "all_conns")
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

def round_seconds(obj: datetime) -> datetime:
    if obj.microsecond >= 500_000:
        obj += timedelta(seconds=1)
    return obj.replace(microsecond=0)


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
sats = []
for i in range(0,len(content)-(len(content)%3),3):
    sats.append({
        "name": content[i],
        "line1": content[i+1],
        "line2": content[i+2]
    })

# Get only leo satellites from all sats
leo_sats = []
timer = round_seconds(datetime.now())
for sat in sats:
    tle_rec = ephem.readtle(sat["name"], sat["line1"], sat["line2"]);
    save_file_name = clean_file_name(sat["name"])
    tle_rec.compute(timer)
    if tle_rec.n >= 11.25 and tle_rec.e < 0.25:
        leo_sats.append(sat)


# Create config file if not exist
try:
    config = load_json(save_location_upper+"/all_conns_config.json")
except:
    config = {
        "timesteps_computed": [

        ]
    }

empty_array = np.zeros([1, len(leo_sats)])
count = 0
for sat in leo_sats:
    if not os.path.isfile(save_location+"/"+clean_file_name(sat["name"])+".csv"):
        np.savetxt(save_location+"/"+clean_file_name(sat["name"])+".csv", empty_array, delimiter=",")
        count += 1
# If no data file reset config and start again
if count == len(leo_sats):
    config = {"timesteps_computed": []}

# Step size in seconds
step_size = 60
# Number of steps to compute
num_steps = 30*1440


start_of_iter = 1702047065  # 8/dec/2023 14:51 ish
end_of_iter = start_of_iter + num_steps*step_size

early_iterations = np.round(np.linspace(start_of_iter, end_of_iter, num_steps))

print("Files created")
print("Starting process...")

t = TicToc()

iterations = []
for i in early_iterations:
    if i not in config["timesteps_computed"]:
        iterations.append(i)
        

for i in iterations:
    t.tic()
    delta_sat_pos = []
    timestep = datetime.fromtimestamp(i)
    for j in range((len(leo_sats))):
        sat = leo_sats[j]
        tle_rec = ephem.readtle(sat["name"], sat["line1"], sat["line2"])
        tle_rec.compute(timestep)

        lon = tle_rec.sublong
        lat = tle_rec.sublat
        elev = tle_rec.sublat

        delta_sat_pos.append([lon, lat, elev])
    document = {
        "delta_sat_pos": delta_sat_pos
    }
    from_json(json.dumps(document).encode('utf-8'))     # Costly function
    # Update all_conn data timestep
    config["timesteps_computed"].append(i)
    save_json(save_location_upper+"/all_conns_config.json", config)
    # Measure time and display timestep
    t.toc()
    print("Timestep", i, "computed")



