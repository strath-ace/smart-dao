import ssl
import requests
from bs4 import BeautifulSoup
import json
import os

def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

json_data = load_json("../local-data-path.json")
save_path = json_data["path"]+"/icsmd-data"

# Input location - html
path_in_file = save_path+"/activations_list.html"
file_type_in = ".html"

# Output location - lots of html
path_out_dir = save_path+"/raw_data"
file_type_out = ".html"



try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
    


with open(path_in_file) as response:
	soup = BeautifulSoup(response, "html.parser")
        
links = soup.find_all('a', href=True)

good_link = []
for i in range(len(links)):
    link = str(links[i]['href'])
    if "https://disasterscharter.org/web/guest/activations" in link:
        good_link.append(link)
    
existing_files = []
for root, dirs, files in os.walk(path_out_dir):
    for file in files:
        if file[-4:] == file_type_out:
            existing_files.append(file)

for i in range(len(good_link)):
    if good_link[i] not in existing_files:
        response = requests.get(good_link[i])
        if response.status_code == 200:
            with open(path_out_dir+"/"+good_link[i][61:]+file_type_out, "wb") as f:
                f.write(response.content)
                f.close()

existing_files = []
for root, dirs, files in os.walk(path_out_dir):
    for file in files:
        if file[-4:] == file_type_out:
            existing_files.append(file)

if len(good_link) == len(existing_files):
    print("Completed Successfully with all files")
else:
    print("Missing some files")