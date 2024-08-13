import torch
import torch.nn as nn
import torch.nn.functional as F
from utils import *
from torchvision.transforms import ToTensor, Normalize, Compose
from torch.utils.data import Dataset
import torch
from torch.utils.data import DataLoader
import sklearn.metrics

from tifffile import imread

import numpy as np
import os
import time

# NOTES
# Remove all values for which a fixed value is given. Such as num_classes=10



def dice_loss(pred, target, smooth=1.):
    pred = pred.contiguous()
    target = target.contiguous()

    intersection = (pred * target).sum(dim=1).sum(dim=1)

    loss = (1 - ((2. * intersection + smooth) / (pred.sum(dim=1).sum(dim=1) + target.sum(dim=1).sum(dim=1) + smooth)))

    return loss.mean()



def train(model,dataloaders, optimizer, use_scheduler=False, epochs=10):
    """
    Train model and store results
    """
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    # best_model_wts = copy.deepcopy(model.state_dict())
    best_loss = 1e10
    stored_data = {"epoch": {}}
    for i, epoch in enumerate(range(epochs)):
        description = 'Epoch {}/{}'.format(epoch+1, epochs)

        model.train()

        sum_loss = 0
        totaler = 0

        for j, data in enumerate(dataloaders):#tqdm(dataloaders,desc=description)):

            inputs = data["image"][:,:-1]
            labels = data["image"][:,-1]

            inputs = inputs.to(device)
            labels = labels.to(device)

            optimizer.zero_grad()

            outputs = model(inputs)

            multi_scale = 0.1   # 0.8 works (0.5, 0.25 good) (0.1 best result so far)          
            
            labels = labels.to(dtype=torch.long)


            labels = F.one_hot(labels, num_classes=10)
            labels = torch.swapaxes(labels, 1,3)
            labels = torch.swapaxes(labels, 2,3)

            labels = labels.to(dtype=torch.float32)

            loss_ce = F.cross_entropy(outputs, labels)

            outputs = F.softmax(outputs, dim=1)

            outputs = F.threshold(outputs, 0.7, 0)

            # Extras
            labels = torch.argmax(labels, dim=1)
            outputs = torch.argmax(outputs, dim=1)

            loss_d = dice_loss(outputs, labels)

            loss = loss_ce * multi_scale + loss_d * (1-multi_scale)

            loss.backward()
            optimizer.step()
            if use_scheduler:
                scheduler.step()

            sum_loss += loss.data.cpu().numpy() * inputs.size(0)
            totaler += inputs.size(0)

        updater = {str(epoch+1): {"loss": sum_loss, "epoch_loss": sum_loss/totaler, "time": 3}}
        stored_data["epoch"].update(updater)
        print("----- Loss:", updater[str(epoch+1)]["epoch_loss"], "-----")
        if updater[str(epoch+1)]["epoch_loss"] < best_loss:
            best_loss = updater[str(epoch+1)]["epoch_loss"]
            temp_model_path = "model_save/model_temp"
            torch.save(model.state_dict(), temp_model_path)

    print('Best val loss: {:4f}'.format(best_loss))
    # save_json("process_output.json", stored_data)
    # # load best model weights
    model.load_state_dict(torch.load(temp_model_path))
    # perm_model_path = "model_save/model_"+str(round(time.time()))
    # torch.save(model.state_dict(), perm_model_path)
    return model, stored_data


def test(model, dataloaders, num_epochs=25):
    """
    Test model and return results
    Return: loss, accuracy

    """
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)

    model.eval()

    sum_loss = 0
    sum_accuracy = 0
    totaler = 0

    big_confusion = np.zeros((10, 10))
    number_in_class = np.zeros(10)
    number_in_pred = np.zeros(10)

    for data in dataloaders:#tqdm(dataloaders,desc=description)):

        inputs = data["image"][:,:-1]
        labels = data["image"][:,-1]

        inputs = inputs.to(device)
        labels_og = labels.to(device)

        # forward
        # with torch.set_grad_enabled(True):
        outputs = model(inputs)

        multi_scale = 0.1   # 0.8 works (0.5, 0.25 good) (0.1 best result so far)   

        labels = labels_og.to(dtype=torch.long)

        labels = F.one_hot(labels, num_classes=10)
        labels = torch.swapaxes(labels, 1,3)
        labels = torch.swapaxes(labels, 2,3)

        labels = labels.to(dtype=torch.float32)

        labels_og = labels_og.to(dtype=torch.float32)

        loss_ce = F.cross_entropy(outputs, labels)

        outputs = F.softmax(outputs, dim=1)
        outputs = F.threshold(outputs, 0.7, 0)
        labels = torch.argmax(labels, dim=1)
        outputs = torch.argmax(outputs, dim=1)

        loss_d = dice_loss(outputs, labels)

        loss = loss_ce * multi_scale + loss_d * (1-multi_scale)

        sum_loss += loss.data.cpu().numpy() * inputs.size(0)
        sum_accuracy += torch.sum(torch.eq(outputs, labels_og)).item()
        totaler += np.prod(list(outputs.size()))

        # Confusion Matrix Calcualtion
        flat_label = torch.flatten(labels).cpu().numpy()
        flat_pred = torch.flatten(outputs).cpu().numpy()
        big_confusion += sklearn.metrics.confusion_matrix(flat_label, flat_pred, labels=np.arange(10))#, normalize="true")

        binners = np.bincount(flat_label)
        binners_pred = np.bincount(flat_pred)
        
        number_in_class[range(len(binners))] += binners
        number_in_pred[range(len(binners_pred))] += binners_pred

    loss = float(sum_loss)/float(totaler)
    accuracy = float(sum_accuracy)/float(totaler)

    for i in range(10):
        if number_in_class[i] > 0:
            big_confusion[i] = big_confusion[i]/number_in_class[i]
    
    return loss, accuracy, big_confusion, number_in_class


class CustomImageDataset(Dataset):
    def __init__(self, annotations_file, dataset_dir, splitter, transform=None, target_transform=None):
        # print("######################")
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
        # print("########################")
        all_patch = np.array(imread(data_path),dtype=float32)
        # print("#########################")
        print(np.shape(all_patch))
        return all_patch
        # inputs = all_patch["input"].astype("float32").swapaxes(0,2).swapaxes(1,2)
        # labels = np.array(self.num_classes*np.flip(all_patch["label"], axis=0).astype("float32"),dtype=int)
        # square_labels = np.zeros((self.num_classes, 256, 256))
        # for i in range(self.num_classes):
        #     square_labels[i][np.where(labels == i)] = i
        # return inputs, square_labels


