import os
import json
import csv

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from scipy.stats import norm

import statistics

SEC_IN_HOUR = 60*60
MAX_PLOT = SEC_IN_HOUR * 600










def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output






def get_all_events(all_data):
    all_events = all_data['all_activations']
    all_events = [eval(i) for i in all_events]
    all_events = sorted(all_events)
    all_events = [str(i) for i in all_events]
    return all_events








def plot_country_in(all_data, save_file, country_of, save_path):
    """
    Counts the number of countries for each pie chart
    """
    if save_file == "copernicus":
        total_number = 654
    else:
        total_number = 812
    all_events = get_all_events(all_data)
    store_li = []
    store_count_li = []
    counter = 0
    for event in all_events:
        try:
            data = all_data[event]
            data_li = data["country_of_"+country_of]['location']
            temp = []
            for point in data_li:
                if point not in temp:
                    temp.append(point)
            data_li = temp
            if len(data_li) > 0:
                for country in data_li:
                    if country == "":
                        continue
                    elif country not in store_li:
                        store_li.append(country)
                        store_count_li.append(1)
                    else:
                        for i in range(len(store_li)):
                            if country == store_li[i]:
                                store_count_li[i] += 1
                                break
                counter += 1
        except:
            continue
    y = np.array(store_count_li)
    mylabels = store_li
    usefulness = 100*counter/total_number
    plt.subplots(figsize=(15,15))
    fig, ax =  plt.pie(y, labels = mylabels, rotatelabels=True, radius=0.9)
    plt.title(save_file+" Division of Country of "+country_of+" ("+str(round(usefulness))+"% of all activations analysed)")
    plt.savefig(save_path+"/pie_"+save_file+"_country_of_"+country_of+"_transparent.png", transparent=True)
    plt.savefig(save_path+"/pie_"+save_file+"_country_of_"+country_of+".png", transparent=False)
    plt.clf()










def plot_country_in_hdi(all_data, save_file, country_of, save_path):
    """
    Counts the number of countries within each hdi region for each pie chart
    """
    if save_file == "copernicus":
        total_number = 654
    else:
        total_number = 812
    all_events = get_all_events(all_data)
    hdi_very_high = 0
    hdi_high = 0
    hdi_medium = 0
    hdi_low = 0
    counter = 0
    for event in all_events:
        try:
            data = all_data[event]
            if data["country_of_"+country_of]['hdi'] > 0:
                if data["country_of_"+country_of]['hdi'] >= 0.8:
                    hdi_very_high += 1
                elif data["country_of_"+country_of]['hdi'] >= 0.7:
                    hdi_high += 1
                elif data["country_of_"+country_of]['hdi'] >= 0.55:
                    hdi_medium += 1
                else:
                    hdi_low += 1
            counter += 1
        except:
            continue

    if hdi_very_high > 0 or hdi_high > 0 or hdi_medium > 0 or hdi_low > 0:
        usefulness = 100*counter/total_number
        y = np.array([hdi_very_high, hdi_high, hdi_medium, hdi_low])
        mylabels = ["Very High", "High", "Medium", "Low"]
        plt.subplots(figsize=(5,5))
        plt.pie(y, labels = mylabels, rotatelabels=False)
        plt.title(save_file+" Division of Country of "+country_of+" ("+str(round(usefulness))+"% of all activations analysed)")
        plt.savefig(save_path+"/pie_"+save_file+"_country_of_"+country_of+"_hdi_transparent.png", transparent=True)
        plt.savefig(save_path+"/pie_"+save_file+"_country_of_"+country_of+"_hdi.png", transparent=False)
        plt.clf()
    else:
        print("No plot - pie_"+save_file+"_country_of_"+country_of+"_hdi")










