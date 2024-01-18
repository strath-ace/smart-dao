from bs4 import BeautifulSoup

def get_url_details(soup):
    sats = []
    producer = []

    mydivs = soup.find_all("table")
    #print(mydivs[0])
    div = str(mydivs[0])

    queries = ["Location of Event:", "Date of Charter Activation:", "Activation ID:"]
    info = []
    for query in queries:
        start = -1
        end = -1
        for i in range(len(div)):
            # Gets Type of Event
            # print(div[i:i+len(query)])
            # print(query)
            if div[i:i+len(query)] == query:
                #print(query)
                start = i+len(query)+9
            if start != -1:
                if div[i:i+3] == "/tr":
                    end = i-6
            if start != -1 and end != -1:      
                info.append(div[start:end])
                start = -1
                end = -1


    mydivs = soup.find_all("div", {"class": "media-activations"})
    try:
        mydivs = mydivs[0]
    except:
        mydivs = mydivs
    for div in mydivs:
        div = str(div)
        start = -1
        end = -1
        start_2 = -1
        end_2 = -1
        for i in range(len(div)):
            # Gets sats
            if div[i:i+7] == "Source:":
                start = i+17
            if start != -1:
                if div[i:i+3] == "div" or div[i:i+3] == "br>":
                    end = i-2
            if start != -1 and end != -1:     
                sats.append(div[start:end])
                start = -1
                end = -1
            # Gets map makers
            if div[i:i+16] == "Map produced by ":
                start_2 = i+16
            if start_2 != -1:
                if div[i:i+3] == "div" or div[i:i+3] == "br>":
                    end_2 = i-2
            if start_2 != -1 and end_2 != -1:
                producer.append(div[start_2:end_2])
                start_2 = -1
                end_2 = -1

    # Splits long string based on /
    sats_2 = []
    for sat in sats:
        start = 0
        end = -1
        for i in range(len(sat)):
            if sat[i] in ["/", ",", "-"]:
                end = i
                sats_2.append(sat[start:end].strip().lower())
                start = i+1
            if sat[i:i+3] == "and":
                end = i
                sats_2.append(sat[start:end].strip().lower())
                start = i+3
        # if start == 0 and end == -1:
        #     sats_2.append(sat.strip().lower())
        sats_2.append(sat[start:len(sat)].strip().lower())

    # Remove repitions from array
    sats_out = []
    for sat in sats_2:
        val = True
        for sat_o in sats_out:
            if sat == sat_o:
                val = False
                break
        if val:
            sats_out.append(sat)

    # Splits long string based on /
    producers_2 = []
    for prod in producer:
        start = 0
        end = -1
        for i in range(len(prod)):
            if prod[i] in ["/", ",", "-"]:
                end = i
                producers_2.append(prod[start:end].strip().lower())
                start = i+1
            if prod[i:i+3] == "and":
                end = i
                producers_2.append(prod[start:end].strip().lower())
                start = i+3
        producers_2.append(prod[start:len(prod)].strip().lower())

    # Remove repitions from array
    producer_out = []
    for prod in producers_2:
        val = True
        for prod_o in producer_out:
            if prod == prod_o:
                val = False
                break
        if val:
            producer_out.append(prod)

    for i in range(len(producer_out)):
        prod_t = [x for x in producer_out[i]]
        if len(prod_t) >= 1:
            while prod_t[-1] in ["<", ".", ">", " "]:
                prod_t.pop()
                if len(prod_t) <= 1:
                    break
        producer_out[i] = "".join(prod_t)


    return(sats_out, producer_out, info)