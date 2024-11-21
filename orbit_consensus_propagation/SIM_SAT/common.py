import json
import ssl
import requests
import csv
import numpy as np

from skyfield.api import load, EarthSatellite, utc
from skyfield.iokit import parse_tle_file
from dateutil.relativedelta import relativedelta

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)

def csv_output(file_name, data_send):
    with open(file_name, "w") as f:
        if len(data_send) == 0:
            f.close()
            return
        else:
            for item in data_send:
                csv.writer(f).writerow(item)
            f.close()
            return
        
    
# Gets all icsmd satellites from tle file
def get_satellites(input_tle, refine_by_name=None):
    ts = load.timescale()

    with load.open(input_tle) as f:
        satellites = list(parse_tle_file(f, ts))

    if refine_by_name != None:
        with open(refine_by_name, "r") as f:
            icsmd_sats = f.read().split("\n")

        icsmd_sats = np.array(icsmd_sats)
        satellites_updated = []
        for sat in satellites:
            if sat.name in icsmd_sats:
                satellites_updated.append(sat)

        return satellites_updated
    
    else:
        return satellites


# Gets random selection of satellites from tle file
def get_random_satellites(input_tle, n=100):
    ts = load.timescale()

    with load.open(input_tle) as f:
        satellites = list(parse_tle_file(f, ts))

    # print('Loaded', len(satellites), 'satellites')

    sat_selection = np.array(np.random.sample(100)*len(satellites), dtype=int)
    # print(sat_selection)
    return np.array(satellites)[sat_selection]




# Create a list of dates based on input
def date_range(start_date, end_date, increment, period):
    result = []
    nxt = start_date
    delta = relativedelta(**{period:increment})
    while nxt <= end_date:
        result.append(nxt)
        nxt += delta
    return result