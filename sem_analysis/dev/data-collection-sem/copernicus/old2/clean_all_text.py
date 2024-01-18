# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import os
import json
import time
import datetime


def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)

def check_int(input):
    """
    Check if input string is a integer
    """
    try:
        int(input)
        is_int = 1
    except:
        is_int = 0
    return is_int


def string_to_list(text):
    """
    Converts string to list
    """
    text_out = []
    text_temp = []
    for i in range(len(text)):
        if text[i] == '-':
            text_out.append("".join(text_temp).replace(" ", ""))
            text_temp = []
        else:
            text_temp.append(text[i])
        if i == len(text):
            text_out.append("".join(text_temp).replace(" ", ""))
    text_return = []
    for x in text_out:
        if x not in [""]:
            text_return.append(x)
    return text_return


def date_to_timestamp(date, date_format):
    return time.mktime(datetime.datetime.strptime(date, date_format).timetuple())



local_data_file = os.path.join(os.path.expanduser('~'), "local-data")

old_data_path = os.path.join(local_data_file, "copernicus-data", "all_text.json")
new_data_path = os.path.join(local_data_file, "copernicus-data", "clean_data.json")

all_text = load_json(old_data_path)

all_events = all_text['all_files']

main_json = {}

for event in all_events:
    text = all_text[event]
    text_li = string_to_list(text)
    del text

    active_id = event[4:7]


    location = ""
    map_maker = ""
    dates_1 = ""
    dates_2 = ""
    post_event = ""

    # Search for specific info
    pre_event = []
    post_event = []
    for text in text_li:
        if text[:2] == "km" and not check_int(text[-3:]) and text[-3:] != "N/A":  #  Check for title
            location = text[2:]
        elif text[0:13] == "Mapproducedby":
            map_maker = text[13:]
        elif text[0:18] == "EventSituationasof":
            dates_1 = text[18:]
        elif text[0:23] == "ActivationMapproduction":
            dates_2 = text[23:]
        elif text[0:16] == "Post/eventimage:":
            for i in range(len(text)):
                if text[i] == "(":
                    post_event.append(text[16:i].lower().replace("/", ""))
                    break
                if i == len(text):
                    post_event.append(text[16:].lower().replace("/", ""))
    

    times = []
    for dates in [dates_1, dates_2]:
        dates = dates.replace(".", "/")
        try:
            times.append(date_to_timestamp(dates[:15], "%d/%m/%Y%H:%M"))
            start = 15
        except:
            try:
                times.append(date_to_timestamp(dates[:10], "%d/%m/%Y"))
                start = 10
            except:
                times.append(0)
                start = 0
        try:
            times.append(date_to_timestamp(dates[start:start+15], "%d/%m/%Y%H:%M"))
        except:
            try:
                times.append(date_to_timestamp(dates[start:start+10], "%d/%m/%Y"))
            except:
                times.append(0)

    try:
        main_json[active_id]["map_maker"].append(map_maker)
        main_json[active_id]["event_date"].append(times[0])
        main_json[active_id]["activation_date"].append(times[1])
        main_json[active_id]["sat_data_date"].append(times[2])
        main_json[active_id]["publish_date"].append(times[3])
        for x in post_event:
            main_json[active_id]["Source:"].append(x)
    except:
        # Make json output
        event_data = {
            "location": location,
            "map_maker": [map_maker],
            'event_date': [times[0]],
            'activation_date': [times[1]],
            'sat_data_date': [times[2]],
            'publish_date': [times[3]],
            "Source:": post_event
        }
        
        main_json.update({active_id: event_data})

all_activations = []
for i in range(len(all_events)):
    try:
        main_json[str(i).zfill(3)]
        all_activations.append(str(i).zfill(3))
    except:
        continue



temp_all_activations = []
slots = ['map_maker', 'event_date', "activation_date", "sat_data_date", "publish_date", "Source:"]
slots_kill = ['event_date', "activation_date", "sat_data_date", "publish_date"]
for code in all_activations:
    for v in slots:
        temp = []
        for x in main_json[code][v]:
            if x not in temp:
                temp.append(x)
        main_json[code][v] = temp
    count = 0
    for v in slots_kill:
        if main_json[code][v][0] in [0, "", []]:
            count += 1
    if count == len(slots_kill):
        main_json.pop(code)
    else:
        temp_all_activations.append(code)

all_activations = temp_all_activations

main_json.update({'all_activations': all_activations})

save_json(new_data_path, main_json)
save_json("clean_data.json", main_json)

