# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import matplotlib.pyplot as plt
import matplotlib as matplot
import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import requests
import os
import json
import datetime
import time
import math
import numpy as np

def to_timestamp(date):
    """
    Convert date from input format to timestamp
    """
    try:
        return time.mktime(datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timetuple())
    except:
        return 0

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


json_data = load_json("local-data-path.json")
save_path = json_data["path"]

open_file_name = "/eq_indonesia_social_media.txt"

big_file = load_json(save_path+open_file_name)

rounder = -2
rounder_mul = round(math.pow(10, rounder*-1))

start_time = "2022-11-21 06:21:00"  # Earthquake
end_time = "2022-11-22 12:54:00"    # ICSMD activation

start_timestamp = round(to_timestamp(start_time))
end_timestamp = round(to_timestamp(end_time))

count = 0
time_li = []
for i in range(len(big_file)):
    this_time = big_file[i]["properties"]["created_at"]
    time_li.append(round(to_timestamp(this_time), rounder))

x = list(range(round(start_timestamp, 2), round(end_timestamp, 2), rounder_mul))
y = []
for val in x:
    adder = 0
    for val2 in time_li:
        if val2 < val:
            adder += 1
    y.append(adder)

x = np.array(x) - start_timestamp
x = x/3600
print(x)
fig, ax = plt.subplots(figsize=(10, 10))
ax.plot(x, y)
#plt.yscale("log")
#plt.ylim([0, 100000])

ax.set_title("Tweets of damage over time for Indonesia Earthquake on 21 Nov 2022")
ax.set_xlabel("Time after Earthquake (Hours)")
ax.set_ylabel("Number of tweets")


plt.savefig(save_path+"/fig_eq_indonesia_socail_media.jpg")