import argparse
from collections import OrderedDict
from typing import Dict, Tuple, List
import time
import os
import yaml

import torch
from torch.utils.data import DataLoader

import flwr as fl
from flwr.common import Metrics
from flwr.common.typing import Scalar

from datasets import Dataset, load_dataset
from datasets.utils.logging import disable_progress_bar
from flwr_datasets import FederatedDataset
from flwr_datasets.partitioner import IidPartitioner
from flwr_datasets.utils import divide_dataset

from torch.utils.data import random_split

from utils import *
# from utils import Net

# num_classes =  int(load_json("../dataset-generator/dataset2/reference.json")["num_classes"])
model = Net(10)



number_of_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print("Number of parameters with weights:", number_of_params)
print("Size on disk of parameters:", round(number_of_params*4/(1024*1024),2), "MB")

# float32 == 4 bytes

# 70000 => 11.6 MB

# 0.99 MB for 6000 images in dataset
# 0.17 MB for model weights