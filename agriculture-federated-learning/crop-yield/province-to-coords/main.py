import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import json
from datasets import load_dataset

# Input json
def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)

# Input csv
def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)   
    f.close()
    return output

# Get files
sheet_to_df_map = []
jsons_roots = []
for root, dirs, files in os.walk("data/"):
    for name in files:
        if name[-8:] == ".geojson":
            jsons_roots.append(os.path.join(root, name))


regions_only = np.array(csv_input("country_aligned.csv"))[:,0]

# print((regions_only))
# print("Ísland")

time = []
regions_new = []

nuts_years = [2003,2006,2010,2013,2016,2021]
for regions in regions_only:
    if "Extra-Regio NUTS 2" not in regions:
        found = False
        for nuts in nuts_years:
            if "(NUTS "+str(nuts)+")" in regions:
                regions_new.append(regions)#.replace("(NUTS "+str(nuts)+")", "").strip())
                time.append(nuts)
                found = True
                break
            if "(statistical region "+str(nuts)+")" in regions:
                regions_new.append(regions)#.replace("(statistical region "+str(nuts)+")", "").strip())
                time.append(nuts)
                found = True
                break
        if not found:
            regions_new.append(regions.strip())
            time.append(9999)


# for i in range(len(regions_new)):
#     print(regions_new[i], "\t\t\t", time[i])

regions2 = regions_new.copy()


dataset_years = load_dataset("0x365/crop-yield-eu", split="regional")
# print(dataset_years["province"])

harvest_amounts = []
for col in dataset_years.column_names[2:]:
    if "Harv_" in col:
        harvest_amounts.append(np.array(dataset_years[col])[:,0])
harvest_amounts = np.array(harvest_amounts,dtype=float)

harvest_amounts = ~np.isnan(harvest_amounts)

years_unsorted = np.mean(np.sum(harvest_amounts, axis=2), axis=0)

# print(np.shape(harvest_amounts))
# print(np.shape(years_unsorted))
# years


years = []
for reg in regions2:
    if len(years_unsorted[np.array(dataset_years["province"]) == reg]) == 0:
        print(reg)
    years.append(years_unsorted[np.array(dataset_years["province"]) == reg][0])

# print(np.shape(years))




numbers = []
for i in jsons_roots:
    numbers.append(i[-17:-13])
indx = np.flip(np.argsort(numbers))
jsons_roots = np.array(jsons_roots)[indx]
numbers = np.array(numbers)[indx]

pos2 = []
for i in range(len(regions_new)):
    pos2.append([])


for k, js in enumerate(jsons_roots):
    # print(k)
    js_data = load_json(js)["features"]
    js_names = []
    # levels = []
    # for i in range(len(js_data)):
    #     levels.append(js_data[i]["properties"]["LEVL_CODE"])
    # indx = np.argsort(levels)
    # js_data_new = []
    # for x in indx:
    #     js_data_new.append(js_data[x])
    # js_data = js_data_new
    pos = []
    for i in range(len(js_data)):
        if js_data[i]["properties"]["LEVL_CODE"] >= 0:
            try:
                js_names.append(js_data[i]["properties"]["NAME_LATN"])
                pos.append(i)
            except:
                js_names.append(js_data[i]["properties"]["NUTS_NAME"])
                pos.append(i)

    for j, name in enumerate(js_names):
        for ii in range(len(regions_new)):
            if int(numbers[k]) <= int(time[ii]):
                if name in regions_new[ii]:
                    if name == "Ísland":
                        print("dounf")
                    pos2[ii].append([int(numbers[k]), pos[j]])
                    regions_new[ii] = regions_new[ii].replace(name, " ")
                    break
                elif name == "Région de Bruxelles-Capitale / Brussels Hoofdstedelijk Gewest" and regions_new[ii] == "Région de Bruxelles-Capitale/Brussels Hoofdstedelijk Gewest":
                    pos2[ii].append([int(numbers[k]), pos[j]])
                    regions_new[ii] = regions_new[ii].replace(name, " ")
                    break
                elif name == "Prov. Brabant Wallon" and regions_new[ii] == "Prov. Brabant wallon":
                    pos2[ii].append([int(numbers[k]), pos[j]])
                    regions_new[ii] = regions_new[ii].replace(name, " ")
                    break
                elif name == "Nisia Aigaiou, Kriti" and regions_new[ii] == "Nisia Aigaiou":
                    pos2[ii].append([int(numbers[k]), pos[j]])
                    regions_new[ii] = regions_new[ii].replace(name, " ")
                    break
                elif name == "Ile-de-France" and regions_new[ii] == "Ile de France":
                    pos2[ii].append([int(numbers[k]), pos[j]])
                    regions_new[ii] = regions_new[ii].replace(name, " ")
                    break
                elif name == "Region Šumadije i Zapadne Srbije" and regions_new[ii] == "Region Sumadije i Zapadne Srbije":
                    pos2[ii].append([int(numbers[k]), pos[j]])
                    regions_new[ii] = regions_new[ii].replace(name, " ")
                    break
                elif name == "Region Južne i Istočne Srbije" and regions_new[ii] == "Region Juzne i Istocne Srbije":
                    pos2[ii].append([int(numbers[k]), pos[j]])
                    regions_new[ii] = regions_new[ii].replace(name, " ")
                    break


    


nuts_years = np.array([2003,2006,2010,2013,2016,2021])
flat_count = np.array([0   ,1   ,2   ,3   ,4   ,5   ])
js_data_all = []
for nuts in nuts_years:
    js_data = load_json("data/NUTS_RG_10M_"+str(nuts)+"_4326.geojson")["features"]
    # levels = []
    # for i in range(len(js_data)):
    #     levels.append(js_data[i]["properties"]["LEVL_CODE"])
    # indx = np.argsort(levels)
    # print(indx)
    # js_data_new = []
    # for x in indx:
    #     js_data_new.append(js_data[x])
    # js_data = js_data_new
    js_data_all.append(js_data)
    

pos_real = []
for x in pos2:
    temp = []
    for y in x:
        # print()
        tempor = js_data_all[flat_count[nuts_years == y[0]][0]][y[1]]["geometry"]["coordinates"]
        try:
            if tempor[0][0][0][0] > -99999999:
                for z in tempor:
                    temp.append(z)
        except:
            temp.append(tempor)
    pos_real.append(temp)




feature_array = []
for x in zip(regions2, pos_real, years):
    if len(x[1]) > 0:
        feature_array.append({
            "type": "Feature",
            "geometry": {
                "type": "MultiPolygon",
                "coordinates":x[1]
            },
            "properties": {
                "name": x[0],
                "years": x[2]
            }
        })
    else:
        print("Bad", x[0])



json_file = {
    "type": "FeatureCollection",
    "features": feature_array,
    "crs": {
        "type": "name",
        "properties": {
        "name": "urn:ogc:def:crs:EPSG::4326"
        }
    }
}


save_json("test.geojson", json_file)
