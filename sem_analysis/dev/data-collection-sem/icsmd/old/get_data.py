from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl

from get_url_details import get_url_details

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

with open("activations_list.html") as response:
    soup = BeautifulSoup(response, 'html.parser')

links = []
divs = soup.find_all('div', {"class": "timeline"})
#print(soup)
for div in divs:
    a_ref = soup.find_all('a', href=True)
    for a in a_ref:
        link = str(a['href'])
        try:
            int(link[len(link)-4:len(link)-1])
            links.append(link)
        except:
            continue

output = []
count = 0
count_limit = 10
for link in links:
    # if count > count_limit:
    #     break

    with urlopen(link) as response:
        soup = BeautifulSoup(response, 'html.parser')

    # try:
        sats, producers, info = get_url_details(soup)

        if len(info) == 3 and len(producers) > 0 and len(sats) > 0:

            json_temp = {   'Country': info[0],
                            'Date': info[1],
                            'Activation_ID': info[2],
                            'Satellites': sats,
                            'Map_Producers': producers                       
                        }

            output.append(json_temp)
            # temp = []
            # for item in info:
            #     temp.append(item)
            # temp.append(sats)
            # temp.append(producers)
            
            # output.append(temp)
            count += 1
            print(count)
            # print(temp)


    # except:
    #     continue






# import csv
# def csv_output(file_name, data_send):
#     '''
#     Open a csv and add the sent data
#     '''
#     with open(file_name, "w") as f:
#         for item in data_send:
#             csv.writer(f).writerow(item)
#         f.close()
#         return
        
# csv_output("output.json", output)

import json
with open("output.json",'w') as f:
    json.dump(output, f)