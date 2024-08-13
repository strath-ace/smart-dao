import csv
import numpy as np

# Input
def csv_input(file_name):
    with open(file_name, "r") as f:
        read_obj = csv.reader(f)
        output = []
        for row in read_obj:
            output.append(row)
    f.close()
    return output

def csv_output(file_name, data_send):
    with open(file_name, "w") as f:
        if len(data_send) == 0:
            f.close()
            return
        else:
            for item in data_send:
                csv.writer(f).writerow(item)
            f.close()
            return

all_nuts = np.array(csv_input("output_data/Area_Arable land.csv"))[1:,0]

c = 0 
classified = []
for i in range(len(all_nuts)):
    if "Extra-Regio NUTS 2" in all_nuts[i]:
        c += 1
    else:
        if all_nuts[i] == "Piemonte":
            c += 1
        classified.append([all_nuts[i], c])

classified = np.array(classified)

# print(classified)

for i in range(c+1):
    print(classified[classified[:,1] == str(i),0])
    classified[classified[:,1] == str(i),1] = input("Enter country: ")
    print("--------------------")

csv_output("country_aligned.csv", classified)