def plot_times_copernicus(all_data, save_file, save_path):
    """
    Plots time graphs for copernicus
    """
    all_events = get_all_events(all_data)
    x = []
    date_a_li = []
    phase_a_li = []
    phase_b_li = []
    phase_c_li = []
    for event in all_events:
        try:
            data = all_data[event]
            good = 1
            try:
                date_a = data["event_date"]
            except:
                good = 0
            try:
                date_b = data['activation_date']
            except:
                good = 0
            try:
                date_c = data['sat_data_date']
            except:
                good = 0
            try:
                date_d = data['publish_date']
            except:
                good = 0
            if good:
                below = date_b-date_a < MAX_PLOT and date_c-date_b < MAX_PLOT and date_d-date_c < MAX_PLOT
                above = date_b-date_a > 0 and date_c-date_b > 0 and date_d-date_c > 0
                if below and above:
                    x.append(int(event))
                    date_a_li.append(date_a / (SEC_IN_HOUR*24))
                    phase_a_li.append((date_b - date_a) / SEC_IN_HOUR)
                    phase_b_li.append((date_c - date_b) / SEC_IN_HOUR)
                    phase_c_li.append((date_d - date_c) / SEC_IN_HOUR)
        except:
            continue

    x_per = []
    phase_a_li_per = []
    phase_b_li_per = []
    phase_c_li_per = []

    for i in range(len(x)):
        total = phase_a_li[i] + phase_b_li[i] + phase_c_li[i]
        x_per.append(x[i])
        phase_a_li_per.append(100*phase_a_li[i]/total)
        phase_b_li_per.append(100*phase_b_li[i]/total)
        phase_c_li_per.append(100*phase_c_li[i]/total)

    window = 15 # 11 good

    # Abs Smoothing
    data = phase_a_li
    average_data = []
    for ind in range(len(data) - window + 1):
        average_data.append(np.mean(data[ind:ind+window]))
    phase_a_li = average_data

    data = phase_b_li
    average_data = []
    for ind in range(len(data) - window + 1):
        average_data.append(np.mean(data[ind:ind+window]))
    phase_b_li = average_data

    data = phase_c_li
    average_data = []
    for ind in range(len(data) - window + 1):
        average_data.append(np.mean(data[ind:ind+window]))
    phase_c_li = average_data

    # Per Smoothing
    data = phase_a_li_per
    average_data = []
    for ind in range(len(data) - window + 1):
        average_data.append(np.mean(data[ind:ind+window]))
    phase_a_li_per = average_data

    data = phase_b_li_per
    average_data = []
    for ind in range(len(data) - window + 1):
        average_data.append(np.mean(data[ind:ind+window]))
    phase_b_li_per = average_data

    data = phase_c_li_per
    average_data = []
    for ind in range(len(data) - window + 1):
        average_data.append(np.mean(data[ind:ind+window]))
    phase_c_li_per = average_data
    
    for i in range(int((window-1)/2)):
        x.pop(len(x)-1)
        x.pop(0)
        x_per.pop(len(x_per)-1)
        x_per.pop(0)
        date_a_li.pop(len(x)-1)
        date_a_li.pop(0)

    if 1:
        plt.stackplot(x, phase_a_li, phase_b_li, phase_c_li, labels=['Phase A','Phase B','Phase C'])
        plt.legend(loc='upper left')
        #plt.title(save_file+" Division of Country of manager ("+str(round(usefulness))+"% of datapoints useable)")
        plt.savefig(save_path+"/stackline_"+save_file+"_plot_times.png")
        plt.clf()

        phase_all_li = []
        for i in range(len(x)):
            phase_all_li.append(phase_a_li[i] + phase_b_li[i] + phase_c_li[i])
        fig, ax = plt.subplots()
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=365))
        ax.stackplot(date_a_li, phase_a_li_per, phase_b_li_per, phase_c_li_per, labels=['Phase A','Phase B','Phase C'])
        ax.legend(loc='lower left')
        ax.set_ylabel("Percentage of total time given to each phase (%)")
        ax.set_xlabel("Timestamp")
        plt.gcf().autofmt_xdate()
        ax2 = ax.twinx()
        ax2.plot(date_a_li, phase_all_li, color="black")
        ax2.set_ylabel('Total time event to data publish (Hours)')
        plt.title("Phase times of Copernicus Satellite-based Emergency Mapping")

        #plt.title(save_file+" Division of Country of manager ("+str(round(usefulness))+"% of datapoints useable)")
        plt.savefig(save_path+"/stackline_"+save_file+"_plot_times_percentage_transparent.png", transparent=True)
        plt.savefig(save_path+"/stackline_"+save_file+"_plot_times_percentage.png", transparent=False)
        plt.clf()
    else:
        print("No plot - stackline_"+save_file+"_plot_times")











