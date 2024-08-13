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

from datasets import Dataset
from datasets.utils.logging import disable_progress_bar
from flwr_datasets import FederatedDataset

from utils import Net, train, test, apply_transforms


parser = argparse.ArgumentParser(description="Flower Simulation with PyTorch")

file_location = os.path.dirname(os.path.abspath(__file__))
with open(file_location+"/../params.yml", "r") as f:
    params_config = yaml.load(f, Loader=yaml.SafeLoader)
print(params_config)

parser.add_argument(
    "--num_cpus",
    type=int,
    default=params_config["NUM_CPU"],
    help="Number of CPUs to assign to a virtual client",
)
parser.add_argument(
    "--num_gpus",
    type=float,
    default=params_config["NUM_GPU"],
    help="Ratio of GPU memory to assign to a virtual client",
)

TARGET_NUM_CLIENTS = params_config["TARGET_NUM_CLIENTS"]
NUM_ROUNDS = params_config["AGR_NUM_ROUNDS"]

# Flower client, adapted from Pytorch quickstart example
class FlowerClient(fl.client.NumPyClient):
    def __init__(self, trainset, valset):
        self.trainset = trainset
        self.valset = valset

        # Instantiate model
        self.model = Net()

        # Determine device
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)  # send model to device

    def get_parameters(self, config):
        return [val.cpu().numpy() for _, val in self.model.state_dict().items()]

    def fit(self, parameters, config):
        set_params(self.model, parameters)

        # Read from config
        batch, epochs = config["batch_size"], config["epochs"]

        # Construct dataloader
        trainloader = DataLoader(self.trainset, batch_size=batch, shuffle=True)

        # Define optimizer
        optimizer = torch.optim.SGD(self.model.parameters(), lr=params_config["LE_lr"], momentum=params_config["LE_momentum"])
        # Train
        train(self.model, trainloader, optimizer, epochs=epochs, device=self.device)

        # Return local model and statistics
        return self.get_parameters({}), len(trainloader.dataset), {}

    def evaluate(self, parameters, config):
        set_params(self.model, parameters)

        # Construct dataloader
        valloader = DataLoader(self.valset, batch_size=64)

        # Evaluate
        loss, accuracy = test(self.model, valloader, device=self.device)

        # Return statistics
        return float(loss), len(valloader.dataset), {"accuracy": float(accuracy)}


def get_client_fn(dataset: FederatedDataset):
    """Return a function to construct a client.

    The VirtualClientEngine will execute this function whenever a client is sampled by
    the strategy to participate.
    """

    def client_fn(cid: str) -> fl.client.Client:
        """Construct a FlowerClient with its own dataset partition."""

        # Let's get the partition corresponding to the i-th client
        client_dataset = dataset.load_partition(int(cid), "train")
        
        # print(client_dataset.num_rows)

        # Now let's split it into train (90%) and validation (10%)
        client_dataset_splits = client_dataset.train_test_split(test_size=0.1, seed=42)
        
        trainset = client_dataset_splits["train"]
        valset = client_dataset_splits["test"]
        
        # print(trainset.num_rows)

        # Now we apply the transform to each batch.
        trainset = trainset.with_transform(apply_transforms)
        valset = valset.with_transform(apply_transforms)

        # Create and return client
        return FlowerClient(trainset, valset).to_client()

    return client_fn


def fit_config(server_round: int) -> Dict[str, Scalar]:
    """Return a configuration with static batch size and (local) epochs."""
    config = {
        "epochs": params_config["CL_epochs"],  # Number of local epochs done by clients
        "batch_size": params_config["CL_batch_size"],  # Batch size to use by clients during fit()
    }
    return config


def set_params(model: torch.nn.ModuleList, params: List[fl.common.NDArrays]):
    """Set model weights from a list of NumPy ndarrays."""
    params_dict = zip(model.state_dict().keys(), params)
    state_dict = OrderedDict({k: torch.Tensor(v) for k, v in params_dict})
    model.load_state_dict(state_dict, strict=True)


