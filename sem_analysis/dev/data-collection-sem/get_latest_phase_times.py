# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import os
import json
import json
import time
import datetime

import matplotlib.pyplot as plt
import numpy as np

from plot_func import *


SEC_IN_HOUR = 60*60
MAX_PLOT = SEC_IN_HOUR * 500

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def date_to_timestamp(date, date_format):
    return time.mktime(datetime.datetime.strptime(date, date_format).timetuple())

def timestamp_to_date(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)


all_data = load_json("copernicus/useful_data.json")

all_events = get_all_events(all_data)

x= []
date_a_li = []
phase_a_li = []
phase_b_li = []
phase_c_li = []
count = 0
for event in all_events:
    try:
        data = all_data[event]
        good = 1
        try:
            date_a = data["event_date"]
        except:
            good = 0
        try:
            date_b = data['activation_date']
        except:
            good = 0
        try:
            date_c = data['sat_data_date']
        except:
            good = 0
        try:
            date_d = data['publish_date']
        except:
            good = 0
        if good:
            
            below = 1#date_b-date_a < MAX_PLOT and date_c-date_b < MAX_PLOT and date_d-date_c < MAX_PLOT
            above = date_b-date_a > 0 and date_c-date_b > 0 and date_d-date_c > 0
            if below and above:
                count += 1
                x.append(int(event))
                date_a_li.append(date_a)
                phase_a_li.append((date_b - date_a) / SEC_IN_HOUR)
                phase_b_li.append((date_c - date_b) / SEC_IN_HOUR)
                phase_c_li.append((date_d - date_c) / SEC_IN_HOUR)
    except:
        continue


# Previous Year
current_date = date_to_timestamp("27032023", "%d%m%Y")
year_ago = date_to_timestamp("27032022", "%d%m%Y")

# # First Data Year
# date_a_1 = date_a_li[0]
# for i in range(1, len(date_a_li)):
#     if date_a_1 > date_a_li[i]:
#         date_a_1 = date_a_li[i]
# copy_date_a_li = date_a_li
# for i in range(50):
#     min_temp = copy_date_a_li[0]
#     min_point = 0
#     for ii in range(1, len(copy_date_a_li)):
#         if min_temp > copy_date_a_li[ii]:
#             min_temp = copy_date_a_li[ii]
#             min_point = ii
#     copy_date_a_li[min_point] = 9999999999
# date_b_1 = copy_date_a_li[0]
# for i in range(1, len(copy_date_a_li)):
#     if date_b_1 > copy_date_a_li[i]:
#         date_b_1 = copy_date_a_li[i]

# print(timestamp_to_date(date_a_1))
# print(timestamp_to_date(date_b_1))


# # Latest Data Year
# date_b_2 = date_a_li[0]
# for i in range(1, len(date_a_li)):
#     if date_b_2 < date_a_li[i]:
#         date_b_2 = date_a_li[i]
# date_a_2 = date_b_2 - 31536000  # Equivalent to one year

date_a_1 = date_a_li[0]
date_b_1 = date_a_li[30]
date_a_2 = date_a_li[-32]
date_b_2 = date_a_li[-1]

a_1 = 0
b_1 = 0
c_1 = 0
counter_1 = 0

a_2 = 0
b_2 = 0
c_2 = 0
counter_2 = 0

print(len(date_a_li))
for i in range(len(date_a_li)):
    if date_a_1 < date_a_li[i] and date_a_li[i] < date_b_1:
        a_1 += phase_a_li[i]
        b_1 += phase_b_li[i]
        c_1 += phase_c_li[i]
        counter_1 += 1

for i in range(len(date_a_li)):
    if date_a_2 < date_a_li[i] and date_a_li[i] < date_b_2:
        a_2 += phase_a_li[i]
        b_2 += phase_b_li[i]
        c_2 += phase_c_li[i]
        counter_2 += 1

avg_a_1 = a_1/counter_1
avg_b_1 = b_1/counter_1
avg_c_1 = c_1/counter_1
avg_tot_1 = avg_a_1+avg_b_1+avg_c_1

avg_a_2 = a_2/counter_2
avg_b_2 = b_2/counter_2
avg_c_2 = c_2/counter_2
avg_tot_2 = avg_a_2+avg_b_2+avg_c_2

print("First Year of Data", timestamp_to_date(date_a_1), "to", timestamp_to_date(date_b_1))
print("Datapoints in this date window", counter_1)
print("Average Phase A:", avg_a_1)
print("Average Phase B:", avg_b_1)
print("Average Phase C:", avg_c_1)
print("Average Total:", avg_tot_1)

print()

print("Last Year of Data", timestamp_to_date(date_a_2), "to", timestamp_to_date(date_b_2))
print("Datapoints in this date window", counter_2)
print("Average Phase A:", avg_a_2)
print("Average Phase B:", avg_b_2)
print("Average Phase C:", avg_c_2)
print("Average Total:", avg_tot_2)
