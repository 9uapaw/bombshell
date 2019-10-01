import json


def load_from_file(path: str) -> dict:
    with open(path) as f:
        return json.load(f)
