from commons import *

import numpy as np
import matplotlib.pyplot as plt
import math

PARAM_partition_style = ["iid", "niid"]
PARAM_num_classes = [11, 21]
PARAM_num_clients = [2, 4, 8, 16, 32, 64, 128, 256]



def calculate_precision_recall_f1(confusion_matrix):
    confusion_matrix = np.array(confusion_matrix)
    precision = {}
    recall = {}
    f1_score = {}
    num_classes = confusion_matrix.shape[0]
    for i in range(num_classes):
        TP = confusion_matrix[i, i]
        FP = confusion_matrix[:, i].sum() - TP
        FN = confusion_matrix[i, :].sum() - TP
        precision[i] = float(TP / (TP + FP) if (TP + FP) > 0 else 0)
        recall[i] = float(TP / (TP + FN) if (TP + FN) > 0 else 0)
        if precision[i] + recall[i] > 0:
            f1_score[i] = float(2 * (precision[i] * recall[i]) / (precision[i] + recall[i]))
        else:
            f1_score[i] = 0.0
    return {"precision": precision, "recall": recall, "f1_score": f1_score}


f1_details_all = []
for starter in range(10):
    for partition_style in PARAM_partition_style:
        for num_classes in PARAM_num_classes:
            for num_clients in PARAM_num_clients:
                save_location = "fed_results"
                file_name = save_location+"/result"
                file_name += "_iteration_"+str(starter)
                file_name += "_partition_style_"+str(partition_style)
                file_name += "_num_classes_"+str(num_classes)
                file_name += "_num_clients_"+str(num_clients)
                file_name += ".json"

                save_file_name = "/"
                save_file_name += "_iteration_"+str(starter)
                save_file_name += "_partition_style_"+str(partition_style)
                save_file_name += "_num_classes_"+str(num_classes)
                save_file_name += "_num_clients_"+str(num_clients)
                save_file_name += ".png"

                try:
                    data = load_json(file_name)
                except:
                    continue
                    
                learning_round = 0

                raw_confusions = (data["result"]["History (metrics, centralized)"]["confusion"])
                confusion = {}
                for i in range(len(raw_confusions)):
                    confusion.update({raw_confusions[i][0]: raw_confusions[i][1]})

                f1_list = {
                    "f1": [],
                    "f1_macro": [],
                    "f1_weighted": [],
                    "f1_weighted_no_background": [],
                    "precision": [],
                    "recall": [],
                    "true_counts": [],
                    "pred_counts": [],
                    "confusions": [],
                    "loss": np.array(data["result"]["History (loss, centralized)"])[:,1].tolist()
                }
                for timestep in range(0,21):

                    confusion_0 = np.reshape(confusion[timestep], (int(math.sqrt(len(confusion[timestep]))),int(math.sqrt(len(confusion[timestep])))))

                    data_0 = calculate_precision_recall_f1(confusion_0)

                    precision = np.array(list(data_0["precision"].values()))
                    # print(precision)
                    recall = np.array(list(data_0["recall"].values()))
                    f1 = np.array(list(data_0["f1_score"].values()))
                    true_counts = np.sum(confusion_0, axis=1).tolist()
                    pred_counts = np.sum(confusion_0, axis=0).tolist()

                    f1_macro = np.mean(f1)
                    f1_weighted = np.sum(f1*true_counts)/np.sum(true_counts)
                    f1_weighted_no_background = np.sum(f1[1:]*true_counts[1:])/np.sum(true_counts[1:])
                    
                    all_data = np.array([precision, recall, f1, true_counts, pred_counts])
                    all_data = np.around(all_data, decimals=5)
                    # print(all_data.tolist())
                    f1_list["f1"].append(f1.tolist())
                    f1_list["f1_macro"].append(float(f1_macro))
                    f1_list["f1_weighted"].append(f1_weighted)
                    f1_list["f1_weighted_no_background"].append(f1_weighted_no_background)
                    f1_list["precision"].append(precision.tolist())
                    f1_list["recall"].append(recall.tolist())
                    f1_list["true_counts"].append(true_counts)
                    f1_list["pred_counts"].append(pred_counts)
                    f1_list["confusions"].append(confusion_0.tolist())

                    if timestep == 20:
                        print("#####################")
                        print("")
                        print(save_file_name[11:])
                        print("")
                        # print("Precision:", all_data[0].tolist())
                        # print("Recall:", all_data[1].tolist())
                        # print("F1-Score:", all_data[2].tolist())
                        # print("True Counts:", all_data[3])
                        # print("Predicted Counts:", all_data[4])
                        # print("")
                        print("Macro F1-Score:", round(f1_weighted,4))
                        print("Weighted F1-Score:", round(f1_weighted,4))
                        print("Weighted F1-Score (No Background):", round(f1_weighted_no_background,4))
                        print("")
                    
                        to_plot = np.array(confusion_0, dtype=float)

                        for jj in range(len(confusion_0)):
                            to_plot[jj] = to_plot[jj]/np.sum(to_plot[jj])
                        
                        plt.figure(figsize=(10,10), layout="constrained")

                        plt.imshow(to_plot, vmin=0, vmax=1)
                        plt.xticks(range(len(confusion_0)), ["Back", *range(1,len(confusion_0))])
                        plt.yticks(range(len(confusion_0)), ["Back", *range(1,len(confusion_0))])
                        plt.gca().invert_yaxis()
                        plt.xlabel("Predictions")
                        plt.ylabel("Truth")
                        plt.savefig("fed_confusion"+save_file_name)
                        plt.clf()

                plt.plot(f1_list["f1"], c="black", alpha=0.4)
                plt.plot(f1_list["f1_macro"], label="F1-Macro")
                plt.plot(f1_list["f1_weighted"], label="F1-Weighted")
                plt.plot(f1_list["f1_weighted_no_background"], label="F1-Weighted (No Background)")
                plt.legend()
                plt.ylim([0,1])
                plt.savefig("fed_learning"+save_file_name)
                plt.clf()
                
                f1_details_all.append({
                    "starter": starter,
                    "partition_style": partition_style,
                    "num_classes": num_classes,
                    "num_clients": num_clients,
                    "results": f1_list
                })

# print(f1_details_all)

save_json("all_results.json", f1_details_all)