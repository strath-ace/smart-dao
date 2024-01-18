import json
import math
import csv

R_EARTH = 6371

def clean_file_name(dirty):
    dirty = dirty.replace("_", " ")
    dirty = dirty.replace("-", " ")
    dirty = dirty.replace("(", " ")
    dirty = dirty.replace(")", " ")
    dirty = dirty.replace("/", " ")
    dirty = dirty.replace("*", " ")
    dirty = dirty.strip()
    dirty = dirty.replace("  ", "_")
    dirty = dirty.replace(" ", "_")
    dirty = dirty.replace("_", "")
    return dirty


def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)


def compute_pos(lon,lat, elev):
    r = elev/1000 + R_EARTH
    x = r*math.cos(lat)*math.cos(lon)
    y = r*math.cos(lat)*math.sin(lon)
    z = r*math.sin(lat)
    return x,y,z

def csv_output(file_name, data_send):
    with open(file_name, "w") as f:
        for item in data_send:
            csv.writer(f).writerow(item)
        f.close()
        return