import json

def clean_file_name(dirty):
    dirty = dirty.replace("_", " ")
    dirty = dirty.replace("-", " ")
    dirty = dirty.replace("(", " ")
    dirty = dirty.replace(")", " ")
    dirty = dirty.replace("/", " ")
    dirty = dirty.replace("*", " ")
    dirty = dirty.strip()
    dirty = dirty.replace("  ", "_")
    dirty = dirty.replace(" ", "_")
    dirty = dirty.replace("_", "")
    return dirty


def load_json(file_name):
    with open(file_name) as f:
        output = json.load(f)
    return output

def save_json(file_name, data):
    with open(file_name,'w') as f:
        json.dump(data, f)
