# 1 - Import
import PySimpleGUI as sg

# 2 - Layout
layout = [
            [sg.Text('What is your name'), sg.Input(key='-Name-')],
            [sg.Text('', key='-Output-')],
            [sg.Button('Ok', size=(6, 1)), sg.Button('Exit', size=(6, 1))]
]

# 3 - Window
window = sg.Window('First GUI window', layout, element_justification='center')

# 4 - Event loop handling
while True:
    event, values = window.read()
    # print(event, values)
    if event in ['Exit', sg.WIN_CLOSED]:
        break
    if event == 'Ok':
        window['-Output-'].update(f"Hello {values['-Name-']}!")

# 5 - Close
window.close()
