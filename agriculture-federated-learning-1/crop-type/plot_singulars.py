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

def get_plots(data_results, file_name, data_type, non_iid=False):
    # Get accuracy data and average
    all_sets_loss_dist = []
    all_sets_loss_cent = []
    all_sets_acc_dist = []
    all_sets_acc_cent = []

    for all_data in data_results:

        li_loss_dist = []
        li_loss_cent = []
        li_acc_dist = []
        li_acc_cent = []

        for i in all_data.keys():

            
            data_loss_centralised = all_data[i]["result"]["History (loss, centralized)"]
            
            data_accuracy_centralised = all_data[i]["result"]["History (metrics, centralized)"]["accuracy"]

            try:
                data_loss_distributed = all_data[i]["result"]["History (loss, distributed)"]
                li_loss_dist.append(data_loss_distributed["rounds"])
                last_one = np.zeros_like(data_loss_distributed["rounds"])
                last_one[last_one == 0] = np.nan
            except:
                li_loss_dist.append(last_one.tolist())
            try:
                data_accuracy_distributed = all_data[i]["result"]["History (metrics, distributed, evaluate)"]["accuracy"]
                li_acc_dist.append(data_accuracy_distributed["rounds"])
                last_one2 = np.zeros_like(data_accuracy_distributed["rounds"])
                last_one2[last_one2 == 0] = np.nan
            except:
                li_acc_dist.append(last_one2.tolist())


            li_loss_cent.append([data_loss_centralised["start"], *data_loss_centralised["rounds"]])
            
            li_acc_cent.append([data_accuracy_centralised["start"], *data_accuracy_centralised["rounds"]])



        # If there arent the same number of rounds, delete most recent round
        if len(all_sets_loss_dist) > 0:
            if len(li_loss_dist) != len(all_sets_loss_dist[0]):
                break

        # Save most recent round
        all_sets_loss_dist.append(li_loss_dist)
        all_sets_loss_cent.append(li_loss_cent)
        all_sets_acc_dist.append(li_acc_dist)
        all_sets_acc_cent.append(li_acc_cent)

    # Convert to numpy arrays
    all_sets_loss_dist = np.array(all_sets_loss_dist)
    all_sets_loss_cent = np.array(all_sets_loss_cent)
    all_sets_acc_dist = np.array(all_sets_acc_dist)
    all_sets_acc_cent = np.array(all_sets_acc_cent)

    # Get length of dimension 1 of arrays, should all be same
    num_datasets = np.shape(all_sets_acc_cent)[0]

    # Flatten by mean dimension 1 of all arrays
    li_loss_dist = np.nanmean(all_sets_loss_dist, axis=0)
    li_loss_cent = np.nanmean(all_sets_loss_cent, axis=0)
    li_acc_dist = np.nanmean(all_sets_acc_dist, axis=0)
    li_acc_cent = np.nanmean(all_sets_acc_cent, axis=0)

    # Get all other data
    all_data = data_results[0]
    characteristics = []
    num_used = []
    for i in all_data.keys():
        try:
            num_used.append(int(i))
            try:
                characteristics.append(all_data[i]["run_details"])
            except:
                pass
        except:
            break
    # print(num_used)

    # size_dataset = []
    # if non_iid == True:
    #     for i in range(len(num_used)):
    #         size_dataset.append("")
    # elif len(characteristics) > 0:
    #     for i in range(len(characteristics)):
    #         size_dataset.append(int(0.95*characteristics[i]["raw_dataset"]["num_train"]/characteristics[i]["num_partitions"]))
    # else:
    #     for i in range(len(num_used)):
    #         size_dataset.append(int(0.95*4792/num_used[i]))

    # Plots
    fig =  plt.figure(figsize=(7,5),layout="constrained")
    cmap = plt.cm.jet
    norm = mpl.colors.LogNorm(vmin=1, vmax=np.amax(np.array(num_used)))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    for i in range(len(li_loss_dist)):
        lab = str(num_used[i])+" clients"
        plt.plot(np.arange(1,len(li_loss_dist[i])+1), li_loss_dist[i], color=cmap(norm(num_used[i])), label=lab)
    plt.xticks(np.arange(0,22,2))
    plt.xlabel("Number of aggregation rounds completed")
    plt.ylabel("Distributed Validation Loss")
    plt.legend(bbox_to_anchor=(1, 0.7))
    plt.title("Distributed Validation Loss by Number of Clients")
    plt.savefig(save_location+"/result_distributed_loss.png")
    plt.clf()
    plt.close()


    fig =  plt.figure(figsize=(7,5),layout="constrained")
    cmap = plt.cm.jet
    norm = mpl.colors.LogNorm(vmin=1, vmax=np.amax(np.array(num_used)))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    for i in range(len(li_loss_dist)):
        lab = str(num_used[i])+" clients"
        plt.plot(np.arange(1,len(li_loss_cent[i])+1), li_loss_cent[i], color=cmap(norm(num_used[i])), label=lab)
    plt.xticks(np.arange(0,22,2))
    plt.xlabel("Number of aggregation rounds completed")
    plt.ylabel("Centralised Testset Loss")
    plt.legend(bbox_to_anchor=(1, 0.7))
    plt.title("Centralised Testset Loss by Number of Clients")
    plt.savefig(save_location+"/result_centralised_loss.png")
    plt.clf()
    plt.close()

    fig =  plt.figure(figsize=(7,5),layout="constrained")
    cmap = plt.cm.jet
    norm = mpl.colors.LogNorm(vmin=1, vmax=np.amax(np.array(num_used)))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    for i in range(len(li_loss_dist)):
        lab = str(num_used[i])+" clients"
        plt.plot(np.arange(1,len(li_acc_dist[i])+1), li_acc_dist[i], color=cmap(norm(num_used[i])), label=lab)
    plt.xticks(np.arange(0,22,2))
    plt.xlabel("Number of aggregation rounds completed")
    plt.ylabel("Distributed Validation Accuracy")
    plt.legend(bbox_to_anchor=(1, 0.7))
    plt.title("Distributed Validation Accuracy by Number of Clients")
    plt.savefig(save_location+"/result_distributed_accuracy.png")
    plt.clf()
    plt.close()

    fig =  plt.figure(figsize=(7,5),layout="constrained")
    cmap = plt.cm.jet
    norm = mpl.colors.LogNorm(vmin=1, vmax=np.amax(np.array(num_used)))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    for i in range(len(li_loss_dist)):
        lab = str(num_used[i])+" clients"
        plt.plot(np.arange(1,len(li_acc_cent[i])+1), li_acc_cent[i], color=cmap(norm(num_used[i])), label=lab)
    plt.xticks(np.arange(0,22,2))
    plt.xlabel("Number of aggregation rounds completed")
    plt.ylabel("Centralised Testset Accuracy")
    plt.legend(bbox_to_anchor=(1, 0.7))
    plt.title("Centralised Testset Accuracy by Number of Clients")
    plt.savefig(save_location+"/result_centralised_accuracy.png")
    plt.clf()
    plt.close()

    # for i in range(len(li_loss_dist)):
    #     lab = str(num_used[i])+" clients with "+str(size_dataset[i])+" images each"
    #     # Plot distributed loss (Top Left)
    #     ax[0,0].plot(np.arange(1,len(li_loss_dist[i])+1), li_loss_dist[i], color=cmap(norm(num_used[i])), label=lab)
    #     # Plot centralised loss (Top Right)
    #     ax[0,1].plot(np.arange(len(li_loss_cent[i])), li_loss_cent[i], color=cmap(norm(num_used[i])))
    #     # Plot distrubted accuracy (Bottom Left)
    #     ax[1,0].plot(np.arange(1,len(li_acc_dist[i])+1), li_acc_dist[i], color=cmap(norm(num_used[i])))
    #     # Plot centralised accuracy (Bottom Right)
    #     ax[1,1].plot(np.arange(len(li_acc_cent[i])), li_acc_cent[i], color=cmap(norm(num_used[i])))

    # ax[0,0].set_xlim([0,len(li_loss_dist[0])])
    # ax[0,0].set_xticks(range(0,len(li_loss_dist[0])+1, 5))
    # ax[0,0].set_ylabel("Loss after round")
    # ax[0,0].set_title("Distributed Validation Loss")

    # ax[0,1].set_xlim([0,len(li_loss_cent[0])-1])
    # ax[0,1].set_xticks(range(0,len(li_loss_cent[0])+1, 5))
    # ax[0,1].set_ylabel("Loss after round")
    # ax[0,1].set_title("Centralised Testset Loss")

    # ax[1,0].set_xlim([0,len(li_acc_dist[0])])
    # ax[1,0].set_xticks(range(0,len(li_acc_dist[0])+1, 5))
    # ax[1,0].set_ylabel("Accuracy after round")
    # ax[1,0].set_title("Distributed Validation Accuracy")

    # ax[1,1].set_xlim([0,len(li_acc_cent[0])-1])
    # ax[1,1].set_xticks(range(0,len(li_acc_cent[0])+1, 5))
    # ax[1,1].set_ylabel("Accuracy after round")
    # ax[1,1].set_title("Centralised Testset Accuracy")

    # fig.suptitle("Accuracy of different number of clients training on "+data_type+" dataset", size=18)
    # fig.text(0.5, 0.15, "Number of aggregation rounds completed", horizontalalignment="center", size=16)
    # plt.figlegend(loc="lower center", bbox_to_anchor=(0.5, 0), ncol=3, fancybox=True, shadow=True)
    # fig.subplots_adjust(bottom=0.2)

    # fig.subplots_adjust(right=0.8)
    # cbar_ax = fig.add_axes([0.85, 0.2, 0.05, 0.68])
    # cbar = fig.colorbar(sm, cax=cbar_ax)#, ticks=[2,4,8,16,32,64,128,256])

    # # cbar.ax.set_yticklabels([])
    # plt.savefig(save_location+"/"+file_name)


if __name__ == "__main__":
    
    # Get input file paths and params.yml data
    file_location = os.path.dirname(os.path.abspath(__file__))
    save_location = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data-vm")
    if not os.path.exists(save_location):
        raise Exception("No data file exists")


    # extra_folder = "/100% taken"
    # data_results = []
    # for i in range(1,100):
    #     try:
    #         data_results.append(load_json(save_location+extra_folder+"/output_r"+str(i)+".json"))
    #     except:
    #         break
    # get_plots(data_results, "mnist_results.png","MNIST")


    extra_folder = "/iid"
    data_results = []
    for i in range(1,100):
        try:
            data_results.append(load_json(save_location+extra_folder+"/output_r"+str(i)+".json"))
        except:
            break
    get_plots(data_results, "crop_type_results.png","Crop Type")

    # extra_folder = "/non-iid-square"
    # data_results = []
    # for i in range(1,100):
    #     try:
    #         data_results.append(load_json(save_location+extra_folder+"/output_r"+str(i)+".json"))
    #     except:
    #         break
    # get_plots(data_results, "mnist_non_iid_square_results.png","NonIID-Square MNIST", non_iid=True)





# Data files 
# 4792 train
# 1198 test