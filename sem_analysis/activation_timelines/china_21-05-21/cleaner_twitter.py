import json
from bs4 import BeautifulSoup

def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def save_json(file_name, data):
    """
    Save json data to file
    """
    with open(file_name,'w') as f:
        json.dump(data, f)


words = ["earthquake", "china", "killed", "terremoto", "tsunami"]
json_out = {}
json_in = load_json("twitter_words1.json")
json_in2 = load_json("twitter_words2.json")
for i in range(len(json_in2)):
    json_in.append(json_in2[i])

for i in range(len(json_in)):
    code_list = []
    if json_in[i]["name"] in words:
        current_data = json_in[i]["data"]
        for ii in range(len(current_data)):
            code_list.append([current_data[ii]["x"], current_data[ii]["y"]])

        json_out.update({
            json_in[i]["name"]: code_list
        })

save_json("clean_twitter.json", json_out)

