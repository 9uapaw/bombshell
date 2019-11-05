import json
from typing import Iterable

from gui.general import BUTTON_SIZE
import PySimpleGUIQt as sg

WAYPOINT_META = ['grind', 'vendor', 'ghost']
WAYPOINT_FORMAT = ['circle', 'line']

waypoint_selector_frame = [sg.Frame('Waypoint',
                                    [[sg.Text('Waypoint type: '), sg.InputCombo(WAYPOINT_META, key='waypoint_meta', enable_events=True, size=(150, 30))],
                                     [sg.Text('Waypoint format: '), sg.InputCombo(WAYPOINT_FORMAT, key='waypoint_format', enable_events=True, size=(150, 30))]])]

waypoint_frame = [sg.Frame('Waypoint', [
    [sg.Text('Waypoint path: ', pad=(20, 20)), sg.InputText(key='save_waypoint'),
     sg.Button('Record waypoint', size=BUTTON_SIZE), sg.Button('Stop record', size=BUTTON_SIZE)],
    [sg.Text('Open waypoint'), sg.InputText(key='waypoint', enable_events=True), sg.FileBrowse(key='Browse', size=BUTTON_SIZE)],
])]

waypoints_loaded = {}
lines = {}
for meta in WAYPOINT_META:
    line = sg.Multiline()
    lines[meta] = line
    loaded = [sg.Frame(meta.capitalize(), [[line]])]
    waypoints_loaded[meta] = loaded

waypoint_loaded_frame = [sg.Frame('Loaded waypoints', waypoints_loaded.values())]

waypoint_layout_list = [waypoint_frame, waypoint_selector_frame, waypoint_loaded_frame]


def load_waypoints(path: str):

    def _format(waypoints: list):
        str = ""
        for wps in waypoints:
            for k, v in wps.items():
                str += "{}: {}\n".format(k, "\n".join(["({}, {})".format(x, y) for x, y in v]) if isinstance(v, list) else v)
            str += "--------------\n"

        return str

    with open(path) as f:
        waypoints = json.load(f)
        for meta, wp in waypoints.items():
            lines[meta].Update(_format(wp))
