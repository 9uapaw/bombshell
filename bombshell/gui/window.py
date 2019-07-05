import io
import sys
import threading
from contextlib import redirect_stdout
from multiprocessing import Process

import PySimpleGUIQt as sg
from core.game_loop import GameLoop

sg.SetOptions(button_color=sg.COLOR_SYSTEM_DEFAULT)
# sg.ChangeLookAndFeel('GreenTan')

BUTTON_SIZE = (80, 20)

def run_window():
    debug_line = sg.Output(size=(400, 300))
    layout = [
        [sg.Text('Waypoint path: '), sg.InputText(key='waypoint'),
         sg.Button('Record', size=BUTTON_SIZE), sg.Button('Stop record', size=BUTTON_SIZE)],
        [sg.Text('Open waypoint'), sg.InputText(key='waypoint'), sg.FileBrowse(key='Browse', size=BUTTON_SIZE)],
        [debug_line],
        [sg.Button('Start bot', size=BUTTON_SIZE), sg.Cancel('Stop bot', size=BUTTON_SIZE)],
        [sg.CloseButton("Close", size=BUTTON_SIZE)]

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
        elif event == 'Stop record' or event == 'Stop bot':
            game_loop.screen.stop_capturing()
            t.join()


