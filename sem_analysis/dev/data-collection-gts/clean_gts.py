from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import requests
import os
import json
import time

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def save_json(file_name, data):
    """
    Save json data to file
    """
    with open(file_name,'w') as f:
        json.dump(data, f)

json_data = load_json("local-data-path.json")
save_path = json_data["path"]

open_file_name = "/gts_events_tc.json"
clean_file_name = "/gts_tc_clean.json"


raw_file = load_json(save_path+open_file_name)
clean_file = []

for i in range(len(raw_file)):
    current_text = raw_file[i]["text"]
    current_text = current_text.replace("\t", "")
    current_text = current_text.replace("\r\n", "£")
    j_0 = 0
    out_text = []
    for j in range(len(current_text)):
        if current_text[j] == "£":
            if current_text[j_0:j] not in [""]:
                out_text.append(current_text[j_0:j])
            j_0 = j+1
    clean_file.append({
        "gdacs_id": raw_file[i]["gdacs_id"],
        "text": out_text
        })
    
save_json(save_path+clean_file_name, clean_file)
