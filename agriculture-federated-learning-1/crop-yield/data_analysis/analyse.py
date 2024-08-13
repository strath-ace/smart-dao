# Area

import numpy as np
import csv
import matplotlib.pyplot as plt
from datasets import load_dataset

from getter_funcs import *

# Input
def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)   
    f.close()
    return output



dataset = load_dataset("0x365/crop-yield-eu", split="regional")
dataset_countries = load_dataset("0x365/crop-yield-eu", split="country")
dataset_global = load_dataset("0x365/crop-yield-global", split="train")

#######################

col = "Area_Cereals_for_the_production_of_grain_including_seed"

#######################


# Example plots
per_province(col, dataset, do_plot=True)
per_mixed(col, dataset, do_plot=True)
per_country(col, dataset_countries, do_plot=True)



data1 = per_province_bar(col, dataset)
data2 = per_mixed_bar(col, dataset)

data1 = data1[~np.isnan(data1)]
data1 = data1[data1 != 0]
data2 = data2[~np.isnan(data2)]
data2 = data2[data2 != 0]
# data3 = per_country(col, dataset_countries)

fig, axs = plt.subplots(1,1,figsize=(10,10))
shaper = np.shape(data1)[0]/np.shape(data2)[0]
plt.barh(np.arange(0,np.shape(data1)[0]), -data1, label="Per Province", height=1)
plt.barh(np.arange(0,np.shape(data2)[0]), data2, label="Combined into countries")
# plt.barh(np.arange(0,np.shape(data3)[0]), data3, label="Per Country", alpha=0.3)
# plt.yticks(np.arange(np.shape(nuts_by_country)[0]), uni_countrys)
axs.invert_yaxis()
plt.plot([0,0], [0,np.shape(data1)[0]], c="black")
# plt.colorbar()
# plt.yscale("log")
# plt.ylim([np.shape(nuts_data)[0],0])
# plt.xlim([-np.amax(data2), np.amax(data2)])
plt.legend()
plt.title("Distribution of area of crop per Province")
plt.xlabel("Area of crop normalised to the total crop across EU")
plt.ylabel("Province or country")
plt.savefig("regions_bar.png")
plt.clf()
plt.close()




# Take std per year, then take mean across all years
std_per_province = []
coeff_per_province = []
std_per_mixed = []
coeff_per_mixed = []
for col in dataset.column_names[2:]:
    if "Harv_" in col:
        std_per_province.append(np.nanmean(np.nanstd(1+(0.5*per_province(col, dataset, do_normalise=True)), axis=0)))
        coeff_per_province.append(np.nanmean(np.nanstd(per_province(col, dataset, do_normalise=False), axis=0)/np.nanmean(per_province(col, dataset, do_normalise=False),axis=0)))
        std_per_mixed.append(np.nanmean(np.nanstd(1+(0.5*per_mixed(col, dataset, do_normalise=True)), axis=0)))
        coeff_per_mixed.append(np.nanmean(np.nanstd(per_mixed(col, dataset, do_normalise=False), axis=0)/np.nanmean(per_mixed(col, dataset, do_normalise=False),axis=0)))




std_per_province = np.array(std_per_province)
coeff_per_province = np.array(coeff_per_province)
std_per_mixed = np.array(std_per_mixed)
coeff_per_mixed = np.array(coeff_per_mixed)


# global_area = np.array(csv_input("land_area_by_country.csv"))
# global_area = np.array(global_area[:,1],dtype=float)
# coeff_global = np.std(global_area)/np.mean(global_area)
# global_area = (global_area-np.nanmin(global_area,axis=0))/(np.nanmax(global_area,axis=0)-np.nanmin(global_area,axis=0))

# print(np.shape(coeff_per_province))

coeff_per_province = coeff_per_province[~np.isnan(coeff_per_province)]
coeff_per_mixed = coeff_per_mixed[~np.isnan(coeff_per_mixed)]
std_per_province = std_per_province[~np.isnan(std_per_province)]
std_per_mixed = std_per_mixed[~np.isnan(std_per_mixed)]
# coeff_per_country = coeff_per_country[~np.isnan(coeff_per_country)]





# print(dataset_global["country"])

# Global
big_grid = []
# for i in range(len(dataset_global)):
big_grid = []
for j in dataset_global.column_names[1:]:
    big_grid.append(dataset_global[j])
big_grid = np.array(big_grid)
big_grid = np.swapaxes(big_grid,0,1)
big_grid = big_grid[:,:,0,-25:]

print(np.shape(big_grid))

std_to_plot = np.nanmean(np.nanstd((big_grid-np.nanmin(big_grid,axis=0))/(np.nanmax(big_grid,axis=0)-np.nanmin(big_grid,axis=0)), axis=0),axis=1)
coeff_to_plot = np.nanmean(np.nanstd(big_grid, axis=0)/np.nanmean(big_grid, axis=0),axis=1)



flanders = np.array(csv_input("flanders.csv"))[:,[1,2]]
flanders = np.array(flanders, dtype=float)

# 9120 for pasture and grass

std_per_crop = []
coeff_per_crop = []
for i in np.unique(flanders[:,1]):
#     print(np.shape([flanders[:,1] == i]))
    crop_areas = flanders[[flanders[:,1] == i][0],0]
    crop_areas_normalised = (crop_areas-np.nanmin(crop_areas))/(np.nanmax(crop_areas)-np.nanmin(crop_areas))
    std_per_crop.append(np.nanstd(crop_areas_normalised))
    coeff_per_crop.append(np.nanstd(crop_areas)/np.nanmean(crop_areas))



