import json
import pprint
from tabulate import tabulate
import numpy as np

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output


def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)


stats = load_json("images/model_stats.json")

big_temp = []
for i in range(len(stats["per_class"]["precision"])):
    temp = [i]
    for x in stats["per_class"].keys():
        temp.append(stats["per_class"][x][i])
    big_temp.append(temp)

print()
print("-------- Per Class --------")
print(tabulate(big_temp, headers=["Class" , *stats["per_class"].keys()], floatfmt=".5f"))
print()
print("---- Overall Scores ----")
print("F1 Macro:", "\t", round(stats["f1-macro"],5))
print("F1 Weighted:","\t", round(stats["f1-weighted"],5))
print("Accuracy:","\t", round(stats["accuracy"],5))