# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

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


tweets = load_json("./eq_indonesia_social_media.json")

location_li = []
time_li = []
text_li = []

for i in range(len(tweets)):
    location = tweets[i]["geometry"]["coordinates"]
    time = tweets[i]["properties"]["created_at"]
    try:
        text = tweets[i]["properties"]["text_clean"][:]
    except:
        text = tweets[i]["properties"]["text"][:]
    if text not in text_li:
        location_li.append(location)
        time_li.append(time)
        text_li.append(text)

out = []
for i in range(len(text_li)):
    out_temp = {
        "location": location_li[i],
        "time": time_li[i],
        "text": text_li[i],
    }
    out.append(out_temp)

save_json("./clean_social_media.json", out)