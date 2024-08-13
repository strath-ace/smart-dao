import matplotlib as mpl
import matplotlib.pyplot as plt
import json
import os
import numpy as np
import yaml
import math

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output


# Get input file paths and params.yml data
file_location = os.path.dirname(os.path.abspath(__file__))
save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data-vm")
if not os.path.exists(save_location):
    raise Exception("No data file exists")

# with open(file_location+"/../params.yml", "r") as f:
#     params_config = yaml.load(f, Loader=yaml.SafeLoader)

open_files = ["/iid/output_r2.json"]


# Get all possible training iterations
data_results = []
for x in open_files:
    try:
        data_results.append(load_json(save_location+x))
    except:
        break

# Get accuracy data and average
temp_big_confusion = []

for all_data in data_results:

    temp_confusion = []

    for i in all_data.keys():
        set_val = all_data[i]["result"]["History (metrics, centralized)"]["big_confusion"]
        # for j in set_val:
        #     print(j)
        temp_confusion.append([j[1] for j in set_val])

    # If there arent the same number of rounds, delete most recent round
    if len(temp_big_confusion) > 0:
        if len(temp_big_confusion) != len(temp_confusion[0]):
            break

    # Save most recent round
    temp_big_confusion.append(temp_confusion)


# Convert to numpy arrays
temp_big_confusion = np.array(temp_big_confusion)

# Get length of dimension 1 of arrays, should all be same
num_datasets = np.shape(temp_big_confusion)[0]

# Flatten by mean dimension 1 of all arrays
confusion = np.mean(temp_big_confusion, axis=0)

# Get all other data
all_data = data_results[0]
characteristics = []
num_used = []
for i in all_data.keys():
    try:
        num_used.append(int(i))
    except:
        break

print(np.shape(confusion))
# print(confusion[0][-1]) # -1 is final aggregation round

num_clients = 0
agr_round = 19


confusion[:,:,0] = 202288074*confusion[:,:,0]
confusion[:,:,1] = 68096739*confusion[:,:,1]
confusion[:,:,2] = 50068391*confusion[:,:,2]
confusion[:,:,3] = 16664081*confusion[:,:,3]
confusion[:,:,4] = 14379282*confusion[:,:,4]
confusion[:,:,5] = 6565216*confusion[:,:,5]
confusion[:,:,6] = 4502781*confusion[:,:,6]
confusion[:,:,7] = 3933897*confusion[:,:,7]
confusion[:,:,8] = 2582060*confusion[:,:,8]
confusion[:,:,9] = 1488258*confusion[:,:,9]

for i in range(10):

    TP_1 = confusion[num_clients][agr_round][i][i]
    FP_1 = np.sum(np.delete(confusion[num_clients,agr_round,0,:],i))
    FN_1 = np.sum(np.delete(confusion[num_clients,agr_round,:,0],i))
    F1_score_1 = TP_1/(TP_1 + (0.5*(FP_1+FN_1)))
    print(F1_score_1)



# # The aggregation round in learning (-1) gives best
j = -1

# import imageio
images = []
for i in range(len(confusion)):
    plt.clf()
    plt.figure(figsize=(7,7))
    plt.imshow(confusion[i][j], vmin=0, vmax=np.amax(confusion), cmap="summer")
    for (j,ii),label in np.ndenumerate(confusion[i][j]):
        plt.text(ii,j,round(100*label,1),ha='center',va='center')
    
    plt.title(str(pow(2,i+1))+" clients")
    plt.savefig(save_location+"/confusion/matrix_for_"+str(pow(2,i+1))+"_clients.png")

#     images.append(imageio.imread(save_location+"/confusion/matrix_for_"+str(pow(2,i+1))+"_clients.png"))

# imageio.mimsave(save_location+"/confusion/movie.gif", images, loop=0, fps=1)


# Data files 
# 4792 train
# 1198 test
