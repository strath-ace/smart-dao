import numpy as np
import matplotlib.pyplot as plt

micro_std = 0.13859
macro_std = 0.1878

dataset_size = 5990

split_train = 0.7

number_clients = 128


dataset_train_per_client = (dataset_size*split_train)/number_clients

# print(dataset_train_per_client)

micro_dist = (np.random.normal(loc=dataset_train_per_client, scale=micro_std*dataset_train_per_client, size=(number_clients)))
macro_dist = (np.random.normal(loc=dataset_train_per_client, scale=macro_std*dataset_train_per_client, size=(number_clients)))

hist, _ = np.histogram(micro_dist, bins=20)
hist2, _ = np.histogram(macro_dist, bins=20)


plt.hist(micro_dist, bins=20, alpha=0.5, label="Micro Distribution")
plt.hist(macro_dist, bins=20, alpha=0.5, label="Macro Distribution")
plt.xlabel("Number of patches for the client")
plt.ylabel("How many of those clients with that dataset size exist")
ticker = np.arange(0, np.amax([hist, hist2]), 2)
plt.yticks(ticker)
plt.legend()
plt.savefig("test.png")

print(dataset_size*split_train)
print(np.sum(micro_dist))
print(np.sum(macro_dist))