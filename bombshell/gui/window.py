import PySimpleGUIQt as sg
from core.game_loop import GameLoop

sg.SetOptions(button_color=sg.COLOR_SYSTEM_DEFAULT)
sg.ChangeLookAndFeel('GreenTan')


def run_window():
    layout = [
        [sg.Text('Waypoint path: '), sg.InputText(key='waypoint'),
         sg.Button('Record')],
        [sg.Text('Open waypoint'), sg.InputText(key='waypoint'), sg.FileBrowse(key='Browse')],
        [sg.Button('Start bot')]

    ]
    window = sg.Window('Everything bagel', default_element_size=(40, 1)).Layout(layout)
    paths = {}
    while True:
        event, values = window.Read()
        if event == 'Record':
            print(values['waypoint'])
            paths['waypoint'] = values['waypoint']
            game_loop = GameLoop()
            game_loop.record_waypoints(paths['waypoint'])
        elif event == 'Start bot':
            paths['waypoint'] = values['waypoint']
            game_loop = GameLoop()
            game_loop.start(paths)

