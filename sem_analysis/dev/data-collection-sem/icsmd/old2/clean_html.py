# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------s

from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import requests
import os


local_data_file = os.path.join(os.path.expanduser('~'), "local-data")

old_data_path = os.path.join(local_data_file, "all-icsmd-data", "html_data")
new_data_path = os.path.join(local_data_file, "all-icsmd-data", "html_data_reduced")


files = os.listdir(old_data_path)


for file in files:
    old_path = os.path.join(old_data_path, file)
    new_path = os.path.join(new_data_path, file)

    with open(old_path) as response:
        soup = BeautifulSoup(response, 'html.parser')

    div = soup.find('div', {"class": "container-fluid page-con act-page"})

    with open(new_path, "w") as f:
        f.write(str(div))
        f.close()



