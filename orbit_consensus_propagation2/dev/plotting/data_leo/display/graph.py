import ctypes
import json
import os
import csv
import matplotlib.pyplot as plt
import numpy as np
from math import ceil
from matplotlib.ticker import MaxNLocator




### Notice - Calculates positions for day in past and future for input TLE data
### Author - Robert Cowlishaw (0x365)

os.system('go build -buildmode=c-shared -o combine.so combine.go')

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    import numpy as np
    from math import factorial
    
    try:
        window_size = np.abs((window_size))
        order = np.abs((order))
    except ValueError:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')





# Opens go code
import ctypes
library = ctypes.cdll.LoadLibrary('./combine.so')
combine = library.combine
combine()

print("Graphing Data")

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


fig,ax = plt.subplots(figsize=[10, 10], dpi=100)

total_timer = round( ( np.amax(config["timesteps_computed"]) - np.min(config["timesteps_computed"]) ) / 3600 ,2)
# total_timer = 10

y_array_1 = [li_count[i] for i in ind]
# Change 101 to make smoother
y_array_1_out = savitzky_golay(y_array_1, 501, 3)
# y_array_1_out = y_array_1

ax.plot(y_array_1_out, c="green", label="Total number of connected timesteps")
ax.set_xlabel("Satellite number")
ax.set_ylabel("Counted connections of time period", c="green")
ax.set_ylim([0, 1.1*np.amax(y_array_1_out)])


ax2=ax.twinx()
ax2.plot([li_unique[i] for i in ind], c="blue")
ax2.set_ylabel("Num of unique combinations", c="blue")
ax2.set_ylim([0, len(li_sat_names)])
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

title_string = "Absolute number of connections (Computed over "+str(total_timer)+" hours with "+str(len(li_sat_names))+" LEO satellites)"
plt.title(title_string)
plt.savefig(save_location+"/num_of_connections_absolute.png")

# plt.show()

plt.clf()


fig,ax = plt.subplots(figsize=[10, 10], dpi=100)

y_array_2 = [100*li_count[i]/(len(config["timesteps_computed"])*li_unique[i]) for i in ind]
# y_array_2 = [100*li_count[i]/(100*li_unique[i]) for i in ind]

# Change 101 to make smoother
y_array_2_out = savitzky_golay(y_array_2, 501, 3)
# y_array_2_out = y_array_2

ax.plot(y_array_2_out, label="Total timesteps connected in time period", c="green")
ax.set_xlabel("Satellite number")
ax.set_ylabel("Percentage of total time connected the unique satellites (%)", c="green")
ax.set_ylim([0.9*np.amin(y_array_2_out), 1.1*np.amax(y_array_2_out)])


ax2=ax.twinx()
ax2.plot([li_unique[i] for i in ind],  label="Unique connections in time period", c="blue")
ax2.set_ylabel("Num of unique combinations", c="blue")
ax2.set_ylim([0, len(li_sat_names)])
ax2.yaxis.set_major_locator(MaxNLocator(integer=True))

title_string = "How connected to the number of unqiue sats (Computed over "+str(total_timer)+" hours with "+str(len(li_sat_names))+" LEO satellites)"
plt.title(title_string)

plt.savefig(save_location+"/num_of_connections_percentage_of_max.png")
plt.savefig(save_location+"/../../data/connections_leo.png")
# plt.show()

plt.clf()






























