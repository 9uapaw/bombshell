import PySimpleGUIQt as sg

from gui.setup_widgets.behavior import behavior_frame, behavior_table_frame

setup_layout = [
    behavior_frame,
    behavior_table_frame
]

setup_layout = sg.Tab('Setup', setup_layout)


def tree_node_handler(values: any):
    print(values)
