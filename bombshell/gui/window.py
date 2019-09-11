import threading

import PySimpleGUIQt as sg
from core.game_loop import GameLoop
from gui.general import general_layout, console

sg.SetOptions(button_color=sg.COLOR_SYSTEM_DEFAULT)
# sg.ChangeLookAndFeel('GreenTan')


def run_window():

    layout = [[sg.TabGroup(general_layout)]]
    window = sg.Window('Project BombShell', default_element_size=(40, 1)).Layout(layout).Finalize()
    paths = {}
    game_loop = GameLoop()
    start = None
    record = None

    while True:
        event, values = window.Read()
        if event == 'Record':
            record = threading.Thread(target=game_loop.record_waypoints, args=(paths, ))
            print(values['save_waypoint'])
            paths['waypoint'] = values['save_waypoint']
            record.start()
        elif event == 'Start bot':
            console.Update(value="")
            start = threading.Thread(target=game_loop.start, args=(paths, ))
            paths['waypoint'] = values['waypoint']
            start.start()
        elif event == 'Stop record':
            game_loop.screen.stop_capturing()
        elif event == 'Stop bot':
            game_loop.screen.stop_capturing()
        elif event == 'Close':
            return



