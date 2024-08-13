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
import json
from tqdm import tqdm
import sklearn.metrics
# from ignite.metrics import ClassificationReport
# import ignite

from utils import *

bands = ["B02","B03","B04","B05","B06","B07","B08","B11","B12"]

def dice_loss(pred, target, smooth=1.):
    pred = pred.contiguous()
    target = target.contiguous()

    intersection = (pred * target).sum(dim=2).sum(dim=2)

    loss = (1 - ((2. * intersection + smooth) / (pred.sum(dim=2).sum(dim=2) + target.sum(dim=2).sum(dim=2) + smooth)))

    return loss.mean()

def dice_loss_less(pred, target, smooth=1.):
    pred = pred.contiguous()
    target = target.contiguous()

    intersection = (pred * target).sum(dim=1).sum(dim=1)

    loss = (1 - ((2. * intersection + smooth) / (pred.sum(dim=1).sum(dim=1) + target.sum(dim=1).sum(dim=1) + smooth)))

    return loss.mean()

def train_model(model, optimizer, scheduler, dataloaders, use_scheduler=False, num_epochs=25):
    """
    Train model and store results


    """
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    best_model_wts = copy.deepcopy(model.state_dict())
    best_loss = 1e10
    stored_data = {"epoch": {}}
    for i, epoch in enumerate(range(num_epochs)):
        description = 'Epoch {}/{}'.format(epoch+1, num_epochs)

        since = time.time()

        # for param_group in optimizer.param_groups:
        #     print("LR", param_group['lr'])

        model.train()

        # metrics = defaultdict(float)
        sum_loss = 0
        totaler = 0
        # print(len(dataloaders))
        for j, data in enumerate(tqdm(dataloaders,desc=description)):
            # print(data)
            inputs = []
            for k in bands:
                # print(data[i])
                inputs.append(data[k][:,0])
            # print(inputs)
            inputs = torch.tensor(torch.stack(inputs,dim=1), dtype=torch.float32)
            # print("SHAPE-inputs:", inputs.shape)
            # print("SHAPE-label:", data["label"][:,0].shape)
            labels = torch.tensor(data["label"][:,0], dtype=torch.long)
            # print(labels)

            # inputs, labels = data
            inputs = inputs.to(device)
            labels = labels.to(device)

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward
            # with torch.set_grad_enabled(True):
            outputs = model(inputs)

            multi_scale = 0.01   # 0.8 works (0.5, 0.25 good) (0.1 best result so far)   

            loss_ce = F.cross_entropy(outputs, labels, ignore_index=255)

            outputs = F.softmax(outputs, dim=1)
            # loss_d = dice_loss(outputs, labels)

            outputs = F.threshold(outputs, 0.83, 0) # 0.7

            # Extras
            labels = torch.argmax(labels, dim=1)
            outputs = torch.argmax(outputs, dim=1)
            
            # loss_d = dice_loss_less(outputs, labels, )
            ## Also try dice loss before argmax

            loss = loss_ce# * multi_scale + loss_d * (1-multi_scale)

            # loss = F.cross_entropy(outputs, labels)

            loss.backward()
            optimizer.step()
            if use_scheduler:
                scheduler.step()

            sum_loss += loss.data.cpu().numpy() * inputs.size(0)
            totaler += inputs.size(0)

        time_elapsed = time.time() - since

        updater = {str(epoch+1): {"loss": sum_loss, "epoch_loss": sum_loss/totaler, "time": round(time_elapsed, 1)}}
        stored_data["epoch"].update(updater)
        print("----- Loss:", updater[str(epoch+1)]["epoch_loss"], "-----")
        if updater[str(epoch+1)]["epoch_loss"] < best_loss:
            best_loss = updater[str(epoch+1)]["epoch_loss"]
            temp_model_path = "model_save/model_temp"
            torch.save(model.state_dict(), temp_model_path)

        if i % 1 == 0:
            save_json("process_output.json", stored_data)

    print('Best val loss: {:4f}'.format(best_loss))
    save_json("process_output.json", stored_data)
    # load best model weights
    model.load_state_dict(torch.load(temp_model_path))
    perm_model_path = "model_save/model_"+str(round(time.time()))
    torch.save(model.state_dict(), perm_model_path)
    return model, stored_data


def combine_dict(d1, d2):
    return {
        k: tuple(d[k] for d in (d1, d2) if k in d)
        for k in set(d1.keys()) | set(d2.keys())
    }

