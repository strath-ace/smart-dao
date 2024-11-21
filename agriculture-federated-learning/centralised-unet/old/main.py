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
import datasets as dt
# from datasets import load_dataset

from utils import *
from UNET import *
from core import *

####################

# Data batch loader sizes
train_batch_size = 32
test_batch_size = 32

# Training epochs
training_epochs = 10

scheduler_on = False

####################

# Set model save location
model_save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model_save")
if not os.path.exists(model_save_location):
    os.mkdir(model_save_location)

# # Get datasets
# training_data = CustomImageDataset(
#     "../dataset-generator/dataset/reference.json",
#      "../dataset-generator/dataset",
#      "train"
# )
# test_data = CustomImageDataset(
#     "../dataset-generator/dataset/reference.json",
#      "../dataset-generator/dataset",
#      "val"
# )
# num_classes =  int(load_json("../dataset-generator/dataset/reference.json")["num_classes"])

training_data = dt.load_dataset("0x365/eo-crop-type-belgium", split=dt.ReadInstruction(
    'train', from_=0, to=10, unit='%', rounding='pct1_dropremainder')).with_format("torch")
test_data = dt.load_dataset("0x365/eo-crop-type-belgium", split=dt.ReadInstruction(
    'train', from_=80, to=90, unit='%', rounding='pct1_dropremainder')).with_format("torch")
num_classes = 78

print(training_data, test_data)

# Get data loaders and print size
train_dataloader = DataLoader(training_data, batch_size=train_batch_size, shuffle=True)
test_dataloader = DataLoader(test_data, batch_size=test_batch_size, shuffle=True)
print("Training data loaded - Batch Size:", train_batch_size, " - Number Batches:", len(train_dataloader))
print("Test data loaded     - Batch Size:", test_batch_size, "  - Number Batches:", len(test_dataloader))

print(train_dataloader, test_dataloader)

# Outputs some random images from training data
input_viewer(train_dataloader, num_classes)

print("Start learning")

# Set device to train on (Priorities cuda but backup is cpu)
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# Import UNET model and send to device
model = UNet(num_classes).to(device)

# Optimizer and scheduler definitions
optimizer_sgd = optim.SGD(model.parameters(), lr=0.01, momentum=0.9)  # lr=0.001, momentum=0.95)
optimizer_ft = optim.Adam(filter(lambda p: p.requires_grad, model.parameters()), lr=0.01)#1e-4)
exp_lr_scheduler = lr_scheduler.StepLR(optimizer_sgd, step_size=90, gamma=0.1)

# Train the model on train_dataloader data
# model, learning_metrics = train_model(model, optimizer_sgd, exp_lr_scheduler, train_dataloader, use_scheduler=scheduler_on, num_epochs=training_epochs)

# Plot the learning metrics generated from training
# plot_learning_metrics(learning_metrics)

# Test the trained model against seperate test data to get accuracy
# model = copy.deepcopy(torch.load("model_save/model_temp").state_dict())
model.load_state_dict(torch.load("model_save/model_temp"))
big_metrics, big_confusion = test_model(model, test_dataloader, num_classes)

save_json("model_stats.json", big_metrics)