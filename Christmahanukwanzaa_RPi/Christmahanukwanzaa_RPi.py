'''***************************************************
  Neo Pixel Christmahanukwanzaa Tree - Arduino Yun Version
    
  Light up a tree with all the colors of the holidays!
  Control the color, pattern, size, and speed of animation of a
  strip of neo pixels through a web page.
  
  See the Adafruit learning system guide for more details
  and usage information:
  
  Dependencies:
  - Neo Pixel Library
    https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel
  
  License:
 
  This example is copyright (c) 2013 Tony DiCola (tony@tonydicola.com)
  and is released under an open source MIT license.  See details at:
    http://opensource.org/licenses/MIT
  
  This code was adapted from Adafruit CC3000 library example 
  code which has the following license:
  
  Designed specifically to work with the Adafruit WiFi products:
  ----> https://www.adafruit.com/products/1469

  Adafruit invests time and resources providing this open source code, 
  please support Adafruit and open-source hardware by purchasing 
  products from Adafruit!

  Written by Limor Fried & Kevin Townsend for Adafruit Industries.  
  BSD license, all text above must be included in any redistribution
 ****************************************************
 Adaptation to CircuitPython for the Raspberry Pi is based on
 code from this example:
 https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/blob/master/examples/rpi_neopixel_simpletest.py
 Which has the following license:
 https://github.com/adafruit/Adafruit_CircuitPython_NeoPixel/blob/master/LICENSE
 ****************************************************'''
import time
import board
import neopixel
import socket
from collections import namedtuple

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 300

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False,
pixel_order=ORDER)

# Color scheme definitions.
Color = namedtuple('Color', ['red', 'green', 'blue'])
ColorScheme = namedtuple('ColorScheme', ['colors', 'count'])

rgbColors = [ Color(255, 0, 0), Color(0, 255, 0), Color(0, 0, 255) ]
rgb = ColorScheme(rgbColors, len(rgbColors))

christmasColors = [ Color(255, 0, 0), Color(0, 255, 0) ]
christmas = ColorScheme(christmasColors, len(christmasColors))

hanukkahColors = [ Color(0, 0, 255), Color(255, 255, 255) ]
hanukkah = ColorScheme(hanukkahColors, len(hanukkahColors))

kwanzaaColors = [ Color(255, 0, 0), Color(0, 0, 0), Color(0, 255, 0) ]
kwanzaa = ColorScheme(kwanzaaColors, len(kwanzaaColors))

rainbowColors = [ Color(255, 0, 0), Color(255, 128, 0), Color(255, 255, 0), Color(0, 255, 0), Color(0, 0, 255), Color(128, 0, 255), Color(255, 0, 255) ]
rainbow = ColorScheme(rainbowColors, len(rainbowColors))

incandescentColors = [ Color(255, 140, 20), Color(0, 0, 0) ]
incandescent = ColorScheme(incandescentColors, len(incandescentColors))

fireColors = [ Color(255, 0, 0), Color(255, 102, 0), Color(255, 192, 0) ]
fire = ColorScheme(fireColors, len(fireColors))

schemes = [ incandescent, rgb, christmas, hanukkah, kwanzaa, rainbow, fire ]

# Enumeration of possible pattern types
Pattern = ['BARS', 'GRADIENT']

# Bar width values (in number of pixels/lights) for different size options.
barWidthValues = [ 1,      # Small
                   3,      # Medium
                   6  ]   # Large

# Gradient width values (in number of gradient repetitions, i.e. more repetitions equals a smaller gradient) for different size options.
gradientWidthValues = [ 12,     # Small
                        6,      # Medium
                        2   ]  # Large

# Speed values in amount of milliseconds to move one pixel/light.  Zero means no movement.
speedValues = [ 0,       # None
                500,     # Slow
                250,     # Medium
                50   ]  # Fast

# Variables to hold current state.
currentScheme = 0
currentPattern = 0
currentWidth = 0
currentSpeed = 0
buffer = ''

# Setup the web server
addr = socket.getaddrinfo('localhost', 8080)

s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on ', addr)

# Main loop
while True:
    cl, addr = s.accept()
    print('client connected from ', addr)
    data = cl.recv(1024)
    if "GET /arduino" in data.decode():
        print('got it')
    response = (b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n')
    cl.sendall(response)
    cl.close()
    