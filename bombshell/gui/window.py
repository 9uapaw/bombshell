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
    t = threading.Thread(target=game_loop.start, args=(paths, ))

    while True:
        event, values = window.Read()
        if event == 'Record':
            print(values['waypoint'])
            paths['waypoint'] = values['waypoint']
            game_loop.record_waypoints(paths['waypoint'])
        elif event == 'Start bot':
            paths['waypoint'] = values['waypoint']
            t.start()
        elif event == 'Stop record' or event == 'Stop bot':
            game_loop.screen.stop_capturing()
            t.join()


