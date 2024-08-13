# ESA Φ-Lab - Decentralised Federated Learning ESA Project

## About

Design and Implementation of Federated Learning for Crop Yield Estimation

## Notes

- Average mnist initial dataset across random seeds?

### Current Ideas
- Implementations with Pytorch
- Federation of the model with [Flower](https://flower.ai/)
- Differential Privacy with [OPACUS](https://github.com/pytorch/opacus)

### Current Datasets

#### MNIST
- Full dataset with labels [LINK](https://huggingface.co/datasets/ylecun/mnist)

#### Crop Type
- Sentinel-2 L2A Satellite Images 9 bands
- World Cereal all datasets [LINK](https://worldcereal-rdm.geo-wiki.org/map/)
- World Cereal Belgium crop type dataset [LINK](https://worldcereal-rdm.geo-wiki.org/collections/details/?id=2018beflandersfullpoly110)

#### Crop Yield

- Crop Production in EU standard humididty by NUTS 2 regions [LINK](https://ec.europa.eu/eurostat/databrowser/view/apro_cpshr/default/table?lang=en&category=agr.apro.apro_crop.apro_cp.apro_cpsh)
- It is now hard to find nuts2 regional divisions but I have a copy

### Test scheme

#### How centralised data effects learning

How centralised is data access and data generation. DIfferent scales of centralisation

Does more centralised data owners prooduce better federated learning. How does decentalisation affect federation.

#### Testing bandwidth on decentralised model

How long does model propagation take with gossip protocol. How big is the model being distributed. Bandwidth requirements. Are there other protocols available.

More information can be found in `./docs`.

## Results

### Crop-Type
<img src="https://github.com/0x365/esa-federated-learning/blob/main/results/crop_type_results.png" width="350" height="350"></img>
<img src="https://github.com/0x365/esa-federated-learning/blob/main/results/movie.gif" width="350" height="350"></img>

Test with Crop Type dataset
```yaml
UM_CPU: 10      # Change to 10 for server
NUM_GPU: 0.1    # Change to 0.1 for server

# How many full runs of process
TRAINING_ITERATIONS: 10

# Tests
TARGET_NUM_CLIENTS: [2, 4, 8, 16, 32, 64, 128, 256]
PARTITION_SCALER: 10

# Aggregator
AGR_fraction_fit: 1.0         # Sample 10% of available clients for training
AGR_fraction_evaluate: 0.05   # Sample 5% of available clients for evaluation
AGR_min_available_clients: 2
AGR_NUM_ROUNDS: 20            # Number of rounds of aggregations
AGR_batch_size: 50            # Centralised Evaluation data loader batch size

# Per client
CL_epochs: 10                 # Number of local epochs done by clients
CL_batch_size: 10            # Batch size to use by clients during fit()
CL_test_size: 0.1             # Test train split for each client
CL_seed: 42                   # Random seed for each client

# Learning
LE_lr: 0.01                  # optimizer
LE_momentum: 0.9             # optimizer
```

Crop Type UNET Model has 31,035,786 trainable parameters. This equates to approximately 118 MB (119MB in practice) if each is a float32 value at 4 bytes. Comparing this to the dataset2 file that it was trained on gives:
```python
# Training data == 22.8 GB => 4552 files
# Evaluation data == 1.2 GB => 240 files
# Testing data == 5.9 GB => 1198 files
```

```python
class UNet(nn.Module):
    def __init__(self, n_class):
        super().__init__()
        
        # Encoder
        # In the encoder, convolutional layers with the Conv2d function are used to extract features from the input image. 
        # Each block in the encoder consists of two convolutional layers followed by a max-pooling layer, with the exception of the last block which does not include a max-pooling layer.
        # -------
        # input: 256x256x9
        self.e11 = nn.Conv2d(9, 64, kernel_size=3, padding=1) # output: 254x254x64
        self.e12 = nn.Conv2d(64, 64, kernel_size=3, padding=1) # output: 252x252x64
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2) # output: 126x126x64

        # input: 126x126x64
        self.e21 = nn.Conv2d(64, 128, kernel_size=3, padding=1) # output: 124x124x128
        self.e22 = nn.Conv2d(128, 128, kernel_size=3, padding=1) # output: 122x122x128
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2) # output: 61x61x128

        # input: 61x61x128
        self.e31 = nn.Conv2d(128, 256, kernel_size=3, padding=1) # output: 59x59x256
        self.e32 = nn.Conv2d(256, 256, kernel_size=3, padding=1) # output: 57x57x256
        self.pool3 = nn.MaxPool2d(kernel_size=2, stride=2) # output: 28x28x256

        # input: 28x28x256
        self.e41 = nn.Conv2d(256, 512, kernel_size=3, padding=1) # output: 26x26x512
        self.e42 = nn.Conv2d(512, 512, kernel_size=3, padding=1) # output: 24x24x512
        self.pool4 = nn.MaxPool2d(kernel_size=2, stride=2) # output: 12x12x512

        # input: 12x12x512
        self.e51 = nn.Conv2d(512, 1024, kernel_size=3, padding=1) # output: 10x10x1024
        self.e52 = nn.Conv2d(1024, 1024, kernel_size=3, padding=1) # output: 8x8x1024


        # Decoder
        # In the decoder, transpose convolutional layers with the ConvTranspose2d function are used to upsample the feature maps to the original size of the input image. 
        # Each block in the decoder consists of an upsampling layer, a concatenation with the corresponding encoder feature map, and two convolutional layers.
        # -------
        self.upconv1 = nn.ConvTranspose2d(1024, 512, kernel_size=2, stride=2)
        self.d11 = nn.Conv2d(1024, 512, kernel_size=3, padding=1)
        self.d12 = nn.Conv2d(512, 512, kernel_size=3, padding=1)

        self.upconv2 = nn.ConvTranspose2d(512, 256, kernel_size=2, stride=2)
        self.d21 = nn.Conv2d(512, 256, kernel_size=3, padding=1)
        self.d22 = nn.Conv2d(256, 256, kernel_size=3, padding=1)

        self.upconv3 = nn.ConvTranspose2d(256, 128, kernel_size=2, stride=2)
        self.d31 = nn.Conv2d(256, 128, kernel_size=3, padding=1)
        self.d32 = nn.Conv2d(128, 128, kernel_size=3, padding=1)

        self.upconv4 = nn.ConvTranspose2d(128, 64, kernel_size=2, stride=2)
        self.d41 = nn.Conv2d(128, 64, kernel_size=3, padding=1)
        self.d42 = nn.Conv2d(64, 64, kernel_size=3, padding=1)

        # Output layer
        self.outconv = nn.Conv2d(64, n_class, kernel_size=1)

    def forward(self, x):
        # Encoder
        xe11 = relu(self.e11(x))
        xe12 = relu(self.e12(xe11))
        xp1 = self.pool1(xe12)

        xe21 = relu(self.e21(xp1))
        xe22 = relu(self.e22(xe21))
        xp2 = self.pool2(xe22)

        xe31 = relu(self.e31(xp2))
        xe32 = relu(self.e32(xe31))
        xp3 = self.pool3(xe32)

        xe41 = relu(self.e41(xp3))
        xe42 = relu(self.e42(xe41))
        xp4 = self.pool4(xe42)

        xe51 = relu(self.e51(xp4))
        xe52 = relu(self.e52(xe51))
        
        # Decoder
        xu1 = self.upconv1(xe52)
        xu11 = torch.cat([xu1, xe42], dim=1)
        xd11 = relu(self.d11(xu11))
        xd12 = relu(self.d12(xd11))

        xu2 = self.upconv2(xd12)
        xu22 = torch.cat([xu2, xe32], dim=1)
        xd21 = relu(self.d21(xu22))
        xd22 = relu(self.d22(xd21))

        xu3 = self.upconv3(xd22)
        xu33 = torch.cat([xu3, xe22], dim=1)
        xd31 = relu(self.d31(xu33))
        xd32 = relu(self.d32(xd31))

        xu4 = self.upconv4(xd32)
        xu44 = torch.cat([xu4, xe12], dim=1)
        xd41 = relu(self.d41(xu44))
        xd42 = relu(self.d42(xd41))

        # Output layer
        out = self.outconv(xd42)

        return out
```

### MNIST
<img src="https://github.com/0x365/esa-federated-learning/blob/main/results/mnist_results.png" width="350" height="350"></img>
<img src="https://github.com/0x365/esa-federated-learning/blob/main/results/mnist_non_iid_square_results.png" width="350" height="350"></img>
Test with MNIST dataset comparing federation scale against accuracy after 10 rounds of aggregation. The size of the dataset remains constant. The parameters are given below:
```yaml
# How many full runs of process
TRAINING_ITERATIONS: 10

# Tests
TARGET_NUM_CLIENTS: [2, 3, 4, 5, 10, 20, 30, 40, 50, 75, 100, 150, 200, 250, 300]
PARTITION_SCALER: 10

# Aggregator
AGR_fraction_fit: 0.1         # Sample 10% of available clients for training
AGR_fraction_evaluate: 0.05   # Sample 5% of available clients for evaluation
AGR_min_available_clients: 2
AGR_NUM_ROUNDS: 10            # Number of rounds of aggregations
AGR_batch_size: 50            # Centralised Evaluation data loader batch size

# Per client
CL_epochs: 1                 # Number of local epochs done by clients
CL_batch_size: 10            # Batch size to use by clients during fit()
CL_test_size: 0.1             # Test train split for each client
CL_seed: 42                   # Random seed for each client

# Learning
LE_lr: 0.01                  # optimizer
LE_momentum: 0.9             # optimizer
```

MNIST model
```python
class Net(nn.Module):
    def __init__(self, num_classes: int = 10) -> None:
        super(Net, self).__init__()
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(6, 16, 5)
        self.fc1 = nn.Linear(16 * 4 * 4, 120)
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = x.view(-1, 16 * 4 * 4)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x
```