import json
import os
import sys
import time


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


def spin(amount: float):
    now = time.time()
    while time.time() - now <= amount:
        pass


class FixedList:

    def __init__(self, capacity: int):
        self._c = capacity
        self._truncate = capacity // 2
        self.data = []

    def append(self, o: any):
        if len(self.data) <= self._c:
            self.data.append(o)
        else:
            self.data = self.data[-self._truncate:]

    def last_n(self, n: int) -> list:
        return self.data[-n:]
