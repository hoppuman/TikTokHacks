import sys
import re

def cleanFile():
	finalText = ""
	past_line = ""
	with open(sys.argv[1], "r") as a_file:
		for line in a_file:
			stripped_line = line.strip()
			if stripped_line == '(--- Line Object ---)' or stripped_line == '(--- Arc Object ---)':
				stripped_line = ""	
			pattern = r'N\d+ '
			stripped_line = re.sub(pattern, '', stripped_line )
			
			if(stripped_line == 'G01 Z -0' or stripped_line == 'G00 Z 0' or stripped_line == 'G00 Z 0' or stripped_line == 'G21' or stripped_line == 'G90'
			or stripped_line == '%'):
				stripped_line = ""
				
			pattern = r'Z -0'
			stripped_line = re.sub(pattern, '', stripped_line )
			
			pattern = r'X '
			stripped_line = re.sub(pattern, 'X', stripped_line )
			
			pattern = r'Y '
			stripped_line = re.sub(pattern, 'Y', stripped_line )
			
			pattern = r'J '
			stripped_line = re.sub(pattern, 'J', stripped_line )
			
			pattern = r'I '
			stripped_line = re.sub(pattern, 'I', stripped_line )

			stripped_line = stripped_line.strip()
			
			if(stripped_line[4:] == past_line[4:]):
				stripped_line = ""
			
			if(len(stripped_line) > 0):
				finalText += stripped_line
				finalText += '\n'
				past_line = stripped_line
				
		f = open(sys.argv[1][:-4] + "_clean.txt", "w+")
		f.write(finalText)
		f.close()

cleanFile()