def weighted_average(metrics: List[Tuple[int, Metrics]]) -> Metrics:
    """Aggregation function for (federated) evaluation metrics, i.e. those returned by
    the client's evaluate() method."""
    # Multiply accuracy of each client by number of examples used
    accuracies = [num_examples * m["accuracy"] for num_examples, m in metrics]
    examples = [num_examples for num_examples, _ in metrics]

    # Aggregate and return custom metric (weighted average)
    return {"accuracy": sum(accuracies) / sum(examples)}


def get_evaluate_fn(
    centralized_testset: Dataset,
):
    """Return an evaluation function for centralized evaluation."""

    def evaluate(
        server_round: int, parameters: fl.common.NDArrays, config: Dict[str, Scalar]
    ):
        """Use the entire CIFAR-10 test set for evaluation."""

        # Determine device
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        model = Net()
        set_params(model, parameters)
        model.to(device)

        # Apply transform to dataset
        testset = centralized_testset.with_transform(apply_transforms)     
        
        # Disable tqdm for dataset preprocessing
        disable_progress_bar()

        testloader = DataLoader(testset, batch_size=params_config["AGR_batch_size"])
        loss, accuracy = test(model, testloader, device=device)

        return loss, {"accuracy": accuracy}

    return evaluate




import json
def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)
def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output


def main():

    # Parse input arguments
    args = parser.parse_args()

    # Resources to be assigned to each virtual client
    client_resources = {
        "num_cpus": args.num_cpus,
        "num_gpus": args.num_gpus,
    }

    
    save_location = os.path.join(file_location, "..", "data", "iid")
    if not os.path.exists(save_location):
        os.makedirs(save_location)

    for j in range(1,params_config["TRAINING_ITERATIONS"]+1):
        file_name = save_location+"/output_r"+str(j)+".json"
        if not os.path.exists(file_name):
            json_out = {}

            for i in TARGET_NUM_CLIENTS:

                # Download MNIST dataset and partition it
                mnist_fds = FederatedDataset(dataset="mnist", partitioners={"train": i*params_config["PARTITION_SCALER"]})
                centralized_testset = mnist_fds.load_split("test")

                run_details = mnist_fds._view_dataset()

                # Configure the strategy
                strategy = fl.server.strategy.FedAvg(
                    fraction_fit=params_config["AGR_fraction_fit"],  # Sample 10% of available clients for training
                    fraction_evaluate=params_config["AGR_fraction_evaluate"],  # Sample 5% of available clients for evaluation
                    min_available_clients=params_config["AGR_min_available_clients"],
                    on_fit_config_fn=fit_config,
                    evaluate_metrics_aggregation_fn=weighted_average,  # Aggregate federated metrics
                    evaluate_fn=get_evaluate_fn(centralized_testset),  # Global evaluation function
                )

                # ClientApp for Flower-Next
                client = fl.client.ClientApp(
                    client_fn=get_client_fn(mnist_fds),
                )

                # ServerApp for Flower-Next
                server = fl.server.ServerApp(
                    config=fl.server.ServerConfig(num_rounds=NUM_ROUNDS),
                    strategy=strategy,
                )


                # Start simulation
                stuff = fl.simulation.start_simulation(
                    client_fn=get_client_fn(mnist_fds),
                    num_clients=i,#NUM_CLIENTS,
                    client_resources=client_resources,
                    config=fl.server.ServerConfig(num_rounds=NUM_ROUNDS),
                    strategy=strategy,
                    actor_kwargs={
                        "on_actor_init_fn": disable_progress_bar  # disable tqdm on each actor/process spawning virtual clients
                    },
                )
                json_out.update({
                    str(i): {
                        "num_clients": i,
                        "run_details": run_details,
                        "result": stuff.repr_json()
                    }            
                })
                save_json(file_name, json_out)
        else:
            print("output_r"+str(j)+".json already exists")

if __name__ == "__main__":
    main()
