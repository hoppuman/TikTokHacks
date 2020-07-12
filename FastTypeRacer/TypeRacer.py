from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import datetime

from bs4 import BeautifulSoup
import urllib

from pyautogui import press, typewrite, hotkey

def TypeRacerFill():
	baselink = "https://play.typeracer.com/"
	driver = webdriver.Chrome(executable_path="chromedriver.exe")
	driver.get(baselink)
	driver.implicitly_wait(5)
	enterRaceButton = driver.find_element_by_link_text("Practice").click()
	print("[2] Retrieving text ...")
	span = driver.find_elements_by_xpath("//span[@unselectable='on']")
	if len(span) == 2:
		full_text = span[0].text + " " + span[1].text
	else:
		full_text = span[0].text + span[1].text + " "+ span[2].text
	print(full_text)
	print("[3] Waiting for countdown ...4")
	time.sleep(1)
	print("[3] Waiting for countdown ...3")
	time.sleep(1)
	print("[3] Waiting for countdown ...2")
	time.sleep(1)
	print("[3] Waiting for countdown ...1")
	time.sleep(1)
	print("getting element by class name")

	typewrite(full_text, interval=0.05)

TypeRacerFill()