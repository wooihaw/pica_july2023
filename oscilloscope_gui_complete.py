import PySimpleGUI as sg
import pyvisa
from time import sleep


def send_command(instr, channel, vscale, voffset, tscale, tpos):
    instr.write(f':CHANnel{channel}:SCALe {vscale}')
    instr.write(f':CHANnel{channel}:OFFSet {voffset}V')
    instr.write(f':TIMebase:SCALe {tscale}')
    instr.write(f':TIMebase:POSition {tpos}')


rm = pyvisa.ResourceManager()
resources = rm.list_resources()

channels = tuple(range(1, 5))
vscales = ('100mV', '200mV', '500mV', '1V', '2V', '5V')
vscale_values = (0.1, 0.2, 0.5, 1.0, 2.0, 5.0)
tscales = ('50us', '100us', '200us', '500us', '1ms', '2ms', '5ms')
tscale_values = (50e-6, 100e-6, 200e-6, 500e-6, 1e-3, 2e-3, 5e-3)

text_size = (13, 1)
button_size = (6, 1)

layout = [  [sg.Text('Device', size=text_size), sg.Combo(resources, key='-device-', expand_x=True)],
            [sg.Text('Channel', size=text_size), sg.Combo(channels, default_value=channels[0], key='-channel-', expand_x=True)],
            [sg.Text('Vertical scale', size=text_size), sg.Combo(vscales, key='-vscale-', default_value=vscales[3], expand_x=True)],
            [sg.Text('Vertical Offset', size=text_size), sg.Slider(range=(-5.0, 5.0), default_value=0.0, resolution=0.1, orientation='h', key='-voffset-', expand_x=True)],
            [sg.Text('Timebase scale', size=text_size), sg.Combo(tscales, key='-tscale-', default_value=tscales[3], expand_x=True)],
            [sg.Text('Timebase position', size=text_size), sg.Slider(range=(-5.0, 5.0), default_value=0.0, resolution=0.1, orientation='h', key='-tpos-', expand_x=True)],
            [sg.Button('Connect', size=button_size), sg.Button('Send', size=button_size, disabled=True), sg.Button('Close', size=button_size)]
]

window = sg.Window('Oscilloscope', layout, element_justification='center')

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, 'Close'):
        break
    if event == 'Connect':
        try:
            mso = rm.open_resource(values['-device-'])
        except pyvisa.errors.VisaIOError:
            sg.popup_error('Instrument not found')
            continue
        else:    
            window['Send'].update(disabled=False)
    elif event == 'Send':
        # sg.Popup(   f"Channel: {values['-channel-']}",
        #             f"Vertical scale: {values['-vscale-']}",
        #             f"Vertical offset: {values['-voffset-']}",
        #             f"Timebase scale: {values['-tscale-']}",
        #             f"Timebase position: {values['-tpos-']}"
        # )

        channel = values["-channel-"]
        vscale = vscale_values[vscales.index(values['-vscale-'])]
        voffset = values["-voffset-"]
        tscale = tscale_values[tscales.index(values['-tscale-'])]
        tpos = tscale * values['-tpos-']
        window.perform_long_operation(lambda: send_command(mso, channel, vscale, voffset, tscale, tpos), "-command_sent-")
    elif event == '-command_sent-':
        sg.Popup("Command sent successfully")

if 'mso' in locals():
    mso.close()
    rm.close()

window.close()