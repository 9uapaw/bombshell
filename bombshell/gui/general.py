import PySimpleGUIQt as sg

BUTTON_SIZE = (100, 30)

waypoint_frame = [sg.Frame('Waypoint', [
    [sg.Text('Waypoint path: ', pad=(20, 20)), sg.InputText(key='save_waypoint'),
     sg.Button('Record waypoint', size=BUTTON_SIZE), sg.Button('Stop record', size=BUTTON_SIZE)],
    [sg.Text('Open waypoint'), sg.InputText(key='waypoint'), sg.FileBrowse(key='Browse', size=BUTTON_SIZE)],
])]

console = sg.Output(size=(400, 300))
console.BackgroundColor = "#00000000"

general_layout = [
    waypoint_frame,
    [console],
    [sg.Button('Start bot', size=BUTTON_SIZE), sg.Cancel('Stop bot', size=BUTTON_SIZE)],
]

general_layout = sg.Tab('General', general_layout)
