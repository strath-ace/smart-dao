# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime 
import json
import math

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

def to_timestamp(date):
    """
    Convert date from input format to timestamp
    """
    try:
        return time.mktime(datetime.strptime(date, "%Y-%m-%d %H:%M:%S").timetuple())
    except:
        try:
            return time.mktime(datetime.strptime(date, "%d%m%Y%H%M").timetuple())
        except:
            try:
                return time.mktime(datetime.strptime(date, "%d%m%Y").timetuple())
            except:
                return 0


num_minutes = 1200      # In minutes
timestep = 15           # In minutes


fig = plt.figure(figsize=(7, 5), dpi=500)

# Earthquake time
earthquake_timestamp = to_timestamp("2022-06-21 20:54:00")

all_stuff = []

# Get twitter words array
x = []
min_val_li = []
words = ["earthquake", "afghanistan", "terremoto", "tsunami"]
twitter_words = load_json("./afghanistan_22-06-21/clean_twitter.json")
for word in words:
    temp = []
    split_x = []
    split_y = []
    for val in twitter_words[word]:
        split_x.append(val[0])
        split_y.append(val[1])
    
    for i in range(0, num_minutes, timestep):
        sum = 0
        for y in range(i, i+timestep):
            if y in split_x:
                for ii in range(len(split_x)):
                    if split_x[ii] == y:
                        sum += split_y[ii]
                        break
        temp.append(sum)
    min_val_li.append(temp)
# Combines tweet words into one output
temp = []
for i in range(len(min_val_li[0])):
    sum = 0
    for ii in range(len(min_val_li)):
        sum += min_val_li[ii][i]
    sum = sum*(math.pow(10,-2))
    for y in range(i, i+timestep):    
        if sum == 0:
            temp.append(0)
        else:
            temp.append(sum)
tweets_sum_li = temp




# Creates x list
for i in range(0, len(tweets_sum_li)):
    x.append(i/60)

def add_dates(x, dates, label_name):
    temp = []
    adjusted_dates = []
    for i in range(len(dates)):
        adjusted_dates.append(round((to_timestamp(dates[i]) - earthquake_timestamp)/60))
    for i in range(0, num_minutes, timestep):
        sum = 0
        for y in range(i, i+timestep):
            if y in adjusted_dates:
                sum += 1
        for y in range(i, i+timestep):
            if sum == 0:
                temp.append(0)
            else:
                temp.append(sum)
    #plt.plot(x, temp, label=label_name)
    #plt.fill_between(x, temp, label=label_name, step="pre", alpha=0.4)
    return temp

def add_minutes(x, minutes_past, label_name):
    temp = []
    for i in range(0, num_minutes, timestep):
        sum = 0
        for y in range(i, i+timestep):
            if y in minutes_past:
                sum += 1
        for y in range(i, i+timestep):
            if sum == 0:
                temp.append(0)
            else:
                temp.append(sum)
    #plt.plot(x, temp, label=label_name)
    #plt.fill_between(x, temp, label=label_name, step="pre", alpha=0.4)
    return temp

usgs_dates = load_json("./afghanistan_22-06-21/clean_usgs.json")

#usgs_dates = ["2022-11-21 06:41:24", "2022-11-21 07:10:56", "2022-11-21 08:21:41", "2022-11-21 15:17:54", "2022-11-22 06:21:39", "2022-12-21 17:34:19", "2023-01-23 07:46:17"]
all_stuff.append(add_minutes(x, usgs_dates, "USGS 'Did you feel it' Notifications"))

# gts_dates = [
#     "2023-02-06 01:26:00",
#     "2023-02-06 01:31:00",
#     "2023-02-06 01:33:00",
#     "2023-02-06 02:40:00",
#     "2023-02-06 02:44:00",
#     "2023-02-06 02:52:00",
#     "2023-02-06 04:18:00",
#     "2023-02-06 06:03:00",
#     "2023-02-06 10:01:00"
# ]
# add_dates(x, gts_dates, "Tsunami Warnings from GTS")

def add_line(date, label_name, colour):
    x = ((to_timestamp(date) - earthquake_timestamp)/3600)
    x_li = [x, x]
    y_li = [0, 20]
    print(x)
    plt.plot(x_li, y_li, label=label_name, linewidth=5, color=colour)

add_line("2022-06-22 14:47:00", "Copernicus Activation", "orange")
add_line("2022-06-22 10:46:00", "ICSMD Activation", "blue")


colours_li = ["darkviolet", "green"]
plt.stackplot(x, tweets_sum_li, all_stuff[0], colors=colours_li, alpha=0.5, labels=["100s of Tweets with Keywords", "USGS 'Did you feel it' Notifications"])    
#plt.stackplot(x, tweets_sum_li, media_sum_li, labels=["100s of Tweets with Keywords", "Media about event"])    
#plt.plot(x, tweets_sum_li, label="100s Tweets with Keywords")
#plt.plot(x, media_sum_li, label="Media about Event")

# plt.fill_between(x, tweets_sum_li, label="100s Tweets with Keywords", step="pre", alpha=0.4)
#plt.fill_between(x, media_sum_li, label="Media about Event", step="pre", alpha=0.4)

#plt.yscale("log")
#plt.legend(loc='upper center')
plt.title("Afghanistan Earthquake 21 Jun 2022")
plt.ylabel("Number of warnings")
plt.xlabel("Time since disaster (Hours)")
plt.savefig("afghanistan_22-11-21")

