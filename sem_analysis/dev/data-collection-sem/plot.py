import os
import json
import csv

import matplotlib.pyplot as plt
import numpy as np

from plot_func import *


def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

json_data = load_json("local-data-path.json")
save_path = json_data["path"]+"/figs"
save_path_c = save_path+"/countries"
save_path_h = save_path+"/hdi"

try:
    os.mkdir(save_path)
except:
    pass
try:
    os.mkdir(save_path_c)
except:
    pass
try:
    os.mkdir(save_path_h)
except:
    pass

SEC_IN_HOUR = 60*60
MAX_PLOT = SEC_IN_HOUR * 500

all_data_copernicus = load_json("copernicus/useful_data.json")
all_data_icsmd = load_json("icsmd/useful_data.json")
clean_data_copernicus = load_json("copernicus/clean_data.json")




# plot_country_in(all_data_copernicus, "copernicus", "activation", save_path_c)
# plot_country_in(all_data_icsmd, "icsmd", "activation", save_path_c)

# plot_country_in(all_data_copernicus, "copernicus", "sat", save_path_c)
# plot_country_in(all_data_icsmd, "icsmd", "sat", save_path_c)

# plot_country_in(all_data_copernicus, "copernicus", "manager", save_path_c)
# plot_country_in(all_data_icsmd, "icsmd", "manager", save_path_c)

# plot_country_in_hdi(all_data_copernicus, "copernicus", "activation", save_path_h)
# plot_country_in_hdi(all_data_icsmd, "icsmd", "activation", save_path_h)

# plot_country_in_hdi(all_data_copernicus, "copernicus", "sat", save_path_h)
# plot_country_in_hdi(all_data_icsmd, "icsmd", "sat", save_path_h)

# plot_country_in_hdi(all_data_copernicus, "copernicus", "manager", save_path_h)
# plot_country_in_hdi(all_data_icsmd, "icsmd", "manager", save_path_h)

# plot_times_copernicus(all_data_copernicus, "copernicus", save_path)


#big_boy(all_data_copernicus, "copernicus", clean_data_copernicus, save_path)


plot_hdi_comparison(all_data_icsmd, save_path)


# s




