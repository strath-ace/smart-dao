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

config = SHConfig()

config.sh_client_id = params_config["CLIENT_ID"]
config.sh_client_secret = params_config["CLIENT_SECRET"]

if config.instance_id == "":
    print("Warning! To use WFS functionality, please configure the `instance_id`.")



# INPUT_FILE = file_location+"/perm_data/hawaii.json"

# geo_json = read_data(INPUT_FILE)
# hawaii_area = shape(geo_json["features"][0]["geometry"])


# INPUT_FILE = file_location+"/perm_data/belgium_cut.json"
INPUT_FILE = file_location+"/perm_data/belgium_crop_type.json"

geo_json = read_data(INPUT_FILE)["features"]




time_interval = ("2018-06-29", "2018-07-01")
# time_interval = ("2020-10-01", "2022-10-13")


all_colour_bands = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04", "B05", "B06", "B07", "B08", "B11", "B12"]
            }],
            output: {
                bands: 9
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B02, sample.B03, sample.B04, sample.B05, sample.B06, sample.B07, sample.B08, sample.B11, sample.B12];
    }
    """

def plot_xr_and_bboxes(data_array, save_file, geo_vector=None):
    fig, ax = plt.subplots(figsize=(10, 10))
    data_array.plot.imshow(ax=ax, robust=True)
    ax.set_ylabel("Latitude")
    ax.set_xlabel("Longitude")
    ax.set_aspect(1)
    if geo_vector is not None:
        geo_vector.plot(ax=ax, edgecolor="red", facecolor="none")
    plt.savefig(save_file)

for i in range(len(geo_json)):
    hawaii_area = shape(geo_json[i]["geometry"])

    # normal_bbox = BBox((2.307129, 51.590723, 6.394043, 49.518076), crs=CRS.WGS84)
    split_bbox = OsmSplitter([hawaii_area], zoom_level=14, crs=CRS.WGS84)    # zoom level 14 for full precision
    # print(normal_bbox)
    # print(split_bbox.get_info_list())

    geometry_list = split_bbox.get_bbox_list()
    # print(geometry_list[0])
    sh_requests = [get_subarea(bbox, all_colour_bands, time_interval, config, data_folder="data", size=(256,256)) for bbox in geometry_list]
    dl_requests = [request.download_list[0] for request in sh_requests]

    # download data with multiple threads
    downloaded_data = SentinelHubDownloadClient(config=config).download(dl_requests, max_threads=40)

    # show_splitter(split_bbox, show_legend=True)
    # for j, kauai in enumerate(hawaii_area.geoms):
    # kauai = hawaii_area.geoms[1]
        # kauai_split = OsmSplitter([kauai], zoom_level=10, crs=CRS.WGS84) # zoom level 14 for full precision
        # show_splitter(kauai_split, show_legend=True)

        # bbox_list = kauai_split.get_bbox_list()
        # sh_requests = [get_subarea(bbox, all_colour_bands, time_interval, config, data_folder="data", size=(256,256)) for bbox in bbox_list]
        # dl_requests = [request.download_list[0] for request in sh_requests]

        # download data with multiple threads
        # downloaded_data = SentinelHubDownloadClient(config=config).download(dl_requests, max_threads=5)

        # print(downloaded_data)

        # Make maps
        # data_folder = sh_requests[0].data_folder
        # tiffs = [Path(data_folder) / req.get_filename_list()[0] for req in sh_requests]
        # composed_tiff = xr.open_mfdataset(tiffs, engine="rasterio")
        # composed_map = composed_tiff.band_data.isel(band=[2,1,0])
        # plot_xr_and_bboxes(composed_map, "extra/test_"+str(i)+"_"+str(j)+".tif")



    print("Map", i, "out of", len(geo_json), "done")

        # kauai_gpd = gpd.GeoDataFrame(geometry=[box(*bbox) for bbox in bbox_list], crs=4326)
        # plot_xr_and_bboxes(composed_tiff.band_data, kauai_gpd)

