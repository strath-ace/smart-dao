from sentinelhub import DataCollection
import sentinelhub
from shapely import Polygon
from helper import *
import itertools
import tempfile
from pathlib import Path
import geopandas as gpd
import matplotlib.pyplot as plt
import rioxarray  # noqa: F401 # Its necesary for xarray.open_mfdataset() with engine `rasterio`
import xarray as xr  # It may need Dask library https://docs.dask.org/en/stable/install.html
from matplotlib.patches import Polygon as PltPolygon
#from mpl_toolkits.basemap import Basemap  # Available here: https://github.com/matplotlib/basemap
import yaml
import os
import numpy as np
import json
from shapely.geometry import MultiLineString, MultiPolygon, Polygon, box, shape
from skimage.draw import polygon
from sentinelhub import (
    CRS,
    BBox,
    BBoxSplitter,
    CustomGridSplitter,
    DataCollection,
    MimeType,
    MosaickingOrder,
    OsmSplitter,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    TileSplitter,
    UtmGridSplitter,
    UtmZoneSplitter,
    read_data,
    SHConfig,
    bbox_to_dimensions,
)



file_location = os.path.dirname(os.path.abspath(__file__))
with open(file_location+"/params.yml", "r") as f:
    params_config = yaml.load(f, Loader=yaml.SafeLoader)

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def plot_xr_and_bboxes(data_array, save_file, geo_vector=None):
    data_array.plot.imshow(ax=ax, robust=True)
    


# Make maps
boxes = []
for root, dirs, files in os.walk("data", topdown=False):
    for name in files:
        file_path = os.path.join(root, name)
        if file_path[-13:] == "response.tiff":
            boxes.append(Path(file_path))


tiffs = boxes
composed_tiff = xr.open_mfdataset(tiffs, engine="rasterio")
composed_map = composed_tiff.band_data.isel(band=[2,1,0])
fig, ax = plt.subplots(figsize=(10, 10), dpi=500)
plot_xr_and_bboxes(composed_map, "extra/test_.tif")
ax.set_ylabel("Latitude")
ax.set_xlabel("Longitude")
ax.set_aspect(1)

plt.savefig("extra/test_.tif")


    # print("Map", i, "out of", 100, "done")

        # kauai_gpd = gpd.GeoDataFrame(geometry=[box(*bbox) for bbox in bbox_list], crs=4326)
        # plot_xr_and_bboxes(composed_tiff.band_data, kauai_gpd)

