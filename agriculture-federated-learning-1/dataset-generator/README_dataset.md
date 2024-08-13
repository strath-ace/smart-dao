# Belgium Crop Type Dataset with Sentinel-2A Product

Contents

`/data/` contains the `.npz` versions of each images. In each `.npz` file you can access array "input" which is a 256x256x9 array containing 10m resolution images from Sentinel-2A with the 9 bands (B02, B03, B04, B05, B06, B07, B08, B11, B12). The other array in the `.npz` file is the "label". This label comes from [here](https://worldcereal-rdm.geo-wiki.org/collections/details/?id=2018beflandersfullpoly110).

The crop types for classification are given at the link.

