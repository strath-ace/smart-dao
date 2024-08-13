import numpy as np
import csv


cropped_data = np.load("cropped_data.npy").tolist()

new_data = []
for x in cropped_data:
    new_data.append([x[0], float(x[1])])

def csv_output(file_name, data_send):
    with open(file_name, "w") as f:
        if len(data_send) == 0:
            f.close()
            return
        else:
            for item in data_send:
                csv.writer(f).writerow(item)
            f.close()
            return
        

csv_output("cropped_data.csv", new_data)