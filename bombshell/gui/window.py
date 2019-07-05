import io
import sys
import threading
from contextlib import redirect_stdout
from multiprocessing import Process

import PySimpleGUIQt as sg
from core.game_loop import GameLoop

sg.SetOptions(button_color=sg.COLOR_SYSTEM_DEFAULT)
sg.ChangeLookAndFeel('GreenTan')


def run_window():
    debug_line = sg.Output()
    layout = [
        [sg.Text('Waypoint path: '), sg.InputText(key='waypoint'),
         sg.Button('Record'), sg.Button('Stop record')],
        [sg.Text('Open waypoint'), sg.InputText(key='waypoint'), sg.FileBrowse(key='Browse')],
        [debug_line],
        [sg.Button('Start bot'), sg.Cancel('Stop bot')],
        [sg.CloseButton("Close")]

    ]

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
            # game_loop.start(paths)
        elif event == 'Stop record' or event == 'Stop bot':
            game_loop.screen.stop_capturing()
            t.join()