def plot_time_since_last_activations(all_data, save_file, save_path):
    """
    Plots time graphs for copernicus
    """
    all_events = get_all_events(all_data)
    x = []
    time_since = []
    date_a_li = []
    date_prev = 0
    for event in all_events:
        try:
            data = all_data[event]
            good = 1
            try:
                date_a = data["activation_date"]
            except:
                good = 0
            if good:
                below = 1#date_a < MAX_PLOT
                above = date_a > 0
                if below and above:
                    x.append(int(event))
                    time_since.append((date_a - date_prev) / (SEC_IN_HOUR))
                    date_a_li.append(date_a / (SEC_IN_HOUR*24))
                    date_prev = date_a
        except:
            continue

    tempt = []
    tempx = []
    tempd = []
    for i in range(len(time_since)):
        if time_since[i] > 0:
            tempt.append(time_since[i])
            tempx.append(x[i])
            tempd.append(date_a_li[i])
    x = tempx
    time_since = tempt
    date_a_li = tempd

    x.pop(0)
    time_since.pop(0)
    date_a_li.pop(0)

    time_interp = []
    prev = time_since[0]
    next = time_since[1]
    prevd = date_a_li[0]
    nextd = date_a_li[1]
    date_interp = []
    xi = 0
    for i in range(x[0], x[len(x)-1]):
        if i in x:
            for ii in range(len(x)):
                if x[ii] == i:
                    xi = ii
                    time_interp.append(time_since[xi])
                    date_interp.append(date_a_li[xi])
                    break
            prev = time_since[xi]
            next = time_since[xi+1]
            prevd = date_a_li[xi]
            nextd = date_a_li[xi+1]
        else:
            interp = prev + (i-x[xi])*(next-prev)/(x[xi+1]-x[xi])
            interp2 = prevd + (i-x[xi])*(nextd-prevd)/(x[xi+1]-x[xi])
            time_interp.append(interp)
            date_interp.append(interp2)

    print(len(range(x[len(x)-1])))
    print(len(time_interp))

    #date_a_li.pop(0)

    # # event_date vs time_since_last_event

    fig, ax = plt.subplots()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=365))
    ax.plot(date_interp, time_interp, color="black")
    ax.legend(loc='lower left')
    ax.set_ylabel("Time since last activation")
    ax.set_xlabel("Timestamp")
    plt.gcf().autofmt_xdate()
    # ax2 = ax.twinx()
    # ax2.set_ylabel('Total time event to data publish (Hours)')
    #plt.title("Phase times of Copernicus Satellite-based Emergency Mapping")

    #plt.title(save_file+" Division of Country of manager ("+str(round(usefulness))+"% of datapoints useable)")
    plt.savefig(save_path+"/event_date_vs_time_since_last_"+save_file+"_tranparent.png", transparent=True)
    plt.savefig(save_path+"/event_date_vs_time_since_last_"+save_file+".png", transparent=False)
    plt.clf()



















def plot_active_activations(all_data, save_file, save_path):
    """
    Plots time graphs for copernicus
    """
    all_events = get_all_events(all_data)
    x = []
    date_a_li = []
    date_b_li = []
    for event in all_events:
        try:
            data = all_data[event]
            good = 1
            try:
                date_a = data["activation_date"]
            except:
                good = 0
            try:
                date_b = data["publish_date"]
            except:
                good = 0
            if good:
                below = 1
                above = date_a > 0 and date_b > 0 and date_a < date_b
                if below and above:
                    x.append(int(event))
                    date_a_li.append(date_a)
                    date_b_li.append(date_b)
        except:
            continue

    all_dates = range(min(date_a_li)-10, max(date_b_li)+10, 10)


    num_li = []
    out_dates = []
    current = 0
    for date in all_dates:
        if date in date_a_li:
            for i in date_a_li:
                if i == date:
                    current += 1
        if date in date_b_li:
             for i in date_b_li:
                if i == date:
                    current -= 1
        num_li.append(current)
        out_dates.append(date / (SEC_IN_HOUR*24))


    fig, ax = plt.subplots()
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=365))
    ax.plot(out_dates, num_li, color="black")
    ax.legend(loc='lower left')
    ax.set_ylabel("Number of Active Activations")
    ax.set_xlabel("Timestamp")
    plt.gcf().autofmt_xdate()
    # ax2 = ax.twinx()
    # ax2.set_ylabel('Total time event to data publish (Hours)')
    #plt.title("Phase times of Copernicus Satellite-based Emergency Mapping")

    #plt.title(save_file+" Division of Country of manager ("+str(round(usefulness))+"% of datapoints useable)")
    plt.savefig(save_path+"/active_activations_"+save_file+"_transparent.png", transparent=True)
    plt.savefig(save_path+"/active_activations_"+save_file+".png", transparent=False)
    plt.clf()














