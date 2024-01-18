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

os.system('go build -buildmode=c-shared -o connected.so connected.go')

# Opens go code
library = ctypes.cdll.LoadLibrary("./connected.so")
from_json = library.fromJSON
from_json.argtypes = [ctypes.c_char_p]


# To acquire this file you can go to
# https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle
input_file = "../../active.txt"


# Create save location if not already exist
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)
save_location_upper = save_location
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)),".." ,"data", "all_conns")
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
all_sats = []
for i in range(0,len(content)-(len(content)%3),3):
    all_sats.append({
        "name": clean_file_name(content[i]),
        "line1": content[i+1],
        "line2": content[i+2]
    })

# Make sure only sats in icmsd_sats appear in sats
f = open(save_location_upper+"/../icsmd_sats.txt", "r")
use_sats = f.read()
use_sats_li = use_sats.split("\n")
use_sats = []
for i in range(len(use_sats_li)):
    use_sats.append(clean_file_name(use_sats_li[i]))
sats = []
for i in range(len(all_sats)):
    if all_sats[i]["name"] in use_sats:
        sats.append(all_sats[i])



# Create config file if not exist
try:
    config = load_json(save_location_upper+"/all_conns_config.json")
except:
    config = {
        "timesteps_computed": [

        ]
    }

empty_array = np.zeros([1, len(sats)])
count = 0
for sat in sats:
    if not os.path.isfile(save_location+"/"+clean_file_name(sat["name"])+".csv"):
        np.savetxt(save_location+"/"+clean_file_name(sat["name"])+".csv", empty_array, delimiter=",")
        count += 1
# If no data file reset config and start again
if count == len(sats):
    config = {"timesteps_computed": []}

# Step size in seconds
step_size = 60
# Number of steps to compute
num_steps = 20*1440


start_of_iter = 1701448313  # 8/dec/2023 14:51 ish
end_of_iter = start_of_iter + num_steps*step_size

early_iterations = np.round(np.linspace(start_of_iter, end_of_iter, num_steps))

print("Files created")
print("Starting process...")

t = TicToc()

iterations = []
for i in early_iterations:
    if i not in config["timesteps_computed"]:
        iterations.append(i)
        
t.tic()
for i in iterations:
    delta_sat_pos = []
    timestep = datetime.fromtimestamp(i)
    for j in range((len(sats))):
        sat = sats[j]
        tle_rec = ephem.readtle(sat["name"], sat["line1"], sat["line2"])
        tle_rec.compute(timestep)

        lon = tle_rec.sublong
        lat = tle_rec.sublat
        elev = tle_rec.elevation

        delta_sat_pos.append([lon, lat, elev])
    document = {
        "delta_sat_pos": delta_sat_pos
    }
    from_json(json.dumps(document).encode('utf-8'))     # Costly function
    # Update all_conn data timestep
    config["timesteps_computed"].append(i)
    save_json(save_location_upper+"/all_conns_config.json", config)
    # Measure time and display timestep
    if i % 10000 == 0:
        t.toc()
        print("Timestep up to", i, "computed")
        t.tic()


t.toc()
print("Done")