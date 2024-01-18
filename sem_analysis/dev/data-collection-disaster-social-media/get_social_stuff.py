from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import requests
import os
import json

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

save_file_name = "/eq_indonesia_social_media.txt"


# This creates ssl file
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

link = "https://www.gdacs.org/contentdata/resources/EQ/1347183/social.json"

response = requests.get(link)

with open(save_path+save_file_name, "w") as f:
    f.write(response.text)