def sort_list_my(input1, input2):
        # First is the one to sort by
        # The second is sorted with it
        temp1 = []
        temp2 = []
        while len(input1) > 0:
            min_value = min(input1)
            min_index = input1.index(min_value)
            temp1.append(input1[min_index])
            temp2.append(input2[min_index])
            input1.pop(min_index)
            input2.pop(min_index)
        return temp1, temp2


def big_boy(all_data, save_file, clean_data, save_path):
    """
    Plots time graphs for copernicus
    """
    if save_file == "copernicus":
        total_number = 654
    else:
        total_number = 812
    all_events = get_all_events(all_data)
    clean_all_events = get_all_events(clean_data)
    x = []
    date_a_li = []
    phase_a_li = []
    phase_b_li = []
    phase_c_li = []
    count = 0
    for event in all_events:
        try:
            data = all_data[event]
            good = 1
            try:
                date_a = data["event_date"]
            except:
                good = 0
            try:
                date_b = data['activation_date']
            except:
                good = 0
            try:
                date_c = data['sat_data_date']
            except:
                good = 0
            try:
                date_d = data['publish_date']
            except:
                good = 0
            if good:
                
                below = 1#date_b-date_a < MAX_PLOT and date_c-date_b < MAX_PLOT and date_d-date_c < MAX_PLOT
                above = date_b-date_a > 0 and date_c-date_b > 0 and date_d-date_c > 0
                if below and above:
                    count += 1
                    x.append(int(event))
                    date_a_li.append(date_a / (SEC_IN_HOUR*24))
                    phase_a_li.append((date_b - date_a) / SEC_IN_HOUR)
                    phase_b_li.append((date_c - date_b) / SEC_IN_HOUR)
                    phase_c_li.append((date_d - date_c) / SEC_IN_HOUR)
        except:
            continue


    temp, x = sort_list_my(date_a_li[:], x)
    temp, phase_a_li = sort_list_my(date_a_li[:], phase_a_li)
    temp, phase_b_li = sort_list_my(date_a_li[:], phase_b_li)
    date_a_li, phase_c_li = sort_list_my(date_a_li[:], phase_c_li)


    x_per = []
    phase_a_li_per = []
    phase_b_li_per = []
    phase_c_li_per = []

    for i in range(len(x)):
        total = phase_a_li[i] + phase_b_li[i] + phase_c_li[i]
        x_per.append(x[i])
        phase_a_li_per.append(100*phase_a_li[i]/total)
        phase_b_li_per.append(100*phase_b_li[i]/total)
        phase_c_li_per.append(100*phase_c_li[i]/total)

    window = 15 # 11 good

    # Abs Smoothing
    # data = phase_a_li
    # average_data = []
    # for ind in range(len(data) - window + 1):
    #     average_data.append(np.mean(data[ind:ind+window]))
    # phase_a_li = average_data

    # data = phase_b_li
    # average_data = []
    # for ind in range(len(data) - window + 1):
    #     average_data.append(np.mean(data[ind:ind+window]))
    # phase_b_li = average_data

    # data = phase_c_li
    # average_data = []
    # for ind in range(len(data) - window + 1):
    #     average_data.append(np.mean(data[ind:ind+window]))
    # phase_c_li = average_data

    # Per Smoothing
    data = phase_a_li_per
    average_data = []
    for ind in range(len(data) - window + 1):
        average_data.append(np.mean(data[ind:ind+window]))
    phase_a_li_per = average_data

    data = phase_b_li_per
    average_data = []
    for ind in range(len(data) - window + 1):
        average_data.append(np.mean(data[ind:ind+window]))
    phase_b_li_per = average_data

    data = phase_c_li_per
    average_data = []
    for ind in range(len(data) - window + 1):
        average_data.append(np.mean(data[ind:ind+window]))
    phase_c_li_per = average_data
    
    for i in range(int((window-1)/2)):
        x.pop(len(x)-1)
        x.pop(0)
        x_per.pop(len(x_per)-1)
        x_per.pop(0)
        date_a_li.pop(len(x)-1)
        date_a_li.pop(0)


    # phase_all_li = []
    # for i in range(len(x)):
    #     phase_all_li.append(phase_a_li[i] + phase_b_li[i] + phase_c_li[i])

    #phase_all_li = []
    total_time = []
    active_start = []
    active_end = []
    timestamp = []
    for event in clean_all_events:
        data = clean_data[event]
        event_date = data['event_date']
        activations = data['activation_date']
        publish = data['publish_date']
        temp = []
        for i in range(len(event_date)):
            if event_date[i] > 0:
                temp.append(event_date[i])
        if len(temp) > 0:
            event_date = statistics.mode(temp)
            min_activation = 99999999999999999999
            for i in range(len(activations)):
                if activations[i] > event_date and activations[i] < min_activation:
                    min_activation = activations[i]
            if min_activation != 99999999999999999999:
                min_publish = 99999999999999999999
                for i in range(len(publish)):
                    if publish[i] > min_activation and publish[i] < min_publish:
                        min_publish = publish[i]
                
                max_publish = 0
                for i in range(1, len(publish)):
                    if publish[i] > min_activation and max_publish < publish[i]:
                        max_publish = publish[i]

                if min_publish != 99999999999999999999:
                    dif = min_publish-event_date
                    if dif < MAX_PLOT*50:
                        total_time.append(dif)
                        timestamp.append(event_date)

                # if min_publish != 99999999999999999999:
                #     active_start.append(min_activation)
                #     active_end.append(min_publish)
                if max_publish != 0:
                    active_start.append(min_activation)
                    active_end.append(max_publish)

    timestamp, total_time = sort_list_my(timestamp, total_time)

    window = 25

    
    total_time = np.array(total_time) / SEC_IN_HOUR

    data = total_time
    average_data = []
    for ind in range(len(data) - window + 1):
        average_data.append(np.mean(data[ind:ind+window]))
    total_time = average_data

    for i in range(int((window-1)/2)):
        timestamp.pop(len(x)-1)
        timestamp.pop(0)

    timestamp = np.array(timestamp) / (SEC_IN_HOUR*24)
    
    SMALL_SIZE = 50
    MEDIUM_SIZE = 75
    BIGGER_SIZE = 100

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

    fig, ax = plt.subplots(2, 1, height_ratios=[6, 1], figsize=(50,30)) # fig size default 20,10
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=365))
    ax[0].stackplot(date_a_li, phase_a_li_per, phase_b_li_per, phase_c_li_per, labels=['Phase A','Phase B','Phase C'])
    ax[0].legend(loc='lower left')
    ax[0].set_ylabel("Percentage of total time given to each phase (%)", rotation=90, wrap=True, labelpad=100)
    ax[0].set_ylim(0, 100)
    ax[0].set_xlabel("Timestamp")
    ax[0].set_xlim(min(timestamp), max(date_a_li))
    plt.gcf().autofmt_xdate()
    ax2 = ax[0].twinx()
    ax2.plot(timestamp, total_time, color="black")
    ax2.set_ylim(0, 600)
    
    left, right = plt.xlim()
    ax2.set_ylabel('Total time of all phases combined (Hours)', rotation=90, wrap=True, labelpad=100)
    counter = len(timestamp)

    print(right, max(date_a_li))   
    

    all_dates = range(round(left*(SEC_IN_HOUR*24)-10), round(right*(SEC_IN_HOUR*24)+10), 10)
    print("Started active SEM section")

    start = left*(SEC_IN_HOUR*24)
    end = right*(SEC_IN_HOUR*24)
    num_li = []
    out_dates = []
    current = 0
    for date in all_dates:
        if date % 1000000 == 0:
            print(100*(date-start)/(end-start))
        if date in active_start:
            for i in active_start:
                if i == date:
                    current += 1
        if date in active_end:
             for i in active_end:
                if i == date:
                    current -= 1
        num_li.append(current)
        out_dates.append(date/(SEC_IN_HOUR*24))
    ax[1].plot(out_dates, num_li, color="black")
    ax[1].set_xlim(left, right)
    ax[1].set_ylim(0, 10)
    
    ax[1].set_xlabel("Date", labelpad=100)
    ax[1].set_ylabel("Active SEM", rotation=90, wrap=True, labelpad=100)
    #plt.xlim(left, right) 
    usefulness = 100*counter/total_number
    plt.title("Phase times of Copernicus Satellite-based Emergency Mapping")
    plt.savefig(save_path+"/"+save_file+"_big_time_graph_transparent.png", transparent=True)
    plt.savefig(save_path+"/"+save_file+"_big_time_graph.png", transparent=False)
    plt.clf()











