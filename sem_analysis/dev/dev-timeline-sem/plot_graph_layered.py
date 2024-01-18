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


num_minutes = 2000

# Earthquake time
earthquake_timestamp = to_timestamp("2022-11-21 06:21:00")


# Get twitter words array
x = []
min_val_li = []
words = ["earthquake", "indonesia", "terremoto", "tsunami"]
twitter_words = load_json("clean_twitter.json")
for word in words:
    temp = []
    split_x = []
    split_y = []
    for val in twitter_words[word]:
        split_x.append(val[0])
        split_y.append(val[1])

    sum = 0
    for i in range(0, num_minutes):
        if i in split_x:
            for ii in range(len(split_x)):
                if split_x[ii] == i:
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
    temp.append(sum*math.pow(10, -2))
tweets_sum_li = temp


# Get media times
media = load_json("clean_media.json")
time_diff = []
for i in range(len(media)):
    time_diff.append(round((to_timestamp(media[i]["time"]) - earthquake_timestamp)/60))
temp = []
print(time_diff)
sum = 0
for i in range(0, num_minutes):
        if i in time_diff:
            sum += 1
        temp.append(sum)
media_sum_li = temp



    


# Creates x list
for i in range(0, num_minutes):
    x.append(i/60)


plt.stackplot(x, tweets_sum_li, media_sum_li, labels=["100s of Tweets with Keywords", "Media about event"])    
#plt.legend(loc='upper left')
plt.ylabel("Number of warnings")
plt.xlabel("Time since disaster (Hours)")
plt.show()

