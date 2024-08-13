import numpy as np
from tqdm import tqdm
import csv
import datasets
import glob
import os

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



initial_data = np.array(csv_input("output_data/Area_Arable land.csv"))[1:,0]
initial_data = initial_data[initial_data != "Extra-Regio NUTS 2"]
initial_data = initial_data[initial_data != "Extra-Regio NUTS 2 (NUTS 2021)"]

country_mapper = np.array(csv_input("country_aligned.csv"))

# print(len(initial_data))
# print(np.sum(country_mapper[:,0] == initial_data))

all_files = []
file_names_to_sort = []
for root, dirs, files in os.walk("./output_data", topdown=False):
    for name in files:
        all_files.append(os.path.join(root, name))
        file_names_to_sort.append(name)

# print(all_files)


table = []
for i in range(len(initial_data)):
    row = [initial_data[i], country_mapper[i,1]]
    table.append(row)
table = np.array(table)
    # for file in all_files:

# print(table)

name_to_sort = []

for file in file_names_to_sort:
    name_to_sort.append(file[5:])
    
# print(name_to_sort)
name_to_sort = np.array(name_to_sort, dtype=str)
indx = np.argsort(name_to_sort)

name_to_sort = name_to_sort[indx[::2]]

all_data = []
all_data_country = []
headings = []
for i in range(len(name_to_sort)):
    headings.append("Area_"+(name_to_sort[i])[:-4])
    csv_in = np.array(csv_input("output_data/Area_"+(name_to_sort[i])))[1:]
    csv_in = csv_in[csv_in[:,0] != "Extra-Regio NUTS 2"]
    csv_in = csv_in[csv_in[:,0] != "Extra-Regio NUTS 2 (NUTS 2021)"]
    csv_in = csv_in[:,1:]
    csv_in[csv_in == ':'] = np.nan
    csv_in = np.array(csv_in, dtype=float)
    all_data.append([csv_in])

    headings.append("Harv_"+(name_to_sort[i])[:-4])
    csv_in = np.array(csv_input("output_data/Harv_"+(name_to_sort[i])))[1:]
    csv_in = csv_in[csv_in[:,0] != "Extra-Regio NUTS 2"]
    csv_in = csv_in[csv_in[:,0] != "Extra-Regio NUTS 2 (NUTS 2021)"]
    csv_in = csv_in[:,1:]
    csv_in[csv_in == ':'] = np.nan
    csv_in = np.array(csv_in, dtype=float)
    all_data.append([csv_in])

    csv_in = np.array(csv_input("output_data_country/Area_"+(name_to_sort[i])))[1:]
    csv_in = csv_in[csv_in[:,0] != "Extra-Regio NUTS 2"]
    csv_in = csv_in[csv_in[:,0] != "Extra-Regio NUTS 2 (NUTS 2021)"]
    country_list = csv_in[:,0]
    csv_in = csv_in[:,1:]
    csv_in[csv_in == ':'] = np.nan
    csv_in = np.array(csv_in, dtype=float)
    all_data_country.append([csv_in])
    csv_in = np.array(csv_input("output_data_country/Harv_"+(name_to_sort[i])))[1:]
    csv_in = csv_in[csv_in[:,0] != "Extra-Regio NUTS 2"]
    csv_in = csv_in[csv_in[:,0] != "Extra-Regio NUTS 2 (NUTS 2021)"]
    country_list = csv_in[:,0]
    csv_in = csv_in[:,1:]
    csv_in[csv_in == ':'] = np.nan
    csv_in = np.array(csv_in, dtype=float)
    all_data_country.append([csv_in])


all_data = np.array(all_data)
all_data =np.swapaxes(all_data, 1,2)
all_data_country = np.array(all_data_country)
all_data_country =np.swapaxes(all_data_country, 1,2)

print(np.shape(all_data_country))

headings = np.array(headings)

for i in range(len(headings)):
    headings[i] = headings[i].replace(" ", "_")
    headings[i] = headings[i].replace(".", "")
    headings[i] = headings[i].replace(",", "")
    headings[i] = headings[i].replace(")", "")
    headings[i] = headings[i].replace("(", "")


# print(np.shape(all_data))
counters = []
for i in range(np.shape(all_data)[0]):
    counters.append(np.nansum(np.isnan(all_data[i])))
counters = np.array(counters)
indx = np.argsort(counters)
all_data = all_data[indx]
all_data_country = all_data_country[indx]
headings = headings[indx]


create_dict = {}
create_dict.update({"province": table[:,0], "country": table[:,1]})
for i in range(len(headings)):
    create_dict.update({str(headings[i]): all_data[i,:]})

features_set = {}
features_set.update({"province": datasets.Value("string"), "country": datasets.Value("string")})
for i in range(len(headings)):
    features_set.update({str(headings[i]): datasets.Array2D(shape=(1,25), dtype='float32')})

dataset = datasets.Dataset.from_dict(create_dict, features=datasets.Features(features_set))

dataset.push_to_hub("0x365/crop-yield-eu", split="regional")


create_dict = {}
create_dict.update({"province":country_list, "country": country_list})
for i in range(len(headings)):
    create_dict.update({str(headings[i]): all_data_country[i,:]})

features_set = {}
features_set.update({"province": datasets.Value("string"), "country": datasets.Value("string")})
for i in range(len(headings)):
    features_set.update({str(headings[i]): datasets.Array2D(shape=(1,25), dtype='float32')})

dataset_country = datasets.Dataset.from_dict(create_dict, features=datasets.Features(features_set))


dataset_country.push_to_hub("0x365/crop-yield-eu", split="country")




print(dataset)


f = open("colum_table.txt", "w")
f.write("| Column  | Crop Type  |\n")
f.write("|-----------|------------|\n")
f.write("| | 0 | Province (NUTS 2 Region) |\n")
f.write("| | 1 | Country |\n")
c = 2
for i in headings:
    f.write("| "+str(c)+" | "+str(i)+" |\n")
    c += 1
f.close()











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