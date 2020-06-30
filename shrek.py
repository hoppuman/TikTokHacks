from time import sleep
from pyautogui import typewrite, press
from keyboard import is_pressed

def SendScript():
    sleep(2)
    with open('script.txt') as f:
        lines = f.readlines()
    for line in lines:
        if is_pressed('F2'):
            print("Fail safe triggered aborting.")
            exit()
        typewrite(line.strip())
        press('enter')
SendScript()