import matplotlib.pyplot as plt
import numpy as np
import rasterio.features
from shapely import intersection, Polygon, box, overlaps, within, MultiPolygon
from PIL import Image
from matplotlib import cm

import os
import json





def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

# big_features = (load_json("perm_data/belgium_cut.json")["features"])
print("Start big json loading")
big_features = (load_json("perm_data/belgium_crop_type.json")["features"])
print("Done big json load")

print("Get all files")
boxes = []
for root, dirs, files in os.walk("data", topdown=False):
    for name in files:
        file_path = os.path.join(root, name)
        if file_path[-12:] == "request.json":
            new_box = load_json(file_path)["request"]["payload"]["input"]["bounds"]["bbox"]
            xmin = new_box[0]
            xmax = new_box[2]
            ymin = new_box[1]
            ymax = new_box[3]
            boxes.append([file_path[:-13], box(xmin,ymin,xmax,ymax), {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax}])
print("Got all files")
# print(boxes)


print("Start main program")
maintain = []
fail_count = 0
for boxy in boxes:
	create_file = not os.path.isfile(boxy[0]+"/label.npy")
	# if not os.path.isfile(boxy[0]+"/test.tif") or True:
	big_image = np.zeros((256,256),dtype=int)
	poly_box = boxy[1]
	next_set = []
	for feat in big_features:

		no_over_lap = False
		for poly_all in feat["geometry"]["coordinates"][0]:
			poly_big = Polygon(poly_all)
			overlapper = overlaps(poly_box, poly_big)
			withiner = within(poly_big, poly_box)
			if overlapper or withiner:
				poly3 = intersection(poly_box, poly_big)
				if overlapper and not withiner:
					no_over_lap = True
				if create_file:
					try:
						poly3_coords = np.array(poly3.exterior.coords)
						poly3_coords[:,0] = 256*(poly3_coords[:,0] - boxy[2]["xmin"]) / (boxy[2]["xmax"] - boxy[2]["xmin"])
						poly3_coords[:,1] = 256*(poly3_coords[:,1] - boxy[2]["ymin"]) / (boxy[2]["ymax"] - boxy[2]["ymin"])
						img = rasterio.features.rasterize([Polygon(poly3_coords)], out_shape=(256, 256))
						img = np.array(img, dtype=bool)
						big_image[img] = feat["properties"]["CT"]
					except:
						fail_count += 1
						print("Fail count:", fail_count)
			else:
				no_over_lap = True
		if no_over_lap:
			next_set.append(feat)

	# del big_features
	print("Big feature count", len(big_features))
	big_features = next_set
	del next_set

	if create_file:
		np.save(boxy[0]+"/label", big_image)
		# im = Image.fromarray(np.uint8(cm.gist_earth(big_image)*255))
		# im.save(boxy[0]+"/test.tif")

		print(boxy[0], "is created", np.sum(big_image))
	else:
		print("File was already created", boxy[0])


del big_features
print("Finished")