def test_model(model, test_dataloader, num_classes, image_path="output_view.png"):

    summer = 0
    divisor = 0
    not_run = True
    summer2 = np.zeros(num_classes,dtype=float)
    divisor2 = np.zeros(num_classes,dtype=float)
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    big_metrics = {}
    flat_pred_ex = np.array([])
    flat_label_ex = np.array([])

    confusion = np.zeros((num_classes, 2, 2))
    big_confusion = np.zeros((num_classes, num_classes))
    number_in_class = np.zeros(num_classes)
    number_in_pred = np.zeros(num_classes)
    total_number = 0

    description = "Testing on test subset "
    for j, data in enumerate(tqdm(test_dataloader,desc=description)):

        inputs = []
        for k in bands:
            # print(data[i])
            inputs.append(data[k][:,0])
        # print(inputs)
        inputs = torch.tensor(torch.stack(inputs,dim=1), dtype=torch.float32)
        # print("SHAPE-inputs:", inputs.shape)
        # print("SHAPE-label:", data["label"][:,0].shape)
        labels = torch.tensor(data["label"][:,0], dtype=torch.long)
        inputs = inputs.to(device)
        labels = labels.to(device)

        pred = model(inputs)

        pred = F.softmax(pred, dim=1)

        # Add threshold
        pred = F.threshold(pred, 0.83, 0)            

        labels_out = torch.argmax(labels, dim=1)
        pred = torch.argmax(pred, dim=1)

        pred_out = pred.data

        # if not_run:
        #     test_viewer(pred_out, labels_out, num_classes, image_path)
        #     not_run = False

        flat_pred = pred_out.cpu().numpy().flatten()
        flat_label = labels_out.cpu().numpy().flatten()

        big_confusion += sklearn.metrics.confusion_matrix(flat_label, flat_pred, labels=np.arange(num_classes))#, normalize="true")
    
        confusion += sklearn.metrics.multilabel_confusion_matrix(flat_label, flat_pred, labels=np.arange(num_classes))

        total_number += len(flat_label)

        binners = np.bincount(flat_label)
        binners_pred = np.bincount(flat_pred)
        
        number_in_class[range(len(binners))] += binners
        number_in_pred[range(len(binners_pred))] += binners_pred

    precision_li = []
    recall_li = []
    F1_li = []
    accuracy_count = 0
    for cla in confusion:
        TP = cla[1,1]
        FP = cla[1,0]
        FN = cla[0,1]
        TN = cla[0,0]
        try:
            precision = TP/(TP+FP)
        except:
            precision = 0
        try:
            recall = TP/(TP+FN)
        except:
            recall = 0
        try:
            F1 = TP/(TP+(0.5*(FP+FN)))
        except:
            F1 = 0
        precision_li.append(precision)
        recall_li.append(recall)
        F1_li.append(F1)
        accuracy_count += TP

    precision_li = np.array(precision_li)
    recall_li = np.array(recall_li)
    F1_li = np.array(F1_li)

    F1_macro = np.nanmean(F1_li)
    F1_weighted = (np.nansum(F1_li*number_in_class))/total_number
    accuracy = accuracy_count/total_number

    precision_li[precision_li == np.nan] = 0
    recall_li[recall_li == np.nan] = 0
    F1_li[F1_li == np.nan] = 0

    big_metrics = {
        "per_class": {
            "precision": precision_li.tolist(),
            "recall": recall_li.tolist(),
            "F1-score": F1_li.tolist(),
            "support_true": number_in_class.tolist(),
            "support_pred": number_in_pred.tolist()
        },
        "f1-macro": F1_macro,
        "f1-weighted": F1_weighted,
        "accuracy": accuracy
    }

    for i in range(num_classes):
        # print(number_in_class[i])
        if number_in_class[i] > 0:
            big_confusion[i] = big_confusion[i]/number_in_class[i]

    return big_metrics, big_confusion



class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, dataset_dir, splitter, transform=None, target_transform=None):
        self.img_data = load_json(annotations_file)
        self.split_list = self.img_data[splitter]
        self.dataset_dir = dataset_dir
        self.transform = transform
        self.target_transform = target_transform
        self.num_classes = int(load_json(annotations_file)["num_classes"])

    def __len__(self):
        # return len(self.split_list)
        return int(len(self.split_list))

    def __getitem__(self, idx):
        data_path = os.path.join(self.dataset_dir, self.img_data["all_data"][self.split_list[idx]]["path"])
        all_patch = np.load(data_path)
        inputs = all_patch["input"].astype("float32").swapaxes(0,2).swapaxes(1,2)
        labels = np.array(self.num_classes*np.flip(all_patch["label"], axis=0).astype("float32"),dtype=int)
        square_labels = np.zeros((self.num_classes, 256, 256))
        for i in range(self.num_classes):
            square_labels[i][np.where(labels == i)] = i
        return inputs, square_labels