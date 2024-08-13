import os
import numpy as np
from torch.utils.data import DataLoader
import torch
from torch.utils.data import Dataset
from torchvision import datasets
from torchvision.transforms import ToTensor
import matplotlib.pyplot as plt
import json
import random
import matplotlib.pyplot as plt
import numpy as np
import random
from functools import reduce
import itertools
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, datasets, models
from collections import defaultdict
import torch.nn.functional as F
import torch
import torch.optim as optim
from torch.optim import lr_scheduler
import time
import copy
from numpy.random import default_rng


bands = ["B02","B03","B04","B05","B06","B07","B08","B11","B12"]

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output


def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)


def input_viewer(train_dataloader, num_classes, how_many_examples=5, save_path="input_view.png"):
    all_points = next(iter(train_dataloader))
    train_features = []
    for i in bands:
        train_features.append(all_points[i])
    train_labels = all_points["label"]
    fig, ax = plt.subplots(how_many_examples,10, figsize=(10,10))
    # train_labels = torch.argmax(train_labels, dim=1)
    for i in range(how_many_examples):
        data_point_id = random.randint(0, len(train_features)-1)
        img = train_features[data_point_id].squeeze()
        labels_out = train_labels[data_point_id].cpu().numpy()[0]
        for j in range(9):
            ax[i,j].imshow(img[j,:,:])
            ax[i,9].imshow(labels_out, vmin=0, vmax=num_classes, cmap="rainbow")
        plt.savefig(save_path)


def test_viewer(pred_out, labels_out, num_classes, file_path):
    fig, ax = plt.subplots(4,2, figsize=(4,10))
    pred_out = pred_out.cpu().numpy()
    labels_out = labels_out.cpu().numpy()
    # print(pred_out, np.shape(pred_out))
    for i in range(4):
        ax[i,0].imshow(labels_out[i], vmin=0, vmax=num_classes, cmap="rainbow")
        ax[i,1].imshow(pred_out[i], vmin=0, vmax=num_classes, cmap="rainbow")
        
    plt.savefig(file_path)



# # DEV
# def parallel_plot_tensor(left_side, right_side, num_classes, file_path):
#     left_side = left_side.cpu().numpy()
#     right_side = right_side.cpu().numpy()

#     width = np.shape(left_side)[1]+np.shape(right_side)[1]
    
#     fig, ax = plt.subplots(4,width, figsize=(width/2,10))
    
#     max_random = np.shape(left_side)[0]
#     rng = default_rng()
#     numbers = rng.choice(max_random, size=4, replace=False)
#     for i, ra in enumerate(numbers):
#         # if np.shape(np.shape(left_side)) == 3:
        
#         # else: 
#         for j in range(width):
#             if j < np.shape(left_side)[1]:
#                 ax[i,j].imshow(left_side[ra,j], vmin=0, vmax=num_classes)
#             else:
#                 ax[i,j].imshow(right_side[ra,j], vmin=0, vmax=num_classes)
    
#     plt.savefig(file_path)


def plot_learning_metrics(learning_metrics, data_path="losses.png"):
    metric_loss = []
    metric_counter = []
    for x in learning_metrics["epoch"].keys():
        metric_loss.append(learning_metrics["epoch"][x]["epoch_loss"])
        metric_counter.append(x)

    plt.clf()
    plt.figure(figsize=(5,5))
    plt.plot(metric_loss, label="Cross Entropy")
    plt.title("Losses from Cross Entropy while training")
    # plt.yscale("log")
    plt.savefig(data_path)
    plt.clf()


# def plot_class_accuracy(overall_accuracy, class_accuracy, file_path="class_accuracy.png"):
#     indx = np.flip(np.argsort(class_accuracy))
#     class_accuracy = class_accuracy[indx]
#     plt.clf()
#     plt.figure(figsize=(5,5))
#     plt.bar(np.arange(len(class_accuracy)), class_accuracy)
#     plt.title("Class Accuracies - Overall accuracy = "+str(round(overall_accuracy,5)))
#     plt.savefig(file_path)