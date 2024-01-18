# ---------- Copyright (C) 2024 University of Strathclyde and Author ---------
# ------------------------- Author: Robert Cowlishaw -------------------------
# -------------- e-mail: robert.cowlishaw.2017@uni.strath.ac.uk --------------

from PyPDF2 import PdfReader
import json
import os


def check_int(input):
    """
    Check if input string is a integer
    """

    try:
        int(input)
        is_int = 1
    except:
        is_int = 0
    return is_int


def save_json(file_name, data):
    """
    Save json data to file
    """
    with open(file_name,'w') as f:
        json.dump(data, f)

 
def get_data(pdf, json_name):
    """
    Converts desired pdf info to json format
    """

    # Convert pdf to string
    reader = PdfReader(pdf)
    page = reader.pages[0]
    text = page.extract_text()

    # Remove bad characters
    text_out = []
    text_temp = []
    for i in range(len(text)):
        if text[i] not in ["!", " "] and text[i:i+1] not in ["\n"]:
            text_temp.append(text[i])
        if text[i:i+1] == "\n":
            if len(text_temp) != 0:
                text_out.append("".join(text_temp))
                text_temp = []

    # Search for specific info
    pre_event = []
    post_event = []
    for text in text_out:
        if text[0:32] == "https://emergency.copernicus.eu/" and check_int(text[-3:]):  # Check for activation id
            active_id = text[-3:]
        elif text[0:2] == "km" and not check_int(text[-3:]) and text[-3:] != "N/A":  #  Check for title
            title = text[2:]
        elif text[0:13] == "Mapproducedby":
            map_maker = text[13:]
        elif text[0:18] == "EventSituationasof":
            dates_1 = text[18:]
        elif text[0:23] == "ActivationMapproduction":
            dates_2 = text[23:]
        elif text[0:15] == "Pre-eventimage:":
            for i in range(len(text)):
                if text[i] == "(":
                    pre_event.append(text[:i])
                    break
        elif text[0:16] == "Post-eventimage:":
            for i in range(len(text)):
                if text[i] == "(":
                    post_event.append(text[:i])
                    break

    # Make json output
    json = {
        "json_name": json_name,
        "active_id": active_id,
        "title": title,
        "map_maker": map_maker,
        "dates_1": dates_1,
        "dates_2": dates_2,
        "pre_event": pre_event,
        "post_event": post_event
    }
    return json


## Main Script


# Get all pdf file paths
pdf_files = []
pdf_folders = os.listdir(os.path.join(os.path.expanduser('~'), "local-data", "all-copernicus-ems"))
for dir in pdf_folders:
    files = os.listdir(os.path.join(os.path.expanduser('~'), "local-data", "all-copernicus-ems", dir))
    for fil in files:
        pdf_files.append([dir, fil])


output = []
counter = 0
for pdf in pdf_files:
    # Counters
    counter += 1
    print(str(100*counter/len(pdf_files)),"% done")
    
    try:
        # Try get pdf data as json
        path = os.path.join(os.path.expanduser('~'), "local-data", "all-copernicus-ems", pdf[0], pdf[1])
        output.append(get_data(path, pdf[0]+"_"+pdf[1]))
    except:
        # Except show what pdf file fails
        print(pdf, "BAD")

# Save json to output json file
save_json("output.json", output)



# Notes
# Add info to json
# old_json.update(new_info)