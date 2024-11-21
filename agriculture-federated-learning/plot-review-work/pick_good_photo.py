from datasets import load_dataset
import matplotlib.pyplot as plt
import numpy as np


from pathlib import Path
my_file = Path("images_model_pred")
if not my_file.is_dir():
    os.mkdir(my_file)


dataset = load_dataset("0x365/eo-crop-type-belgium", split="train").with_format("np")

dataset = dataset.select([5831,1198])

label_dataset = dataset["label"]#.numpy()






# Truth row 0 - small fields 10 classes
img = label_dataset[0].copy()
img[img > 10] = 0
np.save("images_model_pred/column_truth_row_0", img)

# Truth row 1 - big fields 10 classes
img = label_dataset[1].copy()
img[img > 10] = 0
np.save("images_model_pred/column_truth_row_1", img)

# Truth row 2 - small fields 20 classes
img = label_dataset[0].copy()
img[img > 20] = 0
np.save("images_model_pred/column_truth_row_2", img)

# Truth row 3 - big fields 10 classes
img = label_dataset[1].copy()
img[img > 20] = 0
np.save("images_model_pred/column_truth_row_3", img)
