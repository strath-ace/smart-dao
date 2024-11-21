import numpy as np

import ctypes

from sgp4.api import Satrec, WGS72
from skyfield.api import load, EarthSatellite

# Function to evaluate the fitness of satellite communication by counting successful connections
def fitness(sim_sat, satellites, possible, real_sat_grid, depth, time, num_participants):
    # print(np.shape(time))
    # Ticcer = TicToc()
    # Ticcer.tic()
    library = ctypes.cdll.LoadLibrary("./go_fit.so")
    conn1 = library.consensus_completeness_per
    conn1.restype = ctypes.POINTER(ctypes.c_int)

    conn1.argtypes = [
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_int64,
        ctypes.POINTER(ctypes.c_double),
        ctypes.c_int64,
        ctypes.c_int64,
        ctypes.c_int64,
        ctypes.POINTER(ctypes.c_int)
    ]
    # print("Load Library")
    # Ticcer.toc()
    ts = load.timescale()
    time = ts.from_datetimes(time)
    # Ticcer.tic()
    for i in range(1,len(satellites)+1):
        x = np.where((sim_sat.at(time) - satellites[i-1].at(time)).distance().km <= 500)[0]
        real_sat_grid[i*depth:(i*depth)+len(x)] = x
        real_sat_grid[(i*(len(satellites)+1))*depth:((i*(len(satellites)+1))*depth)+len(x)] = x
    # print("Get sim sat pos")
    # Ticcer.toc()
    
    # Ticcer.tic()
    sizer = len(real_sat_grid)
    grid_raw = real_sat_grid.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    # print("To ctype conversion")
    # Ticcer.toc()

    num_sats = int(len(satellites))+1

    output_size = ctypes.c_int()

    # Ticcer.tic()
    c = conn1(possible, len(possible), grid_raw, sizer, num_sats, num_participants, ctypes.byref(output_size))

    return [c[i] for i in range(output_size.value)]


def make_satellite(X, epoch, ts):
    argp_i = X["argp_i"]
    ecc_i = X["ecc_i"]
    inc_i = X["inc_i"]
    raan_i = X["raan_i"]
    anom_i = X["anom_i"]
    mot_i = X["mot_i"]
    satellite2 = Satrec()
    satellite2.sgp4init(
        WGS72,                      # gravity model
        'i',                        # 'a' = old AFSPC mode, 'i' = improved mode
        25544,                      # satnum: Satellite number
        epoch.days,                 # epoch: days since 1949 December 31 00:00 UT
        3.8792e-05,                 # bstar: drag coefficient (1/earth radii)
        0.0,                        # ndot: ballistic coefficient (radians/minute^2)
        0.0,                        # nddot: mean motion 2nd derivative (radians/minute^3)
        ecc_i,                      # ecco: eccentricity
        np.deg2rad(argp_i),         # argpo: argument of perigee (radians)
        np.deg2rad(inc_i),          # inclo: inclination (radians)
        np.deg2rad(anom_i),         # mo: mean anomaly (radians)
        np.deg2rad(mot_i)/(24*60),  # no_kozai: mean motion (radians/minute)
        np.deg2rad(raan_i),         # nodeo: R.A. of ascending node (radians)
    )
    return EarthSatellite.from_satrec(satellite2, ts)


def flatten_plus_one(real_sat_grid, time):
    big_grid = np.zeros((len(real_sat_grid)+1, len(real_sat_grid)+1, len(time)))
    big_grid[big_grid == 0] = -1
    big_grid[1:,1:] = real_sat_grid

    flat_grid = []
    for i in range(np.shape(big_grid)[0]):
        for j in range(np.shape(big_grid)[1]):
            flat_grid.extend(big_grid[i,j])

    return flat_grid


def flattener(real_sat_grid):
        flat_grid = []
        for i in range(np.shape(real_sat_grid)[0]):
            for j in range(np.shape(real_sat_grid)[1]):
                flat_grid.extend(real_sat_grid[i,j])
        return flat_grid