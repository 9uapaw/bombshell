import io
import sys
from contextlib import redirect_stdout

import PySimpleGUIQt as sg
from core.game_loop import GameLoop

sg.SetOptions(button_color=sg.COLOR_SYSTEM_DEFAULT)
sg.ChangeLookAndFeel('GreenTan')


def run_window():
    debug_line = sg.Multiline(key='Debug', do_not_clear=True)
    layout = [
        [sg.Text('Waypoint path: '), sg.InputText(key='waypoint'),
         sg.Button('Record'), sg.Button('Stop record')],
        [sg.Text('Open waypoint'), sg.InputText(key='waypoint'), sg.FileBrowse(key='Browse')],
        [sg.Button('Start bot'), sg.Cancel('Exit')],
        [debug_line]

    ]

    window = sg.Window('Everything bagel', default_element_size=(40, 1)).Layout(layout).Finalize()
    paths = {}
    game_loop = GameLoop()

    with io.StringIO() as buf:
        while True:
            debug_line.Update(value=buf.getvalue(), append=True)
            event, values = window.Read()
            if event == 'Record':
                print(values['waypoint'])
                paths['waypoint'] = values['waypoint']
                game_loop.record_waypoints(paths['waypoint'])
            elif event == 'Start bot':
                paths['waypoint'] = values['waypoint']
                game_loop.start(paths)
            elif event == 'Stop record':
                game_loop.screen.stop_capturing()


