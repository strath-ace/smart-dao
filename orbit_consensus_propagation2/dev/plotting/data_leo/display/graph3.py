import matplotlib.pyplot as plt
import numpy as np
import ctypes
import json
import os
import csv
from math import ceil
from matplotlib.ticker import MaxNLocator
import math
import ephem

# Opens go code
import ctypes
library = ctypes.cdll.LoadLibrary('./combine.so')
combine = library.combine
combine()

print("Grasphing Data")

input_file = "graph_data.csv"

# Create save location if not already exist
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", "data")
if not os.path.exists(save_location):
    os.makedirs(save_location)
# Create save location if not already exist
upper_location = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..", "..", "data")
if not os.path.exists(upper_location):
    os.makedirs(upper_location)
def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output
config = load_json(save_location+"/all_conns_config.json")
def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            try:
                temp = []
                for item in row:
                    temp.append(eval(row))
                output.append(temp)
            except:
                try:
                    output.append(eval(row))
                except:
                    try:
                        output.append(row)
                    except:
                        output = row    
    f.close()
    return output
li_all = csv_input(save_location+"/"+input_file)
li_all = np.rot90(np.array(li_all))
# Sort by li_nums[:,0] first then by li_num[:,1] (aka sort by unique then total)
ind = np.lexsort((li_all[:,1], li_all[:,2]), axis=0)
li_nums = np.asanyarray(li_all[:,1:], dtype=float)
li_sat_names = [li_all[:,0][i] for i in ind]
li_count = li_nums[:,0]
li_unique = li_nums[:,1]


all_tle_data = load_json(save_location+"/leo_sats_parsed.json")

def sat_name_to_kepler(sat_name):
    for i in range(len(all_tle_data)):
        if all_tle_data[i]["name"] == sat_name:
            return all_tle_data[i]
    return "ERROR"

max_params = []


data_types = ["Inclination", "RAAN", "Eccentricity", "Arg of Peri", "Mean Motion"]
data_tamper = [180, 360, 0.0025, 360, 25]

data = []

groups = [[0, 1500], [1500, 3000], [3000, 4000], [4000, 5000], [5000, 7500], [7500, 8250]]

for group in groups:
    temp = []
    for i in range(len(li_sat_names[group[0]:group[1]])):
        current_sat = sat_name_to_kepler(li_sat_names[i])
        tle_rec = ephem.readtle(current_sat["name"], current_sat["line1"], current_sat["line2"]);
        tle_rec.compute()
        temp.append([tle_rec.inc, tle_rec.raan, tle_rec.e, tle_rec.ap, tle_rec.n])
    data.append(temp)

data2 = []
for group in data:
    current = np.array(group)
    current_avg = np.average(current, axis=0)
    data2.append(current_avg)

slots = 5
data2_scaled = np.array(data2)
for i in range(slots):
    data2_scaled[:,i] = np.power(data2_scaled[:,i]/np.average(data2_scaled[:,i]), 1)


#data = [cluster_number[satellite_number[kepler_element]]
plt.xlim([-1.5, 1.5])
plt.ylim([-1.5, 1.5])
c = 0
for slot_in in data2_scaled:
    x = []
    y = []
    for i in range(slots):
        try:
            x.append(slot_in[i]*math.sin(i*2*np.pi/slots))
            y.append(slot_in[i]*math.cos(i*2*np.pi/slots))
        except:
            x.append(0)
            y.append(0)
    try:
        x.append(0)
        y.append(slot_in[0])
    except:
        x.append(0)
        y.append(0)
    plt.plot(x,y, label="Group "+str(c))
    c += 1

for i in range(slots):
    plt.annotate(data_types[i], [1.1*np.amax(data2_scaled[:,i])*math.sin(i*2*np.pi/slots), 1.1*np.amax(data2_scaled[:,i])*math.cos(i*2*np.pi/slots)], ha="center")


plt.legend()
plt.axis('equal')
plt.savefig("distribution_avg.png")
# plt.show()



plt.clf()






fig, axs = plt.subplots(2,3)
axs_li = [axs[0, 0], axs[0, 1], axs[0, 2], axs[1, 0], axs[1, 1], axs[1, 2]]
for ii, curr in enumerate(axs_li):
    all_slots_in = data[ii]
    slots = 5
    curr.scatter(0,0, c="black")
    for slot_in in all_slots_in:
        x = []
        y = []
        for i in range(slots):
            try:
                if slot_in[i]*math.sin(i*2*np.pi/slots)/np.average(np.array(all_slots_in)[:,i]) <= 2 * np.average(np.array(all_slots_in)[:,i]) and slot_in[i]*math.cos(i*2*np.pi/slots)/np.average(np.array(all_slots_in)[:,i]) <= 2 * np.average(np.array(all_slots_in)[:,i]):
                    x.append(slot_in[i]*math.sin(i*2*np.pi/slots)/np.average(np.array(all_slots_in)[:,i]))
                    y.append(slot_in[i]*math.cos(i*2*np.pi/slots)/np.average(np.array(all_slots_in)[:,i]))
            except:
                x.append(0)
                y.append(0)
        try:
            i = 0
            if slot_in[i]*math.sin(i*2*np.pi/slots)/np.average(np.array(all_slots_in)[:,i]) <= 2 * np.average(np.array(all_slots_in)[:,i]) and slot_in[i]*math.cos(i*2*np.pi/slots)/np.average(np.array(all_slots_in)[:,i]) <= 2 * np.average(np.array(all_slots_in)[:,i]):
                x.append(0)
                y.append(slot_in[0]/np.average(np.array(all_slots_in)[:,0]))
        except:
            x.append(0)
            y.append(0)
        curr.plot(x,y, alpha=(5/len(all_slots_in)))
    # Plot axis
    # curr.plot([-1, 1], [0, 0], c="black")
    curr.axis('equal')

plt.savefig("distribution_all.png")
# plt.show()
