#!/usr/bin/env python3
# rpi_ws281x library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from rpi_ws281x import *
import argparse
from flask import Flask

import _thread
import time
from flask import request

app = Flask(__name__)

# LED strip configuration:
LED_COUNT      = 600      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

def send_color(threadName, strip, color):
    #colorWipe(strip, Color(128, 206, 225))  # Pastel Blue
    #colorWipe(strip, Color(255, 209, 200))  # Pastel Blue
    colorWipe(strip, color)  # Pastel Blue

@app.route('/')
def hello():
    _thread.start_new_thread( send_color , ("Thread-1", strip,Color(), ))  
    return "Hello World!"

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        if(i - 30 > 0):
            strip.setPixelColor(i - 30, Color(0,0,0)) 
        #time.sleep(wait_ms/30000.0)
        strip.show()
    for i in range(strip.numPixels() - 30, strip.numPixels()):
        strip.setPixelColor(i, Color(0,0,0))
        time.sleep(wait_ms/30000.0)
        strip.show()

@app.route('/green')
def green():
    _thread.start_new_thread( send_color , ("Thread-1", strip,Color(155,105,180), ))  
    return "Hello World!"

@app.route('/blue')
def blue():
    _thread.start_new_thread( send_color , ("Thread-1", strip,Color(128, 206, 225), ))  
    return "Hello World!"

@app.route('/red')
def red():
    send_color("Thread-1", strip,Color(155,105,180))
    #_thread.start_new_thread( send_color , ("Thread-1", strip,Color(255,0,255), ))  
    return "Hello World!"

# Send a specific color in the form of a string
@app.route('/chooseColor', methods=['POST']) #POST requests
def chooseColor():
    red = request.form["red"]
    green = request.form['green']
    blue = request.form['blue']
    print(red, " " , green , " " , " " , blue)
    ChangeAllLEDToColor(strip, red, green, blue)
    return "true"

@app.route("/test", methods=["POST"])
def test():
    print(request.form["red"])
    return "true"

def ChangeAllLEDToColor(strip, red, green, blue):
    print("Changing colors")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(int(red), int(green), int(blue)))
    strip.show()

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    app.run(host='0.0.0.0')

