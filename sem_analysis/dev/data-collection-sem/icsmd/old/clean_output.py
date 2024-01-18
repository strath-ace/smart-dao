# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import json
import csv

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output


def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)

def load_csv(file_name):
    '''
    Open a csv file and return an array
    '''
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

def save_csv(file_name, data_send):
    '''
    Open a csv and add the sent data
    '''
    with open(file_name, "w") as f:
        for item in data_send:
            csv.writer(f).writerow(item)
        f.close()
        return
    


old_output = load_json("output.json")
map_sat_to_agency = load_json("map_sat_to_agency.json")
map_agency_to_country = load_json("map_agency_to_country.json")
hdi_ratings = load_csv("hdi.csv")
new_output = []
new_output_csv = []

for activity in old_output:
    sats = activity["Satellites"]
    countries = []
    
    for sat in sats:
        for mapping in map_sat_to_agency:
            if mapping["sat_input"] == sat:
                if mapping["real"]:
                    agency = mapping["country"]
                    prob = 1
                else:
                    prob = 0
        if prob:
            for mapping in map_agency_to_country:
                if mapping["agency_input"] == agency:
                    if mapping["real"]:
                        countries.append(mapping["country"])
    countries_out = []
    for cou in countries:
        val = True
        for cou_o in countries_out:
            if cou == cou_o:
                val = False
                break
        if val:
            countries_out.append(cou)

    
    prod_rating = []
    for country in countries_out:
        for item in hdi_ratings:
            if country == item[0].lower():
                rating = item[1]
                break
        prod_rating.append(float(rating))
    tot = 0
    if len(prod_rating) == len(countries_out) and len(prod_rating) > 0:
        for x in prod_rating:
            tot += x
        prod_avg = tot/len(prod_rating)
    user_rating = 0
    for item in hdi_ratings:
        if activity["Country"].lower() == item[0].lower():
            user_rating = float(item[1])
            break
        

    good = 0
    if tot > 0 and user_rating > 0:
        good = 1
    

    if len(countries_out) > 0 and good:
        temp_json = {"activation_id": activity["Activation_ID"],
                    "date": activity["Date"],
                    "producer_country": countries_out,
                    "producer_hdi": prod_avg,
                    "user_country": activity["Country"].lower(),
                    "user_hdi": user_rating}
        temp_csv = [activity["Activation_ID"],
                    activity["Date"],
                    countries_out,
                    prod_avg,
                    activity["Country"].lower(),
                    user_rating]
        new_output.append(temp_json)
        new_output_csv.append(temp_csv)

save_csv("clean_output.csv", new_output_csv)
save_json("clean_output.json", new_output)