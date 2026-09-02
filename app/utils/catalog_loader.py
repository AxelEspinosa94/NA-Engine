import json

def load_catalog(path):
    """
    Load the method catalog from a JSON file.
    """
    with open(path, "r", encoding="utf-8") as f:
        catalog = json.load(f)
    return catalog
