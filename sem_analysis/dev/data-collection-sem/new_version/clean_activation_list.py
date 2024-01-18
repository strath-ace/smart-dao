# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import json
import os
import requests
from bs4 import BeautifulSoup
import webbrowser

def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output



with open("./activation_list_mess.html") as f:
    soup = BeautifulSoup(f, 'html.parser')

a_links = soup.find_all('a', href=True)

links = []
for i in range(len(a_links)):
    link = str(a_links[i]['href'])
    if "web/guest/activations" in link:
        links.append("https://disasterscharter.org"+link)

try:
    json_out = load_json("./event_and_activation.json")
except:
    json_out = []

urls = []
for i in range(len(json_out)):
    urls.append(json_out[i]["URL"])

temp = []
for link in links:
    if link not in urls:
        temp.append(link)
links = temp


for i in range(len(links)):
        response = requests.get(links[i])
        if response.status_code == 200:
            print()
            print("---")
            webbrowser.open_new_tab(links[i])
            print("12:34 56-78-90")
            date_event = input("Event Date-----: ")
            date_activ = input("Activation Date: ")
            json_out.append(
                {
                    "URL": links[i],
                    "date_event": date_event,
                    "date_active": date_activ
                }
            )
        save_json("./event_and_activation.json", json_out)