# import PySimpleGUIQt as sg

BUTTON_SIZE = (100, 30)

console = sg.Output(size=(400, 300))
console.BackgroundColor = "#00000000"

general_layout = [
    [console],
    [sg.Button('Start bot', size=BUTTON_SIZE), sg.Cancel('Stop bot', size=BUTTON_SIZE)],
]

general_layout = sg.Tab('General', general_layout)
