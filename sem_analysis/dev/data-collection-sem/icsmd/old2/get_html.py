from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import requests
import os



# This creates ssl file
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context



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


with open("activations_list.html") as response:
    soup = BeautifulSoup(response, 'html.parser')

links_disaster = []
divs = soup.find_all('div', {"class": "timeline"})
for div in divs:
    a_ref = soup.find_all('a', href=True)
    for a in a_ref:
        link = str(a['href'])
        if check_int(link[-4:-1]):
            links_disaster.append(link)


# For each disaster
counter = 0
for link_disaster in links_disaster:
    counter += 1
    print(100*counter/len(links_disaster), "%")

    code = link_disaster[-4:] + link_disaster[61:-5]

    try:
        response = requests.get(link_disaster)

        path = os.path.join(os.path.expanduser('~'), "local-data", "all-icsmd-data", "html_data", code+".html")

        if response.status_code == 200:
            with open(path, "wb") as f:
                f.write(response.content)
                f.close()
        else:
            print(response.status_code)
    except:
        continue