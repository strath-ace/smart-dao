import matplotlib as mpl
import matplotlib.pyplot as plt
import json
import os
import numpy as np
import yaml

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output


# Get input file paths and params.yml data
file_location = os.path.dirname(os.path.abspath(__file__))
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data-vm")
if not os.path.exists(save_location):
    raise Exception("No data file exists")

with open(file_location+"/../params.yml", "r") as f:
    params_config = yaml.load(f, Loader=yaml.SafeLoader)


# Get all possible training iterations
data_results = []
for i in range(1,params_config["TRAINING_ITERATIONS"]+1):
    try:
        data_results.append(load_json(save_location+"/output_r"+str(i)+".json"))
    except:
        break

# Get accuracy data and average
all_sets = []
for all_data in data_results:
    round_data = []
    for i in all_data.keys():
        try:
            round_data.append(all_data[i]["result"]["History (metrics, distributed, evaluate)"]["accuracy"]["rounds"])
        except:
            break
    if len(all_sets) > 0:
        if len(round_data) != len(all_sets[0]):
            break
    all_sets.append(round_data)
all_sets = np.array(all_sets)
num_datasets = np.shape(all_sets)[0]
round_data = np.mean(all_sets, axis=0)


# Get all other data
all_data = data_results[0]
characteristics = []
num_used = []
for i in all_data.keys():
    try:
        num_used.append(int(i))
        characteristics.append(all_data[i]["run_details"])
    except:
        break


# Plots
fig,ax =  plt.subplots(figsize=(10,10))

cmap = plt.cm.jet
# norm = plt.Normalize(vmin=1, vmax=np.amax(np.array(num_used)))
norm = mpl.colors.LogNorm(vmin=1, vmax=np.amax(np.array(num_used)))

for i in range(len(round_data)):
    div = int(characteristics[i]["raw_dataset"]["num_train"]/characteristics[i]["num_partitions"])
    lab = str(num_used[i])+" clients with "+str(div)+" images each"
    plt.plot(np.arange(1,len(round_data[i])+1), round_data[i], color=cmap(norm(num_used[i])), label=lab)

plt.title("6000 images in dataset. Total images remains constant. Averaged over "+str(num_datasets)+" training iterations")
plt.suptitle("Accuracy of different number of clients training on MNIST dataset")
plt.xlabel("Number of learning rounds completed")
plt.xlim([1,30])
plt.ylabel("Accuracy after round")
plt.ylim([0,1])
plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25),
          ncol=3, fancybox=True, shadow=True)
fig.subplots_adjust(bottom=0.2)
plt.savefig(save_location+"/result.png")
