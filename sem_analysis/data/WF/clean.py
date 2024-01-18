import csv

data = []
with open("C:/Algorand/data/WF/combined.csv", "r") as f:
    csv_reader = csv.reader(f, delimiter=",")
    for row in csv_reader:
        data.append(row)

print(data)
for row in data:
    row[5] = row[5][0:10]+" "+row[5][11:]
    row[6] = row[6][0:10]+" "+row[6][11:]

csvwriter = csv.writer(open("C:/Algorand/data/WF/output.csv", "w", newline=""))
for row in data:
    csvwriter.writerow(row)