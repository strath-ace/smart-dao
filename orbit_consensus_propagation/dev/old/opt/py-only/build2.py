import os
import generic as g
import numpy as np
from datetime import datetime, timedelta
import ephem
import math
from pytictoc import TicToc


ALL_SATS_FILE = ["..", "active.txt"]
USED_SATS_FILE = ["sats_to_use.txt"]
SAVE_DIR = ["..", "data"]

START_TIME = 1701448313
TIMESTEP = 60
MAX_TIME = 24*60*TIMESTEP  # Max search time for each task before failure (in seconds)

MAX_DISTANCE = 500

LAG_TIME = 30*60

BAD_FITNESS = MAX_TIME*4*8*2
BAD_FITNESS_MULTI = 10

R_earth = 6371

# def build(self, bin_sats, i):
def build(int_sats):
    t = TicToc()
    t.tic()
    primary=0
    fit = BAD_FITNESS
    int_sats = np.array(int_sats)
    for i in range(len(int_sats)):
        if i > 81:
            return BAD_FITNESS
        for i1 in range(len(int_sats)):
            if i != i1:
                if int_sats[i] == int_sats[i1]:
                    return BAD_FITNESS
    sats_all = np.array(g.load_json("sorted_sats.json"))
    # Reduce to only those in bin_sats
    sats_tle = []
    for i in int_sats:
        sats_tle.append(sats_all[int(i)])
    sats_tle = np.array(sats_tle)
    # Propagate sats_tle
    all_comp = []
    for sat in sats_tle:
        all_comp.append(ephem.readtle(sat["name"], sat["line1"], sat["line2"]))
    
    # FOR WHO IS PRIMARY

    minus_comp = all_comp.copy()
    minus_comp.pop(primary)

    t_local = np.full(len(all_comp), START_TIME)

    # Pre-Prepare
    # Communicate from primary to all
    for i, sat1 in enumerate([all_comp[primary]]):
        for j, sat2 in enumerate(all_comp):
            if sat1 != sat2:
                conn_time = find_next_conn(t_local[j], MAX_TIME, sat1, sat2)
                if conn_time == -1:
                    return fit
                t_local[j] = conn_time

    # Decision Lag
    t_local = t_local + LAG_TIME

    # Prepare
    # Communicate from all to all
    for j, sat2 in enumerate(all_comp):
        max_time = 0
        for i, sat1 in enumerate(minus_comp):
            if sat1 != sat2:
                conn_time = find_next_conn(t_local[i], MAX_TIME, sat1, sat2)
                if conn_time == -1:
                    return fit*0.75
                if max_time < conn_time:
                    max_time = conn_time
        t_local[j] = max_time

    # Commit
    # Communicate from all to all
    for j, sat2 in enumerate(all_comp):
        max_time = 0
        for i, sat1 in enumerate(all_comp):
            if sat1 != sat2:
                conn_time = find_next_conn(t_local[i], MAX_TIME, sat1, sat2)
                if conn_time == -1:
                    return fit*0.5
                if max_time < conn_time:
                    max_time = conn_time
        t_local[j] = max_time

    # Reply
    # Communicate from all to all
    for j, sat2 in enumerate([all_comp[primary]]):
        max_time = 0
        for i, sat1 in enumerate(all_comp):
            if sat1 != sat2:
                conn_time = find_next_conn(t_local[i], MAX_TIME, sat1, sat2)
                if conn_time == -1:
                    return fit*0.25
                if max_time < conn_time:
                    max_time = conn_time
        t_local[j] = max_time
        
    # print("Success")
    t.toc()
    return np.amax(t_local)-START_TIME


def find_next_conn(t_0, t_max, sat1, sat2):
    for i in range(t_0, t_0+t_max, TIMESTEP):
        timestep = datetime.fromtimestamp(i)
        sat1.compute(timestep)
        sat2.compute(timestep)
        if MAX_DISTANCE >= normalise(compute_pos(sat1.sublong, sat1.sublat, sat1.elevation), compute_pos(sat2.sublong, sat2.sublat, sat2.elevation)):
            return i
    return -1


def compute_pos(lon,lat, elev):
    r = elev/1000 + R_earth
    x = r*math.cos(lat)*math.cos(lon)
    y = r*math.cos(lat)*math.sin(lon)
    z = r*math.sin(lat)
    return x,y,z


def normalise(pos1, pos2):
    pos_n = np.array(pos1) - np.array(pos2)
    return math.sqrt(np.sum(np.square(pos_n)))

    

    
