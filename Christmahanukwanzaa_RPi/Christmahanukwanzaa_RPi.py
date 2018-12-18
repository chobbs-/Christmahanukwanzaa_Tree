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
import random
from collections import namedtuple

# Start the timer
current_milli_time = lambda: int(round(time.time() * 1000))

# Note on MDNS: This should be handled by Raspbian. You should be able to hit
# <hostname>.local on your local network.

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 300

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.RGB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False,
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

classicColors = [ Color(255, 0, 0), Color(255, 128, 0), Color(0, 255, 0), Color(127, 0, 255), Color(0, 0, 255), Color(255, 0, 255) ]
classic = ColorScheme(classicColors, len(classicColors))

schemes = [ incandescent, rgb, christmas, hanukkah, kwanzaa, rainbow, fire, classic ]

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

# Chance of glitter values
glitter = [ 0,       # Off
            75,      # Some
            160,     # More
            255  ]   # TONS

# Variables to hold current state.
currentScheme = 0
currentPattern = 0
currentWidth = 0
currentSpeed = 0
currentGlitter = 0 

# Setup the web server
addr = socket.getaddrinfo('0.0.0.0', 80, socket.AF_INET)[0][-1]
print(addr)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(addr)
s.listen(1)
s.setblocking(0)

print('listening on ', addr)

# Ripped from simpleio because I couldnt get it installed. This works.
def map_range(x, in_min, in_max, out_min, out_max):
    """
    Maps a number from one range to another.
    Note: This implementation handles values < in_min differently than arduino's map function does.

    :return: Returns value mapped to new range
    :rtype: float
    """
    mapped = (x-in_min) * (out_max - out_min) / (in_max-in_min) + out_min
    if out_min <= out_max:
        return max(min(mapped, out_max), out_min)
    return min(max(mapped, out_max), out_min)

# Compute the color of a pixel at position i using a gradient of the color scheme.  
# This function is used internally by the gradient function.
def gradientColor(scheme, pixrange, gradRange, i):
    curRange = i // pixrange
    rangeIndex = i % pixrange
    colorIndex = rangeIndex // gradRange
    start = colorIndex
    end = colorIndex + 1
    if curRange % 2 != 0:
        start = (scheme.count - 1) - start
        end = (scheme.count -1) - end
    return Color(int(map_range(rangeIndex % gradRange, 0, gradRange, scheme.colors[start].red, scheme.colors[end].red)),
                 int(map_range(rangeIndex % gradRange, 0, gradRange, scheme.colors[start].green, scheme.colors[end].green)),
                 int(map_range(rangeIndex % gradRange, 0, gradRange, scheme.colors[start].blue, scheme.colors[end].blue)))

# Display a gradient of colors for the provided color scheme.
# Repeat is the number of repetitions of the gradient (pick a multiple of 2 for smooth looping of the gradient).
# SpeedMS is the number of milliseconds it takes for the gradient to move one pixel.  Set to zero for no animation.
def gradient(scheme, repeat = 1, speed = 1000):
    if scheme.count < 2:
        return

    pixrange = num_pixels // repeat + (num_pixels % repeat > 0)
    gradRange = pixrange // (scheme.count - 1) + (pixrange % (scheme.count -1) > 0)

    current_time = current_milli_time()
    offset = current_time // speed if speed > 0 else 0

    oldColor = gradientColor(scheme, pixrange, gradRange, (num_pixels-1)+offset)
    for i in range(num_pixels):
        currentColor = gradientColor(scheme, pixrange, gradRange, i+offset)
        if speed > 0:
            pixels[i] = (int(map_range(current_time % speed, 0, speed, oldColor.red, currentColor.red)),
                         int(map_range(current_time % speed, 0, speed, oldColor.green, currentColor.green)),
                         int(map_range(current_time % speed, 0, speed, oldColor.blue, currentColor.blue)))
        else:
            pixels[i] = (currentColor.red, currentColor.green, currentColor.blue)
        oldColor = currentColor
    pixels.show()
    return

def bars(scheme, width = 1, speed = 1000):
    maxSize = num_pixels / scheme.count
    if width > maxSize:
        return
    offset = current_milli_time() // speed if speed > 0 else 0

    for i in range(num_pixels):
        colorIndex = int(((i + offset) % (scheme.count * width)) // width)
        pixels[i] = (scheme.colors[colorIndex].red, scheme.colors[colorIndex].green, scheme.colors[colorIndex].blue)
    pixels.show()
    return

def addGlitter(chanceofGlitter):
    if random.randint(0, 255) < chanceofGlitter:
        pixels[random.randint(0, (num_pixels-1))] = (255, 255, 255)
        pixels.show()
    return

# Main loop
while True:
    try:
        cl, addr = s.accept()
    except: 
        pass
    else:
        print('client connected from ', addr)
        data = cl.recv(1024).decode()
        request = data.split('\n')[0]
        if "GET /arduino" not in request:
            cl.close()
            continue
        # Parse request uri
        key = request.split(' ')[1].split('/')[2]
        print(key)
        value = request.split(' ')[1].split('/')[3].split('?')[0]
        print(value)
        if key == 'scheme':
            currentScheme = int(value)
        elif key == 'pattern':
            currentPattern = int(value)
        elif key == 'width':
            currentWidth = int(value)
        elif key == 'speed':
            currentSpeed = int(value)
        elif key == 'glitter':
            currentGlitter = int(value)
        response = (b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n')
        cl.sendall(response)
        cl.close()
    
    # Update pixels based on current state
    if Pattern[currentPattern] == 'BARS':
        bars(schemes[currentScheme], barWidthValues[currentWidth], speedValues[currentSpeed])
    elif Pattern[currentPattern] == 'GRADIENT':
        gradient(schemes[currentScheme], gradientWidthValues[currentWidth], speedValues[currentSpeed])
    
    # Check to see if we should add some glitter!
    addGlitter(glitter[currentGlitter])
