import PySimpleGUIQt as sg

BUTTON_SIZE = (80, 20)
waypoint_frame = [sg.Frame('Waypoint', [
    [sg.Text('Waypoint path: ', pad=(20, 20)), sg.InputText(key='waypoint'),
     sg.Button('Record', size=BUTTON_SIZE), sg.Button('Stop record', size=BUTTON_SIZE)],
    [sg.Text('Open waypoint'), sg.InputText(key='waypoint'), sg.FileBrowse(key='Browse', size=BUTTON_SIZE)],
])]
general_layout = [
    waypoint_frame,
    [sg.Output(size=(400, 300))],
    [sg.Button('Start bot', size=BUTTON_SIZE), sg.Cancel('Stop bot', size=BUTTON_SIZE)],
    [sg.CloseButton("Close", size=BUTTON_SIZE)]

]


general_layout = [[sg.Tab('General', general_layout)]]
