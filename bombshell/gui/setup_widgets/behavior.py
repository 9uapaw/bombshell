import json
from typing import List

import PySimpleGUIQt as sg
from PySimpleGUIQt import TABLE_SELECT_MODE_BROWSE, TABLE_SELECT_MODE_EXTENDED

from core.config import GlobalConfig
from game.behavior.map import UNIT, ATTRIBUTES, ACTIONS, OPERATORS, ATTR_VALUES
from gui.general import BUTTON_SIZE


BEHAVIOR_TYPES = ['grind', 'pull', 'non_combat']
LISTBOX_SIZE = (100, 100)


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


def create_frame(title: str, layout: list):
    return sg.Frame(title, [layout])


behavior_frame = sg.Frame('Behavior profile', [
    [sg.Text('Profile path: '), sg.InputText(key='behavior_save'),
     sg.Button('Save profile', size=BUTTON_SIZE, key='save_behavior')],
    [sg.Button('Load profile', size=BUTTON_SIZE, key='load_behavior', enable_events=True), sg.InputText(key='behavior'),
     sg.FileBrowse(key='behavior_browse', size=BUTTON_SIZE)],
], size=(300, 50))

behavior_tree_tabs = []

all_behavior = {}
for behavior_type in BEHAVIOR_TYPES:
    behavior_entry = {}
    behavior_entry['counter'] = Counter()
    behavior_entry['storage'] = BehaviorStorage()
    tree = sg.TreeData()
    behavior_tree = sg.Tree(data=tree,
                            headings=["st", "gg"],
                            auto_size_columns=True,
                            num_rows=10,
                            col0_width=100,
                            key='tree_' + behavior_type,
                            size=(400, 120),
                            select_mode=TABLE_SELECT_MODE_EXTENDED,
                            change_submits=True,

                            show_expanded=False,
                            enable_events=True)
    behavior_entry['tree'] = behavior_tree
    behavior_entry['tree_data'] = tree

    selected = sg.Listbox(values=[], key='selected_' + behavior_type, enable_events=True, disabled=True, size=(100, 70))
    behavior_entry['select'] = selected
    add_frame = [sg.Frame('Actions',
                          [[sg.Text('Parents: '), selected],
                          [sg.Button('Add', size=BUTTON_SIZE, key='add_behavior_' + behavior_type),
                           sg.Button('Remove', size=BUTTON_SIZE, key='remove_behavior_' + behavior_type)]], size=(300, 50))]
    behavior_table_frame = [sg.Frame(behavior_type.capitalize(), [[behavior_tree]])]
    behavior_tab = sg.Tab(behavior_type.capitalize(), [add_frame, behavior_table_frame], key=behavior_type)
    behavior_tree_tabs.append(behavior_tab)
    all_behavior[behavior_type] = behavior_entry

behavior_layout = [[behavior_frame], [sg.TabGroup([behavior_tree_tabs], key='behavior_tab', enable_events=True)]]


def convert_text(key: str, behavior: dict) -> str:
    return "[{}]: <if {}'s {} is {} than {} then {} {}>".format(key, behavior['unit'], behavior['attrs'],
                                                                behavior['ops'],
                                                                behavior['attr_value'], behavior['actions'],
                                                                behavior['action_value'])


def save_behavior(path: str):
    behaviors = {}
    for behavior_type in all_behavior.keys():
        behaviors[behavior_type] = all_behavior[behavior_type]['storage'].behaviors

    if not path:
        GlobalConfig.config.behavior = behaviors
    else:
        with open(path, 'w') as f:
            json.dump(behaviors, f)

    print('Saved behavior')


def load_behavior(path: str):
    with open(path) as f:
        profile = json.load(f)
        for behavior_type in profile:
            key = all_behavior[behavior_type]['counter']
            behavior_tree = all_behavior[behavior_type]['tree']
            storage = all_behavior[behavior_type]['storage']
            selected = all_behavior[behavior_type]['select']

            tree_data = sg.TreeData()
            keys = []

            for behavior in profile[behavior_type]:
                keys.append(behavior['key'])
                key.increment()

                for parent in behavior['parent']:
                    tree_data.Insert(parent, behavior['key'],
                                 convert_text(behavior['key'], behavior['behavior']), behavior)

            behavior_tree.Update(tree_data)
            storage.extend(profile[behavior_type])
            selected.Update(keys)

        GlobalConfig.config.behavior = profile


def behavior_window_handler(behavior_type: str, select: list):
    listbox_unit = sg.Listbox(list(UNIT.keys()), size=LISTBOX_SIZE, key='unit', enable_events=True)
    widgets = [create_frame('Unit', [listbox_unit]),
               create_frame('Attributes', [sg.Listbox([], key='attrs', enable_events=True, size=LISTBOX_SIZE)]),
               create_frame('Operations', [sg.Listbox([], key='ops', enable_events=True, size=LISTBOX_SIZE)]),
               create_frame('Attribute value', [sg.InputCombo([""], disabled=True, key="attr_value", size=(100, 20))]),
               create_frame('Actions', [sg.Listbox([], key='actions', enable_events=True, size=LISTBOX_SIZE)]),
               create_frame('Action value', [sg.InputText("0", disabled=True, key='action_value')]),
               create_frame('Action duration', [sg.InputText("0", disabled=True, key='action_duration')])]

    behavior_window = sg.Window("Add behavior", layout=[
        widgets
        , [sg.Button('Add', key='+_behavior', size=BUTTON_SIZE),
           sg.CloseButton('Close', key='Close_behavior', size=BUTTON_SIZE)]])
    behavior_window.Finalize()
    while True:
        event, values = behavior_window.Read()
        if event == '+_behavior':
            key = all_behavior[behavior_type]['counter']
            tree = all_behavior[behavior_type]['tree_data']
            behavior_tree = all_behavior[behavior_type]['tree']
            storage = all_behavior[behavior_type]['storage']
            selected = all_behavior[behavior_type]['select']

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
            attrs = values.get('attrs', None)
            if attrs:
                widgets[3].Rows[0][0].Update(values=ATTR_VALUES[attrs[0]], disabled=False)
                widgets[2].Rows[0][0].Update(list(OPERATORS[attrs[0]].keys()))

                widgets[4].Rows[0][0].Update(list(ACTIONS.keys()))
        elif event == 'actions':
            if values.get('actions', []):
                if values.get('actions', [''])[0] != 'do nothing':
                    widgets[5].Rows[0][0].Update(disabled=False)
                    widgets[6].Rows[0][0].Update(disabled=False)
                else:
                    widgets[5].Rows[0][0].Update(disabled=True)

    return
