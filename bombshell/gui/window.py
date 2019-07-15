import io
import sys
import threading
from contextlib import redirect_stdout
from multiprocessing import Process

import PySimpleGUIQt as sg
from core.game_loop import GameLoop
from gui.general import general_layout

sg.SetOptions(button_color=sg.COLOR_SYSTEM_DEFAULT)
# sg.ChangeLookAndFeel('GreenTan')



def run_window():

    layout = [[sg.TabGroup(general_layout)]]
    window = sg.Window('Project BombShell', default_element_size=(40, 1)).Layout(layout).Finalize()
    paths = {}
    game_loop = GameLoop()
    start = threading.Thread(target=game_loop.start, args=(paths, ))
    record = threading.Thread(target=game_loop.record_waypoints, args=(paths, ))

    while True:
        event, values = window.Read()
        if event == 'Record':
            print(values['save_waypoint'])
            paths['waypoint'] = values['save_waypoint']
            record.start()
        elif event == 'Start bot':
            paths['waypoint'] = values['waypoint']
            start.start()
        elif event == 'Stop record':
            game_loop.screen.stop_capturing()
            record.join()
        elif event == 'Stop bot':
            game_loop.screen.stop_capturing()
            start.join()



