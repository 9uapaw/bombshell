import PySimpleGUIQt as sg

from gui.setup_widgets.behavior import behavior_frame, behavior_table_frame, behavior_tree_tabs, behavior_layout

setup_layout = sg.Tab('Behavior', behavior_layout)


def tree_node_handler(values: any):
    print(values)
