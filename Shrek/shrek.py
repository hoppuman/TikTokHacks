import time
import datetime

from bs4 import BeautifulSoup
import urllib

from pyautogui import press, typewrite, hotkey
import pyautogui

def SendScript():
	time.sleep(1)
	with open('script.txt') as f:
		lines = f.readlines()

	for line in lines:
		typewrite(line.strip())
		pyautogui.press('enter')

SendScript()