import requests
from bs4 import BeautifulSoup
import openpyxl
from datetime import date
from datetime import datetime
import os
import time

def printTodaysWeather():
    page = requests.get("https://weather.com/weather/today/l/601fac2e226280fb210240806f04cbc36f884bd3197f17e0ecb438b616466486")
    soup=BeautifulSoup(page.content,"html.parser")
    soup_condition=BeautifulSoup(page.content,"html.parser")

    today = date.today()
    # dd/mm/YY
    d1 = today.strftime("%m/%d/%Y")

    theFile = openpyxl.load_workbook('weather.xlsx')
    currentSheet = theFile['Sheet1']

    currentSheet['A2'].value = d1

    current_temperature = soup.find(class_="CurrentConditions--tempValue--3KcTQ").text

    current_state = soup_condition.find(class_="CurrentConditions--phraseValue--2xXSr").text
    print(current_state)

    emoji = ""

    if(current_state == "Cloudy"):
        emoji = '☁️'
    else:
        emoji = '☀️'

    currentSheet['A3'].value = current_temperature + emoji
    currentSheet['A4'].value = current_state

    print(current_temperature)

    description = soup.find(class_="CurrentConditions--precipValue--RBVJT").text
    description_concise = (description.split("through")[0])
    currentSheet['A5'].value = description_concise


    day_segments = ['Morning','Afternoon','Evening','Overnight']
    day_segments_counter = 0

    table=soup.find(class_="WeatherTable--columns--3q5Nx WeatherTable--wide--YogM9")
    print(len(table))
    for li in table.find_all('li'):
        if(day_segments_counter == 0):
            currentSheet['A7'].value = 'Morning:        ' + li.select_one("span[data-testid*=TemperatureValue]").text
        elif(day_segments_counter == 1):
            currentSheet['A8'].value = 'Afternoon:    ' + li.select_one("span[data-testid*=TemperatureValue]").text
        elif(day_segments_counter == 2):
            currentSheet['A9'].value = 'Evening:         ' + li.select_one("span[data-testid*=TemperatureValue]").text
        else:
            currentSheet['A10'].value = 'Night:             ' + li.select_one("span[data-testid*=TemperatureValue]").text
        day_segments_counter += 1

    theFile.save("weather.xlsx")
    time.sleep(1)
    os.startfile("weather.xlsx", "print")
    time.sleep(1)

while(True):
    now = datetime.now()
    timeOfDay = now.strftime("%H:%M:%S")
    #print("Current Time =", timeOfDay)
    # This is for 9am
    if(timeOfDay == '09:00:00'):
        printTodaysWeather()
    time.sleep(1)