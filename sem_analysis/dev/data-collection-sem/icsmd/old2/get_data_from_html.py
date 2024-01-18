# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

from bs4 import BeautifulSoup
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


local_data_file = os.path.join(os.path.expanduser('~'), "local-data")

old_data_path = os.path.join(local_data_file, "all-icsmd-data", "html_data_reduced")
new_data_path = os.path.join(local_data_file, "all-icsmd-data", "all_data.json")




files = os.listdir(old_data_path)

bad_digits = ["\n", "td", "/td", "tr", "/tr", "br/", "", "div", "/div", "a", "/a", "p", "/p", "h1", "/h1", "h2", "/h2", "h3", "/h3", "h4", "/h4", "strong", "/strong"]

swap_digits = ["<", ">"]


search_parameters = [
                    "TypeofEvent:",
                    "LocationofEvent:",
                    "DateofCharterActivation:",
                    "TimeofCharterActivation:",
                    "CharterRequestor:",
                    "ActivationID:",
                    "ProjectManagement:",
                    "Source:",
                    "Acquired:"
                    ]

active_files = []
files_without_html = []
for file in files:
    if "activation" in file:
        active_files.append(file)
        files_without_html.append(file[:-5])

main_json = {"all_activations": files_without_html}

def divide_by_digits(data, chari):
    temp = []
    output = []
    for i in range(len(data)):
        if data[i] in chari:
            output.append("".join(temp))
            temp = []
        else:
            temp.append(data[i])
        if i == len(data)-1:
            output.append("".join(temp))
    return output

def date_to_timestamp(date, date_format):
    try:
        return time.mktime(datetime.datetime.strptime(date, date_format).timetuple())
    except:
        return 0


for file in active_files:

    old_path = os.path.join(old_data_path, file)

    with open(old_path) as response:
        soup = BeautifulSoup(response, 'html.parser')

    data = str(soup)

    
    
    output = divide_by_digits(data, swap_digits)
    

    main_output = []
    for data in output:
        count = True
        if "class=" in data:
            count = False
        if data not in bad_digits and count:
            main_output.append(data)

    for i in range(len(main_output)):
        main_output[i] = main_output[i].replace("\t", "")
        main_output[i] = main_output[i].replace("\n", "")
        main_output[i] = main_output[i].replace("br&gt", "/")
        main_output[i] = main_output[i].replace(" ", "")
        main_output[i] = main_output[i].replace("and", "&")
        
        

    search_output = {}
    for search in search_parameters:
        temp = []
        for i in range(len(main_output)):
            if search == main_output[i]:
                try:
                    temp.append(main_output[i+1])
                except:
                    continue


        # Split source by digits
        temp_new = []
        if search == "Source:":
            division_digits = ["/", ";", ",", "&"]
            for val in temp:
                #out = [val]
                out = divide_by_digits(val, division_digits)
                for x in out:
                    x_send = x.replace("-", "")
                    temp_new.append(x_send)
        elif search == "ProjectManagement:":
            division_digits = ["/", ";", ",", "&"]
            for val in temp:
                out = divide_by_digits(val, division_digits)
                for x in out:
                    temp_new.append(x)
        elif search == "Acquired:":
            division_digits = [";", ",", "&", ":"]
            for val in temp:
                #out = [val]
                out = divide_by_digits(val, division_digits)
                for x in out:
                    timestamp = date_to_timestamp(x, "%d/%m/%Y")
                    if timestamp > 0:
                        temp_new.append(timestamp)
        elif search == "DateofCharterActivation:":
            temp_new.append(date_to_timestamp(temp[0], "%Y-%m-%d"))
        else:
            temp_new = temp


        
        
        # Remove duplicates
        temp = []
        for val in temp_new:
            try:
                use = val.lower()
            except:
                use = val
            if use not in temp:
                temp.append(use)

        update_json = {search: temp}
        search_output.update(update_json)
   
    
    main_json.update({file[:-5]: search_output})



save_json(new_data_path, main_json)
save_json("all_data.json", main_json)
