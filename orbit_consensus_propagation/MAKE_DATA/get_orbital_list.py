from commons import *
import os
import ephem
import numpy as np


SAVE_DIR = "data_icsmd_1day"

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "DATA", SAVE_DIR)
if not os.path.exists(save_location):
    raise Exception("Sat Data not setup, run get_active_tle.py first")

data_all_sats = load_json(save_location+"/sorted_sats.json")

all_sats = []
for sat_data in data_all_sats:
    all_sats.append(ephem.readtle(sat_data["name"], sat_data["line1"], sat_data["line2"]))

all_data = [["name", "mean motion", "inclination", "raan", "eccentricity", "argp", "mean anomaly"]]
for i in all_sats:
    all_data.append([i.name, i.n, i.inc, i.raan, i.e, i.ap, i.M])

np.save(save_location+"/sat_data", all_data)

