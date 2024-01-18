# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

import json
import os
from PyPDF2 import PdfReader

def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def clean_data(text):
    # Remove bad characters
    # Replaces new lines with £ symbol
    text = text.replace('\u0000', '')
    text = text.replace('!', '')
    text = text.replace('£', '$p')
    text = text.replace('\n\n\n', '£')
    text = text.replace('\n\n', '£')
    text = text.replace('\n', '£')
    text = text.replace('££', '£')
    return text

json_data = load_json("../local-data-path.json")
save_path = json_data["path"]+"/copernicus-data"

# Input location
path_pdf_dir = save_path+"/raw_data"
file_type = ".pdf"

# Output location
out_file_name = "/raw_pdf_data.json"
path_out_file = save_path+out_file_name



# Create todo list of files and names of files
pdf_file_name = []
path_pdf_list = []
for root, dirs, files in os.walk(path_pdf_dir):
    for file in files:
        if file[-4:] == file_type:
            file_name = root + "/" + file
            dir_name = os.path.dirname(file_name)[len(os.path.dirname(os.path.dirname(file_name))):]
            pdf_file_name.append(dir_name+"_"+file)
            path_pdf_list.append(file_name)

# Try load current output file to continue with
try:
    main_json = load_json(path_out_file)
except:
    main_json = []

# Get names of files already done
done_file_names = []
for i in range(len(main_json)):
    done_file_names.append(main_json[i]["file_name"])

# Remove done files from todo list
temp1 = []
temp2 = []
for i in range(len(pdf_file_name)):
    if pdf_file_name[i] not in done_file_names:
        temp1.append(pdf_file_name[i])
        temp2.append(path_pdf_list[i])
pdf_file_name = temp1
path_pdf_list = temp2


# Read PDFs
for i in range(len(pdf_file_name)):
    # Read PDFs and save in json to array
    reader = PdfReader(path_pdf_list[i])
    page = reader.pages[0]
    text = page.extract_text()
    text = clean_data(text)
    text_list = []
    j_0 = 0
    for j in range(len(text)):
        if text[j] == "£":
            if text[j_0:j] not in ["", "£", "££", "^", "^^"]:
                text_list.append(text[j_0:j])
                j_0 = j+1
    text_list.append(text[j_0:])
    main_json.append({
        "file_name": pdf_file_name[i],
        "text": text_list
    })
    # Print progress
    print(str(100*i/len(pdf_file_name))+"%")
    # Occasionally save data
    if i%100 == 0 and i>0:
        print("Saving")
        save_json(path_out_file, main_json)

# Save final array
save_json(path_out_file, main_json)
print("Done")