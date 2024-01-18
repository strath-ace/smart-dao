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
timestep = 15      # In minutes



fig = plt.figure(figsize=(7, 5), dpi=500)

# Earthquake time
earthquake_timestamp = to_timestamp("2021-05-21 13:48:00")

all_stuff = []

# Get twitter words array
x = []
min_val_li = []
words = ["earthquake", "china", "terremoto", "tsunami"]
twitter_words = load_json("./china_21-05-21/clean_twitter.json")
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
    #plt.fill_between(x, temp, label=label_name, step="pre", alpha=0.4)
    return temp

usgs_dates = load_json("./china_21-05-21/clean_usgs.json")

#usgs_dates = ["2022-11-21 06:41:24", "2022-11-21 07:10:56", "2022-11-21 08:21:41", "2022-11-21 15:17:54", "2022-11-22 06:21:39", "2022-12-21 17:34:19", "2023-01-23 07:46:17"]
all_stuff.append(add_minutes(x, usgs_dates, "USGS 'Did you feel it' Notifications"))

gts_dates = [
"2021-05-21 16:15:00",
"2021-05-21 17:02:00"
]
all_stuff.append(add_dates(x, gts_dates, "Tsunami Warnings from GTS"))

def add_line(date, label_name, colour):
    x = ((to_timestamp(date) - earthquake_timestamp)/3600)
    x_li = [x, x]
    y_li = [0, 10]
    print(x)
    plt.plot(x_li, y_li, label=label_name, linewidth=5, color=colour)

#add_line("2021-08-14 16:08:00", "Copernicus Activation")
add_line("2021-05-22 08:26:00", "ICSMD Activation", "blue")


colours_li = ["darkviolet", "green", "peru"]
plt.stackplot(x, tweets_sum_li, all_stuff[0], all_stuff[1], colors=colours_li, alpha=0.5, labels=["100s of Tweets with Keywords", "USGS 'Did you feel it' Notifications", "Tsunami Warnings from GTS"])    
#plt.plot(x, tweets_sum_li, label="100s Tweets with Keywords")
#plt.plot(x, media_sum_li, label="Media about Event")

# Normally this one
#plt.fill_between(x, tweets_sum_li, label="100s Tweets with Keywords", step="pre", alpha=0.4)

#plt.fill_between(x, media_sum_li, label="Media about Event", step="pre", alpha=0.4)

#plt.yscale("log")
#plt.legend(loc='upper center')
plt.title("China Earthquake 21 May 2021")
plt.ylabel("Number of warnings")
plt.xlabel("Time since disaster (Hours)")
plt.savefig("china_21-05-21")

