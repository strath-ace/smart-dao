import os
import json
import random
import time

import numpy as np
import matplotlib.pyplot as plt

import torch
from torch.utils.data import Dataset, DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor
import torch.optim as optim
from torch.optim import lr_scheduler

from utils import *
from UNET import *
from core import *

####################

# Data batch loader sizes
test_batch_size = 32

model_name = "model_temp"
# Evaluate currently training model

# model_name = "model_1717588915"
# Threshold = 0.87, Multi_scale = 0.1, lr=0.01, momentum=0.9, scheduler = false, 100 iterations
# Max accuracy 73.775%

# model_name = "model_1717575560.410076"
# Threshold = 0.73, Multi_scale = 0.1, lr=0.01, momentum=0.9, scheduler = false, 40 iterations
# Max accuracy 72.977%

model_name = "model_1717610163"
# Threshold = 0.87, Multi_scale = 0.1, lr=0.0075, momentum=0.9, scheduler = false, 100 iterations
# Max accuracy = 73.97%

# model_name = "model_1717660275"
# /10 dataset    No argmax before loss in train
# Threshold = 0.87, Multi_scale = 0.1, lr=0.001, momentum=0.9, scheduler = false, 100 iterations
# Accuracy = 66.16%

# model_name = "model_1717664907"
# /10 dataset
# Threshold = 0.87, Multi_scale = 0.01, lr=0.01, momentum=0.9, scheduler = false, 100 iterations
# Accuracy = 67.9%

# model_name = "model_1717667257"
# /10 dataset With threshold in training also
# Threshold = 0.7, Multi_scale = 0.01, lr=0.01, momentum=0.9, scheduler = false, 100 iterations
# Accuracy = 70.1%

# model_name = "model_1717677939"
# threshold in training also
# Threshold = 0.7, Multi_scale = 0.01, lr=0.01, momentum=0.9, scheduler = false, 100 iterations
# Accuracy = 73.3%

# try lr = 0.0075, multi_scale=0.1 model_1717689924
# Maybe change threshold on training?

####################

# Set model save location
model_save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_save")
if not os.path.exists(model_save_location):
    os.mkdirs(model_save_location)

test_data = CustomImageDataset(
    "../dataset-generator/dataset/reference.json",
     "../dataset-generator/dataset",
     "val"
)
num_classes =  int(load_json("../dataset-generator/dataset/reference.json")["num_classes"])

# Get data loaders and print size
# train_dataloader = DataLoader(training_data, batch_size=train_batch_size, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=test_batch_size, shuffle=True)
# print("Training data loaded - Batch Size:", train_batch_size, " - Number Batches:", len(train_dataloader))
print("Test data loaded     - Batch Size:", test_batch_size, "  - Number Batches:", len(test_dataloader))

# Outputs some random images from training data
# input_viewer(train_dataloader, num_classes)

print("Start learning")

# Set device to train on (Priorities cuda but backup is cpu)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Import UNET model and send to device
model = UNet(num_classes).to(device)


model.load_state_dict(torch.load(model_save_location+"/"+model_name))

# Test the trained model against seperate test data to get accuracy
big_metrics, big_confusion = test_model(model, test_dataloader, num_classes)
# print(big_confusion)
plt.clf()
plt.figure(figsize=(7,7))
plt.imshow(big_confusion, vmin=0, vmax=1, cmap="summer")
for (j,i),label in np.ndenumerate(big_confusion):
    plt.text(i,j,round(100*label,1),ha='center',va='center')
plt.savefig("confusion.png")

save_json("model_stats.json", big_metrics)
