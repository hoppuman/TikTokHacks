import requests
import keyboard  # using module keyboard
import time
import socket

def run():
	while True:  
		if keyboard.is_pressed('q'):  # if key 'q' is pressed 
			sendNewColorToPi(254,254,0)
			print('You Pressed q Key!')
		if keyboard.is_pressed('w'):  # if key 'q' is pressed 
			sendNewColorToPi(0,255,0)
			print('You Pressed w Key!')
		if keyboard.is_pressed('e'):  # if key 'q' is pressed 
			sendNewColorToPi(0,0,255)
			print('You Pressed e Key!')

def sendNewColorToPi(red, green, blue):
	url = 'http://192.168.1.240:5000/chooseColor'
	dictToSend = {'red':red,'green':green, 'blue':blue}
	res = requests.post(url, data=dictToSend)

def testCall():
	url = 'http://192.168.1.240:5000/test'
	dictToSend = {'red':'red','blue':'blue','green':'green'}
	res = requests.post(url, data=dictToSend)
	
def testColorRanges():
	r = 0
	g = 0
	b = 255
	while(True):  
		if keyboard.is_pressed('q'):
			r = r + 5
			sendNewColorToPi(r,g,b)
			print(r)
			time.sleep(.25)
		if(r == 255):
			break
			
def testAllColors():
	r = 0
	g = 0
	b = 0
	speed = 10
	sensitivity = .10
	while(True):  
		if keyboard.is_pressed('q'):
			r = r + speed
			sendNewColorToPi(r,g,b)
			time.sleep(sensitivity)
			print("red: " , r, "green: ", g, "blue: " , b)
		if keyboard.is_pressed('w'):
			g = g + speed
			sendNewColorToPi(r,g,b)
			time.sleep(sensitivity)
			print("red: " , r, "green: ", g, "blue: " , b)
		if keyboard.is_pressed('e'):
			b = b + speed
			sendNewColorToPi(r,g,b)
			time.sleep(sensitivity)
			print("red: " , r, "green: ", g, "blue: " , b)
		if keyboard.is_pressed('a'):
			r = r - speed
			sendNewColorToPi(r,g,b)
			time.sleep(sensitivity)
			print("red: " , r, "green: ", g, "blue: " , b)
		if keyboard.is_pressed('s'):
			g = g - speed
			sendNewColorToPi(r,g,b)
			time.sleep(sensitivity)
			print("red: " , r, "green: ", g, "blue: " , b)
		if keyboard.is_pressed('d'):
			b = b - speed
			sendNewColorToPi(r,g,b)
			time.sleep(sensitivity)
			print("red: " , r, "green: ", g, "blue: " , b)	
		
		if(r == 255):
			break
	
def readToken():
	with open('actual_token.txt') as f:
		lines = f.readlines()
		# return my token
		return lines[0]

def readTwitchChat():
	
	sock = socket.socket()

	server = 'irc.chat.twitch.tv'
	port = 6667
	nickname = 'hoppuman2'
	token = readToken()
	channel = '#hoppuman2'

	sock.connect((server, port))
	sock.send(f"PASS {token}\n".encode('utf-8'))
	sock.send(f"NICK {nickname}\n".encode('utf-8'))
	sock.send(f"JOIN {channel}\n".encode('utf-8'))

	# !color 255,0,0
	while(True):
		try:
			resp = sock.recv(2048).decode('utf-8')
			chatParts = resp.split(":")
			message = chatParts[2]
			rgb = ""
			if(message.startswith('!color')):
				color = message.split(" ")[1]
				colorSplit = color.split(",")
				red = colorSplit[0]
				green = colorSplit[1]
				blue = colorSplit[2]
				sendNewColorToPi(red,green,blue)
				print("red: " , red, "green: " , green, "blue: " , blue)
		except:
			print("no second message")

		#print(resp)


	sock.close()


testAllColors()

#testAllColors()