# For coefficient of variation
bins = np.linspace(0,np.amax([*coeff_per_province, *coeff_per_mixed]),20)
binned_coeff_per_province = np.histogram(coeff_per_province, bins)
binned_coeff_per_mixed = np.histogram(coeff_per_mixed, bins)
binned_coeff_per_global = np.histogram(coeff_to_plot, bins)
binned_coeff_per_field = np.histogram(coeff_per_crop, bins)
# binned_coeff_per_country = np.histogram(coeff_per_country, bins)


# For std
bins = np.linspace(0,0.5,20)
binned_std_per_province = np.histogram(std_per_province, bins)
binned_std_per_mixed = np.histogram(std_per_mixed, bins)
# binned_std_per_global = np.histogram(np.std(global_area), bins)
binned_std_per_global = np.histogram(std_to_plot, bins)
binned_std_per_field = np.histogram(std_per_crop, bins)





plt.bar(binned_coeff_per_field[1][:-1], binned_coeff_per_field[0]/np.sum(binned_coeff_per_field[0]),
        width=np.diff(binned_coeff_per_field[1]), edgecolor="black",
        align="edge", label="MICRO Level", alpha=0.3)
plt.bar(binned_coeff_per_province[1][:-1], binned_coeff_per_province[0]/np.sum(binned_coeff_per_province[0]),
        width=np.diff(binned_coeff_per_province[1]), edgecolor="black",
        align="edge", label="MESO Level", alpha=0.3)
plt.bar(binned_coeff_per_mixed[1][:-1], binned_coeff_per_mixed[0]/np.sum(binned_coeff_per_mixed[0]),
        width=np.diff(binned_coeff_per_mixed[1]), edgecolor="black",
        align="edge", label="MACRO Level", alpha=0.3)
# plt.bar(binned_coeff_per_global[1][:-1], binned_coeff_per_global[0]/np.sum(binned_coeff_per_global[0]),
#         width=np.diff(binned_coeff_per_global[1]), edgecolor="black",
#         align="edge", label="Countries Globally", alpha=0.3)

plt.title("Coefficient of Variation across each crop type")
plt.xlabel("Coefficient of Variation")
plt.ylabel("% of all crop types")
# plt.yscale("log")

# This graph shows that when looking at per province, the std is lower for a fewer number of datasets as these provinces dont
# provide the data. The problem with many provinces also means each dataset is smaller and there are more clients

plt.legend()
plt.savefig("coefficient_of_variation_in_region_group.png")
plt.clf()
plt.close()

# plt.bar(binned_std_per_field[1][:-1], binned_std_per_field[0]/np.sum(binned_std_per_field[0]),
#         width=np.diff(binned_std_per_field[1]), edgecolor="black",
#         align="edge", label="MICRO - Fields in Belgium Dataset", alpha=0.3)
# plt.bar(binned_std_per_province[1][:-1], binned_std_per_province[0]/np.sum(binned_std_per_province[0]),
#         width=np.diff(binned_std_per_province[1]), edgecolor="black",
#         align="edge", label="MESO - NUTS Level 2 Regions (EU)", alpha=0.3)
# plt.bar(binned_std_per_mixed[1][:-1], binned_std_per_mixed[0]/np.sum(binned_std_per_mixed[0]),
#         width=np.diff(binned_std_per_mixed[1]), edgecolor="black",
#         align="edge", label="MACRO - NUTS Level 2 Regions Combined into Countries (EU)", alpha=0.3)
# # plt.bar(binned_std_per_global[1][:-1], binned_std_per_global[0]/np.sum(binned_std_per_global[0]),
# #         width=np.diff(binned_std_per_global[1]), edgecolor="black",
# #         align="edge", label="Countries Globally", alpha=0.3)

plt.bar(binned_std_per_field[1][:-1], binned_std_per_field[0]/np.sum(binned_std_per_field[0]),
        width=np.diff(binned_std_per_field[1]), edgecolor="black",
        align="edge", label="MICRO Level", alpha=0.3)
plt.bar(binned_std_per_province[1][:-1], binned_std_per_province[0]/np.sum(binned_std_per_province[0]),
        width=np.diff(binned_std_per_province[1]), edgecolor="black",
        align="edge", label="MESO Level", alpha=0.3)
plt.bar(binned_std_per_mixed[1][:-1], binned_std_per_mixed[0]/np.sum(binned_std_per_mixed[0]),
        width=np.diff(binned_std_per_mixed[1]), edgecolor="black",
        align="edge", label="MACRO Level", alpha=0.3)
# plt.bar(binned_std_per_global[1][:-1], binned_std_per_global[0]/np.sum(binned_std_per_global[0]),
#         width=np.diff(binned_std_per_global[1]), edgecolor="black",
#         align="edge", label="Countries Globally", alpha=0.3)


plt.title("Standard Distribution across each crop type")
plt.xlabel("Standard Distribution")
plt.ylabel("% of all crop types")

# This graph shows that when looking at per province, the std is lower for a fewer number of datasets as these provinces dont
# provide the data. The problem with many provinces also means each dataset is smaller and there are more clients

plt.legend()
plt.savefig("std_in_region_group.png")
plt.clf()
plt.close()





