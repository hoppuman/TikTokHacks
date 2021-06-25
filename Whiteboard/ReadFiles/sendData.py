import serial
from serial import Serial
import time

def sendManualInstruction():
	arduino.write("G1 X10 Y10 test Z200 ".encode())
	time.sleep(3)
	arduino.write("G1 X0 Y0 test Z200 ".encode())
	time.sleep(3)
	arduino.write("G1 X10 Y10 test Z200 ".encode())
	time.sleep(3)
	arduino.write("G1 X0 Y0 test Z200 ".encode())

def generateCommands(text):

	Lines = []

	for c in text:
		file = "letters/" + c + ".txt"
		### Sends the commands line by line, also doens't work ###
		file1 = open(file, 'r') 
		Lines.extend(file1.readlines())
		file1.close()
	
	return Lines
	
def generateCommandsFromFile(text):

	Lines = []

	file = text
	### Sends the commands line by line, also doens't work ###
	file1 = open(file, 'r') 
	Lines.extend(file1.readlines())
	file1.close()
	
	return Lines
	
	
def test():
	arduino = serial.Serial('com5', 9600)

	time.sleep(5)

	#with open('data.txt', 'r') as file:
	#	data = file.read()
	#	arduino.write(data.encode())	
	
	#Lines = generateCommands("ab")
	Lines = generateCommandsFromFile("as200_clean.txt")
	
	count = 0
	out = ''
	# let's wait one second before reading output (let's give device time to answer)
	time.sleep(0)
	doneReading = 0
	currentString = ""
	
	arduino.write(Lines[count].encode())
	count = count + 1

	while doneReading != 1:
		readBit = arduino.read(1)
		readBitString = readBit.decode("utf-8")
		currentString += readBitString
		if(readBit == b'j'):
			arduino.write(Lines[count].encode())
			count = count + 1
		if(readBit == b'q'):
			doneReading = 0
		elif(readBit == b'\n'):
			print(currentString.strip())
			currentString = ""
		
		
	if out != '':
		print(out)

test()
#sendManualInstruction()

print("done")


