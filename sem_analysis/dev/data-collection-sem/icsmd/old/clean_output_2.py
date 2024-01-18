# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import json
import statistics
import time
import datetime

MAX_TIME = 99999999999999999

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

def to_timestamp(date):
    """
    Convert date from input format to timestamp
    """
    try:
        return time.mktime(datetime.datetime.strptime(date, "%d%m%Y%H%M").timetuple())
    except:
        try:
            return time.mktime(datetime.datetime.strptime(date, "%d%m%Y").timetuple())
        except:
            return 0
    

old_data = load_json("output.json")
map_sat_agency = load_json("map_sat_agency.json")
map_agency_country = load_json("map_agency_country.json")


code_list = []
for i in range(654):
    temp = []
    for pdf in old_data:
        if int(pdf['active_id']) == i:
            temp.append(pdf)
    code_list.append(temp)


clean_data = []
counter = -1
for code in code_list:
    counter += 1

    # If empty
    if len(code) == 0:
        clean_data.append({
        'active_id': counter,
        'exists': 0
        })
        continue

    # Single data point
    title = code[0]['title']

    # Multiple data points
    pdf_names = []
    country_rep = []
    date_event_li = []
    date_situation_li = []
    date_active_li = []
    date_map_li = []
    sat_post = []
    agency_rep = []
    country_rep2 = []
    for pdf in code:
        # Pdf Names
        pdf_names.append(pdf['json_name'])
        # Countrys
        for i in range( len(pdf['title'])-1 , 0 , -1 ):
            if pdf['title'][i] == '-' or i == 0:
                country_rep.append(pdf['title'][i+1:])
                break
        
        # Dates
        colon_count = 0
        long_date = []
        for x in pdf['dates_1']:
            if check_int(x):
                long_date.append(x)
            if x == ":":
                colon_count += 1
        if colon_count == 2:
            date_event = to_timestamp("".join(long_date[0:12]))
            date_situation = to_timestamp("".join(long_date[12:]))
        else:
            date_event = to_timestamp("".join(long_date[0:12]))
            date_situation = to_timestamp("".join(long_date[12:20]))
        colon_count = 0
        long_date = []
        for x in pdf['dates_2']:
            if check_int(x):
                long_date.append(x)
            if x == ":":
                colon_count += 1
        if colon_count == 2:
            date_active = to_timestamp("".join(long_date[0:12]))
            date_map = to_timestamp("".join(long_date[12:]))
        else:
            date_active = to_timestamp("".join(long_date[0:12]))
            date_map = to_timestamp("".join(long_date[12:20]))

        date_event_li.append(date_event)
        date_situation_li.append(date_situation)
        date_active_li.append(date_active)
        date_map_li.append(date_map)

        for x in pdf['post_event']:
            sat_post.append(x)

    # Get first activation time after event occurs 
    min_act = MAX_TIME
    point = -1
    for i in range(len(date_active_li)):
        situ = date_active_li[i]
        if situ > date_event and situ < min_act:
            min_act = situ
            point = i
    if min_act == MAX_TIME:
        continue
    dates_active = {
        'pdf_id': pdf_names[point],
        'date_event': date_event_li[point],
        'date_active': date_active_li[point],
        'date_situation': date_situation_li[point],
        'date_map': date_map_li[point]
        }


    # Get first situation time after event occurs 
    date_event = statistics.mode(date_event_li)
    min_situ = MAX_TIME
    point = -1
    for i in range(len(date_situation_li)):
        situ = date_situation_li[i]
        if situ > date_event and situ < min_situ:
            min_situ = situ
            point = i
    if min_situ == MAX_TIME:
        continue
    dates_situ = {
        'pdf_id': pdf_names[point],
        'date_event': date_event_li[point],
        'date_active': date_active_li[point],
        'date_situation': date_situation_li[point],
        'date_map': date_map_li[point]
        }
    
    # Get first map time after event occurs 
    min_map = MAX_TIME
    point = -1
    for i in range(len(date_map_li)):
        situ = date_map_li[i]
        if situ > date_event and situ < min_map:
            min_map = situ
            point = i
    if min_map == MAX_TIME:
        continue
    dates_map = {
        'pdf_id': pdf_names[point],
        'date_event': date_event_li[point],
        'date_active': date_active_li[point],
        'date_situation': date_situation_li[point],
        'date_map': date_map_li[point]
        }
    
    

    for sat in sat_post:
        try:
            if map_sat_agency[sat]['real']:
                agency_rep.append(map_sat_agency[sat]['agency'])
        except:
            print("No mapping for this sat")
            continue

    for agency in agency_rep:
        try:
            if map_agency_country[agency]['real']:
                country_rep2.append(map_agency_country[agency]['country'])
        except:
            print("No mapping for this agency")
            continue


    # Remove repititions in country
    country = []
    for rep in country_rep:
        res = rep.replace('\u0000', '')
        if res.lower() not in country:
            country.append(res.lower())
    # Remove repitions in agency
    agency_post = []
    for rep in agency_rep:
        res = rep.replace('\u0000', '')
        if res.lower() not in agency_post:
            agency_post.append(res.lower())
    # Remove repitions in agency
    country_post = []
    for rep in country_rep2:
        res = rep.replace('\u0000', '')
        if res.lower() not in country_post:
            country_post.append(res.lower())

    

        

    clean_data.append({
        'active_id': counter,
        'exists': 1,
        #'pdf_names': pdf_names,
        'country_effected': country,
        'date_first_active': dates_active,
        'date_first_situation': dates_situ,
        'date_first_map': dates_map,
        'post_event_sat': sat_post,
        'post_event_agency': agency_post,
        'post_event_country': country_post
        })

save_json('clean_output.json', clean_data)