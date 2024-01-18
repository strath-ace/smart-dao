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

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

 
def get_data(pdf, json_name):
    """
    Converts desired pdf info to json format
    """

    # Convert pdf to string
    reader = PdfReader(pdf)
    page = reader.pages[0]
    text = page.extract_text()

    # Remove bad characters
    text = text.replace('\u0000', '')
    text = text.replace('!', '')
    text = text.replace('-', '/')
    text = text.replace('\n\n\n', '-')
    text = text.replace('\n\n', '-')
    text = text.replace('\n', '-')
    text = text.replace('--', '-')

    # Make json output
    json = {
        json_name: text,
    }
    return json


## Main Script

json_data = load_json("../local-data-path.json")
save_path = json_data["path"]

save_file_name = "/eq_indonesia_social_media.txt"

pdf_location = save_path+"/pdfs"

# Try get pdf files
try:
    # Get all pdf file paths
    pdf_files = []
    pdf_folders = os.listdir(pdf_location)
    for dir in pdf_folders:
        files = os.listdir(pdf_location+dir)
        for fil in files:
            pdf_files.append([dir, fil])
except:
    print("PDF files not in correct location")
    print(pdf_location)

pdf_names = []
for pdf in pdf_files:
    pdf_names.append(pdf[0]+"_"+pdf[1])

# Try load currently stored data
try:
    main_json = load_json("all_text.json")
except:
    main_json = {}

# Try update currently stored pdf names list
try:
    main_json['all_files'].update(pdf_names)
except:
    main_json.update({'all_files': pdf_names})

counter = 0
for pdf in pdf_files:
    # Counters
    counter += 1

    print(str(100*counter/len(pdf_files)),"% done")
    json_name = pdf[0]+"_"+pdf[1]
    
    try:
        if len(main_json[json_name]) > 0:
            continue
        else:
            print("Zero Length on", json_name)
            raise Exception("Zero Length on", json_name)
    except:
        try:
            # Try get pdf data as json
            path = os.path.join(os.path.expanduser('~'), "local-data", "all-copernicus-ems", pdf[0], pdf[1])
            main_json.update(get_data(path, json_name))
        except:
            # Except show what pdf file fails
            print(pdf, "BAD")

    if counter % 100 == 0:
        print("Saving...")
        try:
            save_json("all_text.json", main_json)
            print("Saved")
        except:
            print("Not saved?")

# Save json to output json file
print("Saving...")
save_json("all_text.json", main_json)
print("Saved")

for i in range(5):
    print()


c_good = 0
c_bad = 0
c_empty = 0
for x in main_json['all_files']:
    try:
        if len(main_json[x]) > 0:
            c_good += 1
        else:
            c_empty += 1
    except:
        c_bad += 1

print("Checks:")
print("Total number of files", len(main_json['all_files']))
print("Good info files", c_good, "/", len(main_json['all_files']))
print("Empty info files", c_empty, "/", len(main_json['all_files']))
print("Missing info files", c_bad, "/", len(main_json['all_files']))
