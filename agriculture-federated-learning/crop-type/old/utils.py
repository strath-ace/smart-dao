import json


def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)
        
def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output