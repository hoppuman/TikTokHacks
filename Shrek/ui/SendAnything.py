import PySimpleGUI as sg
import time
import pyautogui

"""
	Allows you to "browse" through the Theme settings.  Click on one and you'll see a
	Popup window using the color scheme you chose.  It's a simple little program that also demonstrates
	how snappy a GUI can feel if you enable an element's events rather than waiting on a button click.
	In this program, as soon as a listbox entry is clicked, the read returns.
"""

sg.theme('Kayak')

texts = ['shrek.txt' , 'beemovie.txt','bible.txt']

layout = [[sg.Text('What do you want to send?')],
		  [sg.Text(size=(40,1), key='-OUTPUT-')],
		  [sg.Listbox(values=texts, size=(20, 12), key='-LIST-', enable_events=True)],
		  [sg.Button('Ok')],
		  [sg.Button('EXIT')],
		  [sg.Text('test'), sg.Text(size=(15,1), key='-COUNTDOWN-')]]

window = sg.Window('Theme Browser', layout)

def SendScript(filename: str):
	time.sleep(2)
	with open(filename) as f:
		lines = f.readlines()
	for line in lines:
		pyautogui.typewrite(line.strip())
		pyautogui.press('enter')

while True:  # Event Loop
	
	event, values = window.read()
	if event in (sg.WIN_CLOSED, 'EXIT'):
		break
	if event == 'Ok':
		window['-OUTPUT-'].update('Sending: ' + selected)
		SendScript(selected)
	else:
		selected = values['-LIST-'][0]
		window['-OUTPUT-'].update('You chose: ' + selected)
		

window.close()