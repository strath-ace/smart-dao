# Area

import numpy as np
import csv
import matplotlib.pyplot as plt
from datasets import load_dataset

def per_province(column_name, dataset, do_plot=False, do_normalise=True):
    nuts_data = np.array(dataset[column_name])[:,0]
    # Sort nuts data
    indx = np.argsort(np.nanmean(nuts_data,axis=1))
    nuts_data = nuts_data[np.flip(indx)]
    # Normalise nuts data
    if do_normalise:
        nuts_data = nuts_data/np.nanmean(nuts_data,axis=0)
        nuts_data = 2*(nuts_data-np.nanmin(nuts_data,axis=0))/(np.nanmax(nuts_data,axis=0)-np.nanmin(nuts_data,axis=0))-1

    if do_plot:
        fig, axs = plt.subplots(1,1,figsize=(10,20))
        plt.imshow(nuts_data, cmap="seismic_r", aspect='auto')
        axs.invert_yaxis()
        plt.colorbar()
        plt.title("Area of crop per provinces")
        plt.savefig("regions.png")
        plt.clf()
        plt.close()

    return nuts_data


def per_province_bar(column_name, dataset):
    nuts_data = np.array(dataset[column_name])[:,0]
    provinces = np.array(dataset["province"])
    # Sort nuts data
    indx = np.argsort(np.nanmean(nuts_data,axis=1))
    nuts_data = nuts_data[np.flip(indx)]
    provinces = provinces[np.flip(indx)]
    # Normalise nuts data
    nuts_data = np.nanmean(nuts_data,axis=1)
    nuts_data = (nuts_data-np.nanmin(nuts_data,axis=0))/(np.nansum(nuts_data,axis=0))

    return nuts_data


def per_mixed(column_name, dataset, do_plot=False, do_normalise=True):
    nuts_data = np.array(dataset[column_name])[:,0]
    countrys = np.array(dataset["country"])
    uni_countrys = np.unique(countrys)

    nuts_by_country = []
    for uni in uni_countrys:
        nuts_by_country.append(np.nansum(nuts_data[countrys == uni],axis=0))
    nuts_by_country = np.array(nuts_by_country)

    # Sort country data
    indx2 = np.argsort(np.nanmean(nuts_by_country,axis=1))
    nuts_by_country = nuts_by_country[np.flip(indx2)]
    uni_countrys = uni_countrys[np.flip(indx2)]
    # Normalise country data
    if do_normalise:
        nuts_by_country = nuts_by_country/np.nanmean(nuts_by_country,axis=0)
        nuts_by_country = 2*(nuts_by_country-np.nanmin(nuts_by_country,axis=0))/(np.nanmax(nuts_by_country,axis=0)-np.nanmin(nuts_by_country,axis=0))-1

    if do_plot:
        # Plot country data
        fig, axs = plt.subplots(1,1,figsize=(10,20))
        plt.imshow(nuts_by_country, cmap="seismic_r", aspect='auto')
        plt.yticks(np.arange(np.shape(nuts_by_country)[0]), uni_countrys)
        axs.invert_yaxis()
        plt.colorbar()
        plt.title("Area of crop per country")
        plt.subplots_adjust(left=0.2)
        plt.savefig("countries_per_region.png")
        plt.clf()
        plt.close()

    return nuts_by_country


def per_mixed_bar(column_name, dataset):
    nuts_data = np.array(dataset[column_name])[:,0]
    countrys = np.array(dataset["country"])
    uni_countrys = np.unique(countrys)

    nuts_by_country = []
    for uni in uni_countrys:
        nuts_by_country.append(np.nansum(nuts_data[countrys == uni],axis=0))
    nuts_by_country = np.array(nuts_by_country)

    # Sort country data
    indx2 = np.argsort(np.nanmean(nuts_by_country,axis=1))
    nuts_by_country = nuts_by_country[np.flip(indx2)]
    uni_countrys = uni_countrys[np.flip(indx2)]
    # Normalise country data
    nuts_by_country =  np.nanmean(nuts_by_country,axis=1)
    nuts_by_country = (nuts_by_country-np.nanmin(nuts_by_country,axis=0))/(np.nansum(nuts_by_country,axis=0))

    return nuts_by_country


def per_country(column_name, dataset_countries, do_plot=False, do_normalise=True):
    nuts_data = np.array(dataset_countries[column_name])[:,0]
    countries = np.array(dataset_countries["province"])
    # Sort nuts data
    indx = np.argsort(np.nanmean(nuts_data,axis=1))
    nuts_data = nuts_data[np.flip(indx)]
    countries = countries[np.flip(indx)]
    # Normalise nuts data
    if do_normalise:
        nuts_data = nuts_data/np.nanmean(nuts_data,axis=0)
        nuts_data = 2*(nuts_data-np.nanmin(nuts_data,axis=0))/(np.nanmax(nuts_data,axis=0)-np.nanmin(nuts_data,axis=0))-1

    if do_plot:
        fig, axs = plt.subplots(1,1,figsize=(10,20))
        plt.imshow(nuts_data, cmap="seismic_r", aspect='auto')
        plt.yticks(np.arange(np.shape(nuts_data)[0]), countries)
        axs.invert_yaxis()
        plt.colorbar()
        plt.title("Area of crop per country")
        plt.savefig("countries_per_country.png")
        plt.clf()
        plt.close()

    return nuts_data