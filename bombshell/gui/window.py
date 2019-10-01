import threading

import PySimpleGUIQt as sg

from core.config import GlobalConfig
from core.game_loop import GameLoop
from core.logger import Logger
from core.util import load_from_file
from gui.general import general_layout, console, BUTTON_SIZE
from gui.setup import setup_layout
from gui.setup_widgets.behavior import behavior_window_handler, load_behavior, save_behavior
from gui.waypoint_widgets.waypoints import load_waypoints
from gui.waypoints import waypoint_layout

sg.SetOptions(button_color=sg.COLOR_SYSTEM_DEFAULT)


def run_window():

    layout = [[sg.TabGroup([[general_layout, setup_layout, waypoint_layout]])], [sg.CloseButton("Close", size=BUTTON_SIZE)]]

    window = sg.Window('Project BombShell', default_element_size=(40, 1)).Layout(layout).Finalize()
    paths = {}
    game_loop = None

    Logger.info("Loading global config file: global.json")
    GlobalConfig.load_from_file('global.json')
    global_conf = load_from_file('global.json')
    load_behavior(global_conf['behavior'])
    load_waypoints(global_conf['waypoint'])

    while True:
        event, values = window.Read()
        if event == 'Record waypoint':
            if not game_loop or not game_loop.screen.capturing:
                game_loop = GameLoop(GlobalConfig.config)
                record = threading.Thread(target=game_loop.record_waypoints, args=(paths,))
                Logger.info("Saving position {}".format(values['save_waypoint']))
                paths['waypoint'] = values['save_waypoint']
                paths['wp_type'] = values.get('waypoint_meta', 'grind')
                paths['wp_format'] = values.get('waypoint_format', 'circle')
                record.start()
        elif event == 'Start bot':
            if not game_loop or not game_loop.screen.capturing:
                Logger.info("Starting bot", True)

                game_loop = GameLoop(GlobalConfig.config)
                console.Update(value="")
                start = threading.Thread(target=game_loop.start)
                start.start()
        elif "add_behavior" in event:
            behavior_type = values.get('behavior_tab')
            behavior_window_handler(behavior_type, '' if not values.get('selected_' + behavior_type, '') else values.get('selected_' + behavior_type, ''))
        elif event == "waypoint":
            GlobalConfig.config.waypoint = load_from_file(values['waypoint'])
            load_waypoints(values['waypoint'])
            Logger.info("Waypoint loaded")
        elif event == 'load_behavior':
            load_behavior(values['behavior'])
        elif event == 'save_behavior':
            save_behavior(values['behavior_save'])
        elif event == 'Stop record':
            if game_loop:
                game_loop.screen.stop_capturing()
        elif event == 'Stop bot':
            if game_loop:
                game_loop.screen.stop_capturing()
        elif event == 'Close':
            return



