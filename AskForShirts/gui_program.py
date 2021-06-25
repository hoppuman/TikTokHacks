import PySimpleGUI as sg

import os
import smtplib
import imghdr
from email.message import EmailMessage
import re
import time

EMAIL_ADDRESS = 'placeholder'
EMAIL_PASSWORD = 'placeholder'

def formatBody(collegeName):
    body = ""
    with open("Message.txt") as fp:
        for line in fp.readlines():
            if "[CollegeName]" in line:
                line = line.replace("[CollegeName]" , collegeName)
            body = body + line
    return body
    
def sendToTestEmail(email, password):
    collegeName = ""

    with open("test.txt") as fp:
        line = fp.readline() 
        linesplit = re.split(r'\t+', line)
        collegeName = linesplit[0]
    
    body = formatBody(collegeName)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, password)
        msg = EmailMessage()
        msg['Subject'] = 'Testing Shirt Script'
        msg['From'] = email
        msg.set_content(body)
        msg['To'] = email	
        smtp.send_message(msg)
        #print(body)

def startGUI():
    sg.theme('Reddit')

    layout = [[sg.Text(''), sg.Text(size=(40,3,), font=("Helvetica", 25), key='-OUTPUT-')],
            [sg.Text('Email:'), sg.Text(size=(15,1), key='-OUTPUT1-')],
            [sg.Input(key='-EMAIL-')],
            [sg.Text('Password:'), sg.Text(size=(15,1), key='-OUTPUT2-')],
            [sg.Input(key='-PASSWORD-')],
            [sg.Button('GO TIME'), sg.Button('Exit'), sg.Button('Test (Send To Myself)')]]

    window = sg.Window('Pattern 2B', layout)

    while True:  # Event Loop
        event, values = window.read()
        #print(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'GO TIME':
            email = values['-EMAIL-']
            password = values['-PASSWORD-']
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                #smtp.login(email, password)
                with open("colleges.txt") as fp:
                    line = fp.readline()
                    while(line):
                        linesplit = re.split(r'\t+', line)
                        body = formatBody(linesplit[0])
                        labelMessage = "Sent: " + linesplit[0]
                        window['-OUTPUT-'].update(labelMessage)
                        window.refresh()
                        #msg = EmailMessage()
                        #msg['Subject'] = 'Request From An Applicant'
                        #msg['From'] = EMAIL_ADDRESS
                        ##msg.set_content(body)
                        #msg['To'] = linesplit[1]
                        line = fp.readline()
                        print("Sent: " , linesplit[1].strip())
                        #smtp.send_message(msg)
                        time.sleep(.025)
        if event == "Test (Send To Myself)":
            email = values['-EMAIL-']
            password = values['-PASSWORD-']
            sendToTestEmail(email, password)
    
    window.close()

startGUI()