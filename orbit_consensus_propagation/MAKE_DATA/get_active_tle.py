# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import os
from datetime import datetime
from commons import *
import os
import ssl
import requests


ALL_DIRS = [["data_all", ""], 
            ["data_icsmd_1day", "icsmd_sats.txt"]]
            # ["data_icsmd_1day_v0", "icsmd_sats.txt"],
            # ["data_icsmd_1day_v1", "icsmd_sats.txt"],
            # ["data_icsmd_1day_v2", "icsmd_sats.txt"],
            # ["data_icsmd_1day_v3", "icsmd_sats.txt"],
            # ["data_icsmd_1day_v4", "icsmd_sats.txt"],
            # ["data_icsmd_1day_v5", "icsmd_sats.txt"],
            # ["data_icsmd_1day_v6", "icsmd_sats.txt"],
            # ["data_icsmd_1day_v7", "icsmd_sats.txt"],
            # ["data_icsmd_1day_v8", "icsmd_sats.txt"],
            # ["data_icsmd_1day_v9", "icsmd_sats.txt"],
            # ["data_icsmd_1day_1sec", "icsmd_sats.txt"], 
            # ["data_icsmd_10day", "icsmd_sats.txt"],
            # ["data_orbital", "icsmd_sats.txt"],  
            # ["data_icsmd_100day", "icsmd_sats.txt"]]




def reduce_sats(USED_SATS_FILE, SAVE_DIR):
    this_location = os.path.dirname(os.path.abspath(__file__))

    save_location = os.path.join(this_location, "..", "DATA",SAVE_DIR)
    if not os.path.exists(save_location):
        os.makedirs(save_location)    

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        # Legacy Python that doesn't verify HTTPS certificates by default
        pass
    else:
        # Handle target environment that doesn't support HTTPS verification
        ssl._create_default_https_context = _create_unverified_https_context
        
    link = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"

    response = requests.get(link)

    # Seperate sat list into individual sats
    rep = response.text.replace("\r", "")
    content = rep.split("\n")
    all_sats = []
    for i in range(0,len(content)-(len(content)%3),3):
        all_sats.append({
            "name": clean_file_name(content[i]),
            "line1": content[i+1],
            "line2": content[i+2]
        })

    # Make sure only sats in icmsd_sats appear in sats
    try:
        f = open(this_location+"/../"+USED_SATS_FILE, "r")
        use_sats = f.read()
        use_sats_li = use_sats.split("\n")
        use_sats = []
        for i in range(len(use_sats_li)):
            use_sats.append(clean_file_name(use_sats_li[i]))
        sats = []
        for i in range(len(all_sats)):
            if all_sats[i]["name"] in use_sats:
                sats.append(all_sats[i])

        save_json(save_location+"/sorted_sats.json", sats)
    except:
        save_json(save_location+"/sorted_sats.json", all_sats)
    
    return round(datetime.now().timestamp())


save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..","DATA")
if not os.path.exists(save_location):
    os.makedirs(save_location)

for i in range(len(ALL_DIRS)):
    SAVE_DIR = ALL_DIRS[i][0]
    USED_SATS_FILE = ALL_DIRS[i][1]
    save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
    if not os.path.exists(save_location):
        os.makedirs(save_location)
        START_TIME = reduce_sats(USED_SATS_FILE, SAVE_DIR)
        save_json(save_location+"/dataset.json", {"timestamp": START_TIME})
    else:
        print(SAVE_DIR, "already exists")