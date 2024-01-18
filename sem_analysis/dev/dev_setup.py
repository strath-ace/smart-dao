# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import os
import json

def save_json(file_name, data):
    """
    Save json data to file
    """
    with open(file_name,'w') as f:
        json.dump(data, f)


# Builds local-data-storage


config_f = open("./config.json")
config = json.load(config_f)

home_path = os.path.expanduser('~')
local_data_folder = config["local_data_dir"]
local_app_folder = config["local_app_dir"]

try:
    os.mkdir(os.path.join(home_path, local_data_folder))
except:
    pass

try:
    os.mkdir(os.path.join(home_path, local_data_folder, local_app_folder))
except:
    pass


counter = 0
for root, dirs, files in (os.walk(os.path.dirname(os.path.abspath(__file__)))):
    if counter == 0:
        folders = dirs
        root_store = root
    counter += 1


for fold in folders:
    if fold not in [".git"]:
        try:
            c_path = os.path.join(home_path, local_data_folder, local_app_folder, fold)
            os.mkdir(c_path)
        except:
            pass
        try:
            json_data = {"path": c_path}
            print(root_store+"/"+fold)
            save_json(root_store+"/"+fold+"/local-data-path.json", json_data)
        except:
            pass



