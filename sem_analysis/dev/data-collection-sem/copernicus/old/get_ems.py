from bs4 import BeautifulSoup
from urllib.request import urlopen
import ssl
import requests
import os


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

# Current 654
for i in range(0, 654):
    try:
        num = str(i)
        code = "EMSR"+num.zfill(3)

        url = "https://emergency.copernicus.eu/mapping/list-of-components/"+code


        with urlopen(url) as response:
            soup = BeautifulSoup(response, 'html.parser')
        links = []
        a_ref = soup.find_all('a', href=True)
        for a in a_ref:
            link = str(a['href'])
            if link[-4:] == ".pdf":
                links.append(link)
        
        if len(links) > 2:
            print(code)
            print(len(links))
            count = 0
            os.mkdir(os.path.join(os.path.expanduser('~'), "local-data", "all-copernicus-ems", code))
            for link in links:
                count += 1
                print(count)
                try:
                    response = requests.get(link)

                    
                    path = os.path.join(os.path.expanduser('~'), "local-data", "all-copernicus-ems", code, str(count)+".pdf")

                    if response.status_code == 200:
                        with open(path, "wb") as f:
                            f.write(response.content)
                            f.close()
                    else:
                        print(response.status_code)
                except:
                    continue

    except:
        continue

