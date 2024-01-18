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

# Avalaible lists
# list_gts_eq.html
# list_gts_tc.html

open_file_name = "/list_gts_eq.html"
save_file_name = "/gts_events_eq.json"

# This creates ssl file
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

with open(save_path+open_file_name) as response:
    soup = BeautifulSoup(response, "html.parser")

try:
    gts_list = load_json(save_path+save_file_name)
except:
    gts_list = []


links = soup.find_all('a', href=True)
print("--------")
print()
print(len(links), "GTS messages to download")
print()
print("--------")
time.sleep(0.5)
for i in range(len(gts_list)+1, len(links)):
    link = str(links[i]['href'])
    txt_link_a = []
    while len(txt_link_a) == 0:
        r = requests.get(link).text
        dir_2 = BeautifulSoup(r, "html.parser")
        txt_link_a = dir_2.find_all('a', href=True)
        if len(txt_link_a) == 0:
            print("Too many requests - Waiting")
            time.sleep(2)
    try:
        for ii in range(1, len(txt_link_a)):
            txt_link = txt_link_a[ii]['href']
            txt = requests.get("https://www.gdacs.org"+txt_link).text
            gts_list.append({
                "gdacs_id": txt_link[20:],
                "text": txt
            })
        print(100*i/len(links),"% done")
    except:
        print("FAIL")
        print(100*i/len(links),"% done")
        pass
    if i%100 == 0 and i > 0:
        print("Saving progress")
        save_json(save_path+save_file_name, gts_list)

save_json(save_path+save_file_name, gts_list)
print("Done")
