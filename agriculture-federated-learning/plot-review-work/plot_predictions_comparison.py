from datasets import load_dataset
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from PIL import Image

file_path = 'path/to/your/file.txt'


file_paths = [
    {
        "file": "images_model_pred/column_truth_row_0.npy",
        "pos": [0,0],
        "title": "High class diversity small fields"
    },
    {
        "file": "images_model_pred/predictions_iteration_7_partition_style_iid_num_classes_11_num_clients_2.npy",
        "pos": [1,0],
        "item": 0
    },
    {
        "file": "images_model_pred/predictions_iteration_7_partition_style_iid_num_classes_11_num_clients_32.npy",
        "pos": [2,0],
        "item": 0
    },
    {
        "file": "images_model_pred/column_truth_row_1.npy",
        "pos": [0,1],
        "title": "Low class diversity large fields"
    },
    {
        "file": "images_model_pred/predictions_iteration_7_partition_style_iid_num_classes_11_num_clients_2.npy",
        "pos": [1,1],
        "item": 1
    },
    {
        "file": "images_model_pred/predictions_iteration_7_partition_style_iid_num_classes_11_num_clients_32.npy",
        "pos": [2,1],
        "item": 1
    },
    {
        "file": "images_model_pred/column_truth_row_2.npy",
        "pos": [0,2],
        "title": "High class diversity small fields"
    },
    {
        "file": "images_model_pred/predictions_iteration_7_partition_style_iid_num_classes_21_num_clients_2.npy",
        "pos": [1,2],
        "item": 0
    },
    {
        "file": "images_model_pred/predictions_iteration_7_partition_style_iid_num_classes_11_num_clients_32.npy",
        "pos": [2,2],
        "item": 0
    },
    {
        "file": "images_model_pred/column_truth_row_3.npy",
        "pos": [0,3],
        "title": "Low class diversity large fields"
    },
    {
        "file": "images_model_pred/predictions_iteration_7_partition_style_iid_num_classes_21_num_clients_2.npy",
        "pos": [1,3],
        "item": 1
    },
    {
        "file": "images_model_pred/predictions_iteration_7_partition_style_iid_num_classes_11_num_clients_32.npy",
        "pos": [2,3],
        "item": 1
    },
]


fig, axs = plt.subplots(3,4, figsize=(20,15))

for entry in file_paths:
    if os.path.exists(entry["file"]):
        img = np.array(np.load(entry["file"]), dtype=float).copy()
        x, y = entry["pos"]
        if "item" in entry.keys():
            img[img == 0] = np.nan
            img -= 1
            axs[x, y].imshow(img[entry["item"]], vmin=0, vmax=19, cmap="tab20c")
        else:
            img[img == 0] = np.nan
            img -= 1
            im = axs[x, y].imshow(img, vmin=0, vmax=19, cmap="tab20c")
        if "title" in entry.keys():
            axs[x,y].set_title(entry["title"])
    
    

axs = axs.flatten()
for ax in axs:
    ax.axis("off")

fig.text(0.023, 0.765, 'Truth', va='center', ha='center', fontsize=20, rotation=90)
fig.text(0.023, 0.482, 'Highest F1 Model Prediction', va='center', ha='center', fontsize=20, rotation=90)
fig.text(0.023, 0.199, 'Lowest F1 Model Prediction', va='center', ha='center', fontsize=20, rotation=90)

left_line_1 = Line2D([0.035, 0.035], [0.635, 0.895], color="black", linewidth=2, transform=fig.transFigure)
fig.add_artist(left_line_1)
left_line_2 = Line2D([0.035, 0.035], [0.352, 0.612], color="black", linewidth=2, transform=fig.transFigure)
fig.add_artist(left_line_2)
left_line_3 = Line2D([0.035, 0.035], [0.069, 0.329], color="black", linewidth=2, transform=fig.transFigure)
fig.add_artist(left_line_3)

top_line_1 = Line2D([0.048, 0.45], [0.915, 0.915], color="black", linewidth=2, transform=fig.transFigure)
fig.add_artist(top_line_1)
top_line_2 = Line2D([0.458, 0.86], [0.915, 0.915], color="black", linewidth=2, transform=fig.transFigure)
fig.add_artist(top_line_2)

fig.text(0.249, 0.93, '10 Class Models', va='center', ha="center", fontsize=20)
fig.text(0.659, 0.93, '20 Class Models', va='center', ha="center", fontsize=20)

plt.subplots_adjust(top=0.97, bottom=0, right=0.99, left=0.05)
plt.subplots_adjust(wspace=0.1, hspace=-0.3)

crop_types = np.array(["Background/Unclassified", "maize", "winter wheat", "potatoes", "fodder beets", "leguminous cover",    "winter barley", "pears", "appels", "beans", "engelwortel", "hemp", "cauliflower", "fodder carrots",    "other crops", "brussels sprouts", "triticale", "sjalots", "leek", "chicory", "peas", "fodder mixture", "spinach",    "parsnip", "strawberries", "cherry", "spring barley", "vegetables - seeds", "cucumber herb", "zucchini",    "winter rapeseed", "asparagus", "spring wheat", "fodder cabbages", "butternut", "sword herd", "haricot",    "winter rye", "grape seedlings", "ornamental plants", "other annual fruit", "buckwheat", "fodder turnips",    "tagetes", "blueberries", "fennel", "red berries", "raspberry", "other fodder crops", "aromatic herbs", "sorghum",    "soybeans", "yellow mustard", "tobacco", "walnuts", "barley", "spring rapeseed", "kiwi berries", "spring rye",    "plums", "chervil", "phacelia", "gooseberries", "hazelnuts", "sunflower", "Background/Unclassified"])
crop_nums = np.arange(len(crop_types))


cbar = fig.colorbar(im, ax=axs, fraction=0.12, pad=0.02, shrink=0.85)
tickers = np.linspace(0,19,21)+0.425
cbar.set_ticks(tickers[:-1])
crop_types = crop_types[crop_nums <= 20]
crop_types = crop_types[1:]
cbar.set_ticklabels(crop_types)
cbar.set_label('Class Crop Type', fontsize=20)
# plt.legend(handles=patches)

plt.suptitle("Predictions from Highest and Lowest F1-Score Models", fontsize=24)

plt.savefig("predictions.png")


plt.clf()






### Plot label image for unet model graphic

img = np.array(np.load("images_model_pred/column_truth_row_2.npy"), dtype=float)
img[img == 0] = np.nan
img -= 1

plt.figure(figsize=(10,10))

plt.imshow(img, vmin=0, vmax=19, cmap="tab20c")  # You can choose any colormap like 'gray', 'viridis', 'plasma', etc.
plt.axis('off')
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
plt.savefig("crop_type.jpg")