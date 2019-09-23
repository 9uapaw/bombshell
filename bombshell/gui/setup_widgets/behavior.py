import json
from typing import List

import PySimpleGUIQt as sg
from PySimpleGUIQt import TABLE_SELECT_MODE_BROWSE, TABLE_SELECT_MODE_EXTENDED

from core.config import GlobalConfig
from game.behavior.map import UNIT, ATTRIBUTES, ACTIONS, OPERATORS
from gui.general import BUTTON_SIZE


class BehaviorStorage:

    def __init__(self):
        self.behaviors = []  # type: List[dict]

    def extend(self, behaviors: list):
        self.behaviors.extend(behaviors)

    def insert(self, parents: List[str], key: str, behavior: dict):
        self.behaviors.append({"parent": parents, "key": key, "behavior": behavior})


class Counter:

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1


key = Counter()
storage = BehaviorStorage()


def create_frame(title: str, layout: list):
    return sg.Frame(title, [layout])


LISTBOX_SIZE = (100, 100)

selected = sg.Listbox(values=[], key='selected', enable_events=True, disabled=True, size=(100, 70))

behavior_frame = [sg.Frame('Behavior profile', [
    [sg.Text('Profile path: '), sg.InputText(key='behavior_save'),
     sg.Button('Save profile', size=BUTTON_SIZE, key='save_behavior')],
    [sg.Button('Load profile', size=BUTTON_SIZE, key='load_behavior', enable_events=True), sg.InputText(key='behavior'),
     sg.FileBrowse(key='behavior_browse', size=BUTTON_SIZE)],
    [sg.Text('Parents: '), selected],
    [sg.Button('Add', size=BUTTON_SIZE, key='add_behavior'),
     sg.Button('Remove', size=BUTTON_SIZE, key='remove_behavior')],
])]

tree = sg.TreeData()

behavior_tree = sg.Tree(data=tree,
                        headings=["st"],
                        auto_size_columns=True,
                        num_rows=20,
                        col0_width=100,
                        key='tree',
                        size=(400, 300),
                        select_mode=TABLE_SELECT_MODE_EXTENDED,
                        change_submits=True,

                        show_expanded=False,
                        enable_events=True)
listbox_unit = sg.Listbox(list(UNIT.keys()), size=LISTBOX_SIZE, key='unit', enable_events=True)
listbox_empty_init = sg.Listbox([])
widgets = [create_frame('Unit', [listbox_unit]),
           create_frame('Attributes', [sg.Listbox([], key='attrs', enable_events=True, size=LISTBOX_SIZE)]),
           create_frame('Operations', [sg.Listbox([], key='ops', enable_events=True, size=LISTBOX_SIZE)]),
           create_frame('Attribute value', [sg.InputText("0", disabled=True, key="attr_value")]),
           create_frame('Actions', [sg.Listbox([], key='actions', enable_events=True, size=LISTBOX_SIZE)]),
           create_frame('Action value', [sg.InputText("0", disabled=True, key='action_value')])]
behavior_table_frame = [sg.Frame('Behaviors', [[behavior_tree]])]


def convert_text(key: str, behavior: dict) -> str:
    return "[{}]: <if {}'s {} is {} than {} then {} {}>".format(key, behavior['unit'], behavior['attrs'], behavior['ops'],
                                                        behavior['attr_value'], behavior['actions'],
                                                        behavior['action_value'])


def save_behavior(path: str):
    if not path:
        GlobalConfig.config.behavior['grind'] = storage.behaviors
    else:
        with open(path, 'w') as f:
            json.dump({'grind': storage.behaviors}, f)

    print('Saved behavior')


def load_behavior(path: str):
    with open(path) as f:
        profile = json.load(f)
        tree_data = sg.TreeData()
        keys = []

        for behavior in profile['grind']:
            keys.append(behavior['key'])
            key.increment()

            for parent in behavior['parent']:
                tree_data.Insert("" if parent == "0" else parent, behavior['key'],
                                 convert_text(behavior['key'], behavior['behavior']), behavior)

        behavior_tree.Update(tree_data)

        GlobalConfig.config.behavior = profile
        storage.extend(profile['grind'])
        selected.Update(keys)


def behavior_window_handler(select: list):
    behavior_window = sg.Window("Add behavior", layout=[
        widgets
        , [sg.Button('Add', key='+_behavior'),
           sg.CloseButton('Close', key='Close_behavior')]])
    behavior_window.Finalize()
    while True:
        event, values = behavior_window.Read()
        if event == '+_behavior':
            key.increment()
            new_values = {k: v[0] if not isinstance(v, str) else v for k, v in values.items() if v}

            if select:
                for i in select:
                    tree.Insert(i, str(key.count), convert_text(str(key.count), new_values), values)
            else:
                tree.Insert(select, str(key.count), convert_text(str(key.count), new_values), values)
            behavior_tree.Update(tree)

            parents = selected.Values
            parents.append(str(key.count))
            selected.Update(values=parents, disabled=False)

            storage.insert(select, str(key.count), new_values)
        elif event == 'Close_behavior':
            break
        elif event == 'unit':
            vals = list(ATTRIBUTES[values['unit'][0]].keys())
            widgets[1].Rows[0][0].Update(vals)
        elif event == 'attrs':
            if values.get('attrs', None):
                if values['attrs'][0] == 'is in combat':
                    widgets[3].Rows[0][0].Update(disabled=False)
                    widgets[2].Rows[0][0].Update(['EQUALS'])
                else:
                    widgets[3].Rows[0][0].Update(disabled=False)
                    widgets[2].Rows[0][0].Update(list(OPERATORS['int'].keys()))

                widgets[4].Rows[0][0].Update(list(ACTIONS.keys()))
        elif event == 'actions':
            if values.get('actions', [''])[0] != 'do nothing':
                widgets[5].Rows[0][0].Update(disabled=False)
            else:
                widgets[5].Rows[0][0].Update(disabled=True)

    return
