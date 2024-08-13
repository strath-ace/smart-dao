import numpy as np
from tifffile import imread, imsave
# import tiffile
import os
import json
import csv
from PIL import Image

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)

# Input
def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(int(row[0]))  
    f.close()
    return output

save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset2")
if not os.path.exists(save_location):
    os.makedirs(save_location)
data_location = os.path.join(save_location, "data")
if not os.path.exists(data_location):
    os.makedirs(data_location)
data_location_train = os.path.join(data_location, "train", "0")
if not os.path.exists(data_location_train):
    os.makedirs(data_location_train)
data_location_test = os.path.join(data_location, "test", "0")
if not os.path.exists(data_location_test):
    os.makedirs(data_location_test)


all_classes = csv_input("perm_data/all_crop_numbers.csv")
unique_classes = np.unique(all_classes)
indx = np.argsort(unique_classes)
# print(class_counts[indx])
# indx = indx
unique_classes = unique_classes[indx]
class_map = np.linspace(0, 1, len(unique_classes))
# print(unique_classes, class_map)
# print(class_map)
num_classes = len(unique_classes)



whole_list = {}
all_names_train = []
all_names_val = []
c = 0
split = 0.8

uni_stack = []
cou_stack = []
counter = 0
for root, dirs, files in os.walk("data", topdown=False):
    for i, name in enumerate(files):
        file_path = os.path.join(root, name)
        if os.path.exists(file_path[:-12]+"/label.npy"):
            counter += 1
            uni, cou = np.unique(np.load(file_path[:-12]+"/label.npy"), return_counts=True)
            for k, x in enumerate(uni):
                if x in uni_stack:
                    for l, y in enumerate(uni_stack):
                        if x == y:
                            cou_stack[l] += cou[k]
                else:
                    uni_stack.append(x)
                    cou_stack.append(cou[k])

# print(uni_stack)
# print(cou_stack)

indx = np.flip(np.argsort(cou_stack))
indx = indx[:10]
print(indx)
# print(indx)
unique_classes = (np.array(uni_stack)[indx])
# class_map = np.round(np.linspace(0, 255, len(unique_classes)))
class_map = np.arange(len(unique_classes), dtype=int)
# print(unique_classes, class_map)
# print(class_map)
num_classes = len(unique_classes)
print(num_classes)

# print(counter)

for root, dirs, files in os.walk("data", topdown=False):
    for i, name in enumerate(files):
        file_path = os.path.join(root, name)
        if str(file_path).split("/")[-1] == "request.json":
            new_name = str(file_path).split("/")[-2]
            if os.path.exists(file_path[:-12]+"/response.tiff") and os.path.exists(file_path[:-12]+"/label.npy"):
                new_bounds = load_json(file_path)["request"]["payload"]["input"]["bounds"]
                new_data = load_json(file_path)["request"]["payload"]["input"]["data"]

                xmin = new_bounds["bbox"][0]
                xmax = new_bounds["bbox"][2]
                ymin = new_bounds["bbox"][1]
                ymax = new_bounds["bbox"][3]
                
                input_data = imread(file_path[:-12]+"/response.tiff")
                label_data = np.array(np.load(file_path[:-12]+"label.npy"),dtype=float)
                new_labels = np.zeros(np.shape(label_data))
                for j, cla in enumerate(unique_classes):
                    new_labels[label_data == cla] = class_map[j]
                    # print(class_map[j])
                    # print(np.sum(label_data==cla))
                # print(np.mean(label_data))
                # np.savez(data_location+"/"+new_name, input=input_data, label=new_labels)
                
                
                input_data = np.swapaxes(input_data, 0,2)
                input_data = np.swapaxes(input_data, 1,2)
                output_data = np.append(input_data, [np.flip(new_labels, axis=0)], axis=0)
                # im = Image.fromarray(output_data)
                # im.save(data_location+"/"+new_name+".tif", bigtiff=True)
                if c < split*counter:
                    all_names_train.append(new_name)
                    # print(np.shape(output_data))
                    # print(np.shape(np.uint8(output_data)))
                    # output_data = np.swapaxes(output_data,0,2)
                    # pil_image = Image.fromarray(np.uint8(output_data))
                    # pil_image.save(data_location+"/"+"train"+"/"+new_name+".png")
                    imsave(data_location+"/"+"train"+"/0/"+new_name+".tiff", output_data, bigtiff=True)
                else:
                    all_names_val.append(new_name)
                    # pil_image = Image.fromarray(np.uint8(output_data))
                    # pil_image.save(data_location+"/"+"train"+"/"+new_name+".png")
                    imsave(data_location+"/"+"test"+"/0/"+new_name+".tiff", output_data, bigtiff=True)
                # imsave(data_location+"/"+"train"+"/"+new_name+".tiff", output_data, bigtiff=True)

                ##### SPLIT ##### >= seems wrong way round but produces correct data
                if c < split*counter:
                    all_names_train.append(new_name)
                else:
                    all_names_val.append(new_name)
                
                whole_list.update({new_name: {
                    "path": "data/"+new_name+".tiff",
                    "box": {"xmin": xmin, "xmax": xmax, "ymin": ymin, "ymax": ymax},
                    "bound_data": new_bounds,
                    "extra_data": new_data
                }})
            # else:
                # print(new_name, "does not have all required files")
    if c % 100 == 0:
        print(c, "done out of 6000")
    # print(, "out of", len(files), "files done")
    c += 1

save_json(save_location+"/reference.json", {"train": all_names_train, "val": all_names_val, "num_classes": str(num_classes), "all_data": whole_list})