def pdf(x):
    mean = np.mean(x)
    std = np.std(x)
    y_out = 1/(std * np.sqrt(2 * np.pi)) * np.exp( - (x - mean)**2 / (2 * std**2))
    return y_out

def plot_hdi_comparison(all_data, save_path):
    """
    Counts the number of countries within each hdi region for each pie chart
    """
    total_number = 812
    all_events = get_all_events(all_data)
    act_li = []
    sat_li = []
    man_li = []
    for event in all_events:
        try:
            data = all_data[event]
            activation_check = data["country_of_activation"]['hdi'] > 0
            sat_check = data["country_of_sat"]['hdi'] > 0
            manager_check = data["country_of_manager"]['hdi'] > 0
            if activation_check and sat_check and manager_check:
                act_li.append(data["country_of_activation"]['hdi'])
                sat_li.append(data["country_of_sat"]['hdi'])
                man_li.append(data["country_of_manager"]['hdi'])
        except:
            continue


    act_li = np.array(act_li)
    sat_li = np.array(sat_li)
    man_li = np.array(man_li)

    act_li = np.sort(act_li)
    sat_li = np.sort(sat_li)
    man_li = np.sort(man_li)

    x = np.arange(0, 1, 0.001)

    act_y = norm.pdf(x, np.mean(act_li), np.std(act_li))
    sat_y = norm.pdf(x, np.mean(sat_li), np.std(sat_li))
    man_y = norm.pdf(x, np.mean(man_li), np.std(man_li))


    # act_y = pdf(act_li)
    # sat_y = pdf(sat_li)
    # man_y = pdf(man_li)


    counter = len(act_li)

    SMALL_SIZE = 20
    MEDIUM_SIZE = 75
    BIGGER_SIZE = 100

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=15)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    
    fig, ax = plt.subplots(figsize=(10,6))

    width_line = 5

    #y = np.array([hdi_very_high, hdi_high, hdi_medium, hdi_low])
    plt.plot(x, act_y, label="SEM Activators", linewidth=width_line)
    plt.plot(x, sat_y, label="Satellite Data Providers", linewidth=width_line)
    plt.plot(x, man_y, label="SEM Managers", linewidth=width_line)
    plt.xlim(0, 1)
    plt.legend()
    plt.xlabel("Average Human Development Index (HDI) of an Activation")
    plt.ylabel("Probability (%)")
    usefulness = 100*counter/total_number
    plt.title("ICSMD HDI for activation, management and satellite operators", wrap=True)
    plt.savefig(save_path+"/icsmd_hdi_transparent.png", transparent=True)
    plt.savefig(save_path+"/icsmd_hdi.png", transparent=False)
    plt.clf()







