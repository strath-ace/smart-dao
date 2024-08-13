import numpy as np
from tqdm import tqdm
import csv
import datasets
import glob
import os
import matplotlib.pyplot as plt

#    ["Province", "Country", ["Crop1 per year"], ["Crop2 per year"], ["Crop3 per year"]]

# Input
def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)   
    f.close()
    return output



initial_data = np.array(csv_input("global_crop_yields.csv"))

countries = np.unique(initial_data[1:,0])
removers = [
    'Upper-middle-income countries',
    'Low-income countries',
    'Lower-middle-income countries',
    'Ethiopia (former)',
    'European Union (27)',
    'Sudan (former)',
    'North America',
    'South America',
    'Europe',
    'Asia',
    'Oceania',
    'Africa',
    'Antartica',
    'World',
    'USSR'
]
countries_refined = []
for i in range(len(countries)):
    if "FAO" in countries[i]:
        pass
    elif countries[i] in removers:
        pass
    else:
        countries_refined.append(countries[i])

# print(countries_refined)
# print(len(countries_refined))
big_array = np.zeros((len(countries_refined), 203, 75))
big_array[big_array == 0] = np.nan

headings = initial_data[0,2:]

print(np.shape(headings))

for i, cou in enumerate(countries_refined):
    temp = initial_data[initial_data[:,0] == cou,1:]
    indx = np.argsort(np.array(temp[:,0],dtype=int))
    temp = temp[indx]
    temp[temp == ""] = np.nan
    temp = np.array(temp, dtype=float)
    big_array[i,:,np.array(temp[:,0],dtype=int)-1950] = temp[:,1:]
    # print(temp)
    # break

adder = []
for i in range(np.shape(big_array)[0]):
    temp = []
    for j in range(np.shape(big_array)[1]):
        temp.append([big_array[i,j]])

    adder.append(temp)
big_array = np.array(adder)


# print(np.shape(big_array))
# print(np.sum(np.isnan(big_array))/np.prod(np.shape(big_array)))
# # print(np.count_nonzero(big_array))

# std_to_plot = np.nanmean(np.nanstd((big_array-np.nanmin(big_array,axis=0))/(np.nanmax(big_array,axis=0)-np.nanmin(big_array,axis=0)), axis=0),axis=1)
# coeff_to_plot = np.nanmean(np.nanstd(big_array, axis=0)/np.nanmean(big_array, axis=0),axis=1)

# plt.hist(std_to_plot)
# plt.savefig("test.png")





create_dict = {}
create_dict.update({"country": countries_refined})
for i in range(len(headings)):
    create_dict.update({str(headings[i]): big_array[:,i,:,:]})

features_set = {}
features_set.update({"country": datasets.Value("string")})
for i in range(len(headings)):
    features_set.update({str(headings[i]): datasets.Array2D(shape=(1,75), dtype='float32')})

dataset = datasets.Dataset.from_dict(create_dict, features=datasets.Features(features_set))

# print(dataset["country"])

dataset.push_to_hub("0x365/crop-yield-global", private=True)






# print(dataset)


# f = open("colum_table.txt", "w")
# f.write("| Column  | Crop Type  |\n")
# f.write("|-----------|------------|\n")
# f.write("| | 0 | Province (NUTS 2 Region) |\n")
# f.write("| | 1 | Country |\n")
# c = 2
# for i in headings:
#     f.write("| "+str(c)+" | "+str(i)+" |\n")
#     c += 1
# f.close()




"""



"""








"""
dataset = datasets.Dataset.from_dict({
    "province": names,
    "country": v1,Area_Utilised_agricultural_area:,5,:,:],
    "v1x": to_file[:,6,:,:],
    "v1y": to_file[:,7,:,:],
    "v2x": to_file[:,8,:,:],
    "v2y": to_file[:,9,:,:],
    "v3x": to_file[:,10,:,:],
    "v3y": to_file[:,11,:,:]
    }, 
    features=datasets.Features({
        "id": datasets.Value("string"),
        "v1": datasets.Value("float32"),
        "v2": datasets.Value("float32"),
        "period": datasets.Value("float32"),
        "stability": datasets.Value("float32"),
        "collisional": datasets.Value("bool"),
        "r1x": datasets.Array2D(shape=(1,25), dtype='float32'),
        "r1y": datasets.Array2D(shape=(1,25), dtype='float32'),
        "r2x": datasets.Array2D(shape=(1,25), dtype='float32'),
        "r2y": datasets.Array2D(shape=(1,25), dtype='float32'),
        "r3x": datasets.Array2D(shape=(1,25), dtype='float32'),
        "r3y": datasets.Array2D(shape=(1,25), dtype='float32'),
        "v1x": datasets.Array2D(shape=(1,25), dtype='float32'),
        "v1y": datasets.Array2D(shape=(1,25), dtype='float32'),
        "v2x": datasets.Array2D(shape=(1,25), dtype='float32'),
        "v2y": datasets.Array2D(shape=(1,25), dtype='float32'),
        "v3x": datasets.Array2D(shape=(1,25), dtype='float32'),
        "v3y": datasets.Array2D(shape=(1,25), dtype='float32')
    }))

print(dataset)
# print((np.array(dataset[0]["r1x"])))

# dataset.push_to_hub("0x365/stable-orbits", private=True, split=f"part_{ii:05d}")
"""