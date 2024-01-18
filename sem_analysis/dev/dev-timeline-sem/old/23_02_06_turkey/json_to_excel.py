import json
import csv
import time

# Open the JSON file and load its contents
with open('earthquakes_in_turkey.json', 'r') as json_file:
    json_data = json.load(json_file)

# Open a CSV file for writing
data_x = []
data_y = []
with open('earthquake_data.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)

    for data in json_data["features"]:
        date = data["properties"]["fromdate"][-8:]+" "+data["properties"]["fromdate"][0:10]
        date_clean = timestamp = int(time.mktime(time.strptime(date, '%H:%M:%S %Y-%m-%d')))
        output = [date_clean, data["properties"]["severitydata"]["severity"]]
        writer.writerow(output)
        data_x.append(round(date_clean, -2))
        data_y.append(data["properties"]["severitydata"]["severity"])





import matplotlib.pyplot as plt
import numpy as np
import math

min_time = round(min(data_x))
max_time = round(max(data_x))

arr_x = np.linspace(min_time, max_time, 1+round((max_time-min_time)/100))

arr_y = []

for i in range(len(arr_x)):
    if arr_x[i] in data_x:
        for ii in range(len(data_x)):
            if data_x[ii] == arr_x[i]:
                arr_y.append(math.pow(10,data_y[ii]))
    else:
        arr_y.append(0)


# print(arr_y)

plt.plot(arr_x, arr_y)
plt.savefig("fig.jpg")