def plot_activations_per_year(save_path):

    years = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 
             2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

    copernicus = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21, 34, 45, 31, 33, 63, 71, 75, 71, 61, 75]

    icsmd = [11, 17, 17, 21, 23, 25, 43, 40, 43, 54, 32, 41, 40, 41, 38, 31, 44, 33, 43, 55, 53, 51]

    sentinel = [0, 0, 0, 0, 0, 0, 15, 16, 21, 32, 31, 19, 19, 17, 24, 34, 32, 30,  25 , 28, 33, 28]
    
    total = []
    for i in range(len(years)):
        total.append(copernicus[i]+icsmd[i]+sentinel[i])

    combined_titles = ["Copernicus", "ICSMD", "Sentinel-Asia", "All methods combined"]
    combined = [copernicus, icsmd, sentinel, total]

    np.array(combined)
    np.array(combined_titles)

    SMALL_SIZE = 20
    MEDIUM_SIZE = 75
    BIGGER_SIZE = 100

    plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
    plt.rc('axes', titlesize=SMALL_SIZE)     # fontsize of the axes title
    plt.rc('axes', labelsize=SMALL_SIZE)    # fontsize of the x and y labels
    plt.rc('xtick', labelsize=15)    # fontsize of the tick labels
    plt.rc('ytick', labelsize=15)    # fontsize of the tick labels
    plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
    plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title
    
    fig, ax = plt.subplots(figsize=(10,10))

    for i in range(len(combined)):#
        a, b = np.polyfit(years, combined[i], 1)

        this_data = []
        this_year = []
        for ii in range(len(combined[i])):
            if combined[i][ii] != 0:
                this_data.append(combined[i][ii])
                this_year.append(years[ii])
        
        markers = np.array([this_year[0], this_year[-1]])

        plt.scatter(this_year, this_data, label=combined_titles[i])
        plt.plot(markers, a*markers+b)

    

    plt.legend()
    plt.ylim(0, )
    plt.xlabel("Year")
    plt.ylabel("Number of activations")
    plt.title("Number of Activations per Year", wrap=True)
    plt.savefig(save_path+"/activations_per_year_transparent.png", transparent=True)
    plt.savefig(save_path+"/activations_per_year.png", transparent=False)
    plt.clf()
