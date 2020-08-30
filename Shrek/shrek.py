import time
import pyautogui
import sys

def SendScript(filename: str):
	time.sleep(2)
	with open(filename) as f:
		lines = f.readlines()
	for line in lines:
		pyautogui.typewrite(line.strip())
		pyautogui.press('enter')

if __name__ == "__main__":
	SendScript(sys.argv[1])
