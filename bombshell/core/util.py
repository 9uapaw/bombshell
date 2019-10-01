import json
import os
import sys

def load_from_file(path: str) -> dict:
    if '/' in path:
        if sys.platform == 'win32':
            work_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path.replace('/','\\'))
            with open(work_path) as f:
                return json.load(f)
        else:
            work_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
            with open(work_path) as f:
                return json.load(f)
    else:
        work_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), path)
        with open(work_path) as f:
            return json.load(f)
