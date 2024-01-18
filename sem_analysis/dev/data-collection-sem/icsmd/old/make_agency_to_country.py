import csv
import json

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output


def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)
    

try:
    all_sats = load_json("map_agency_to_country.json")
except:
    all_sats = []

all_data = load_json("map_sat_to_agency.json")

sats_in = []
for event in all_data:
    if event["real"]:
        sats_in.append(event["country"])
            
sats = []
for sat in sats_in:
    start = 0
    end = -1
    for i in range(len(sat)):
        if sat[i] in ["/", ",", "-"]:
            end = i
            sats.append(sat[start:end].strip().lower())
            start = i+1
        if sat[i:i+3] == "and":
            end = i
            sats.append(sat[start:end].strip().lower())
            start = i+3
    sats.append(sat[start:len(sat)].strip().lower())

sats_uniq = []
for sat in sats:
    val = True
    for sat_o in sats_uniq:
        if sat == sat_o:
            val = False
            break
    if val:
        sats_uniq.append(sat)

sat_list = []
for sat in all_sats:
    sat_list.append(sat["agency_input"])
for sat in sats_uniq:
    if sat in sat_list:
        continue
    else:
        print("")
        print("--------")
        print(len(sats_uniq)-len(sat_list))
        print("")
        print(sat)
        inp = input("Operator or 0 bad or 1 to quit: ")
        try:
            if int(inp) == 0:
                data = {"agency_input": sat, "real": 0, "country": "na"}
                all_sats.append(data)
            if int(inp) == 1:
                break
        except:
            data = {"agency_input": sat, "real": 1, "country": str(inp)}
            all_sats.append(data)

save_json("map_agency_to_country.json", all_sats)
