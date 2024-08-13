import tifffile as tiffio
import numpy as np
import matplotlib.pyplot as plt
import csv
import sys
from PIL import Image
import os
np.set_printoptions(edgeitems=12)


save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cropped")
if not os.path.exists(save_location):
    os.makedirs(save_location)

# Input
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

new_figs = []
c1 = 0

file_data = np.array(csv_input("data/data/neon_test_data.csv"))

files1s = file_data[1:,3]
files2s = file_data[1:,5]

for file1, file2 in zip(files1s, files2s):
    mats = tiffio.imread("data/data/images/"+file1)
    # print(np.shape(mats))
    mat_flat = tiffio.imread("data/data/images/"+file2)

    xs = [512,1024,1536,2048]
    ys = [512,1024,1536,2048]
    c = 0
    for x in xs:
        for y in ys:
            try:
                # print(np.shape(mats[x-512:x,y-512:y]))
                if np.shape(mats)[0] >= x and np.shape(mats)[1] >= y:
                    new_image = Image.fromarray(mats[x-512:x,y-512:y])
                    avg_height = np.mean(mat_flat[x-512:x,y-512:y])
                    new_figs.append(["c"+str(c1)+"_s"+str(c)+".tif", avg_height])
                    new_image.save(save_location+"/c"+str(c1)+"_s"+str(c)+".tif")
                    c += 1
            except:
                pass
            plt.clf()
    c1 += 1

# print(new_figs)
np.save("cropped_data", np.array(new_figs))
            