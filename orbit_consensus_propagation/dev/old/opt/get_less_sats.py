import generic as g
import os

ALL_SATS_FILE = "active.txt"
USED_SATS_FILE = "sats_to_use.txt"
SAVE_DIR = "data"

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)

try:
    #sats = load_json(save_location_upper+"/sats_used.json")
    f = open(ALL_SATS_FILE, 'r')
    content = f.read()
    f.close()
except:
    raise Exception(ALL_SATS_FILE, "does not exist") 

# Seperate sat list into individual sats
content = content.split("\n")
all_sats = []
for i in range(0,len(content)-(len(content)%3),3):
    all_sats.append({
        "name": g.clean_file_name(content[i]),
        "line1": content[i+1],
        "line2": content[i+2]
    })

# Make sure only sats in icmsd_sats appear in sats
f = open(USED_SATS_FILE, "r")
use_sats = f.read()
use_sats_li = use_sats.split("\n")
use_sats = []
for i in range(len(use_sats_li)):
    use_sats.append(g.clean_file_name(use_sats_li[i]))
sats = []
for i in range(len(all_sats)):
    if all_sats[i]["name"] in use_sats:
        sats.append(all_sats[i])

g.save_json(SAVE_DIR+"/sorted_sats.json", sats)
