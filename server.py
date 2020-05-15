#!/usr/bin/env python

import spidev
import os
import json
import unicornhat
import threading
import glob
import colorsys
from time import sleep
from datetime import datetime
from gpiozero import CPUTemperature
from unicornhatmini import UnicornHATMini

from flask import Flask, jsonify, make_response, request
from random import randint

blinkThread = None
globalRed = 0
globalGreen = 0
globalBlue = 0
globalLastCalled = None
globalLastCalledApi = None

try:
        spidev.SpiDev(0,0)
        unicornmini=True
except FileNotFoundError:
        unicornmini=False

class UnicornWrapper:
    def __init__(self, hat = None):
        if hat == 'phat':
            self.hat = unicornhat
            self.type = hat
            self.hat.set_layout(unicornhat.PHAT)
            self.hat.brightness(0.5)
        elif hat == 'mini':
            self.hat = UnicornHATMini()
            self.type = hat
            self.hat.set_brightness(0.5)
            self.hat.set_rotation(90)
        else:
            self.hat = None
            self.type = 'none'
        self.brightness = 0.5
        self.rotation = 0
    def get_type(self):
        return self.type

    def get_hat(self):
        return self.hat

    def clear(self):
        return self.hat.clear()

    def get_shape(self):
        return self.hat.get_shape()

    def set_all(self, r, g, b):
        self.hat.set_all(r, g, b)

    def get_brightness(self):
        if self.type == 'phat':
            return self.hat.get_brightness()
        
        return self.brightness
    
    def set_brightness(self, brightness):
        self.brightness = brightness

        if self.type == 'phat':
            self.hat.brightness(brightness)
        elif self.type == 'mini':
            self.hat.set_brightness(brightness)
    
    def set_pixel(self, x, y, r, g, b):
        self.hat.set_pixel(x, y, r, g, b)
    
    def set_rotation(self, r=0):
        if self.type == 'phat':
            self.hat.rotation(r)
        elif self.type == 'mini':
            self.hat.set_rotation(r)
        self.rotation = r
    
    def get_rotation(self):
        return self.rotation
    
    def show(self):
        self.hat.show()

    def off(self):
        self.hat.clear()
        self.hat.show()

if unicornmini:
        unicorn = UnicornWrapper('mini')
else:
        unicorn = UnicornWrapper('phat')

#get the width and height of the hardware and set it to portrait if its not
width, height = unicorn.get_shape()

app = Flask(__name__)

def validateJson(j):
        if j['size']['height'] != height:
                return False, f"Height is wrong, expected: {height} got: {j['size']['height']}"
        if j['size']['width'] != width:
                return False, f"Height is wrong, expected: {width} got: {j['size']['width']}"
        if len(j['pixels']) != height:
                return False, "Parsing json found wrong number of rows"
        for x in range(len(j['pixels'])):
                if len(j['pixels'][x]) != width:
                        return False, f"Parsing json found wrong number of columns in row {x+1}"
        return True, ''

def setPixels(jsonObj, r, g, b, brightness):
        global crntColors, globalIcon, globalBlue, globalGreen, globalRed
        globalRed = r
        globalGreen = g
        globalBlue = b
        if brightness != '' :
                unicorn.set_brightness(brightness)
        if jsonObj != '':
                globalIcon = jsonObj['name']
                for x in range(width):
                        for y in range(height):
                                pixel = jsonObj['pixels'][y][x]
                                if pixel['red'] == -1:
                                        red = r
                                else:
                                        red = pixel['red']
                                if pixel['green'] == -1:
                                        green = g
                                else:
                                        green = pixel['green']
                                if pixel['blue'] == -1:
                                        blue = b
                                else:
                                        blue = pixel['blue']
                                unicorn.set_pixel(x, y, red, green, blue)
        else:
                globalIcon="none"
                for x in range(width):
                        for y in range(height):
                                unicorn.set_pixel(x, y, r, g, b)

def setDisplay(jsonObj, r, g, b, brightness = 0.5, speed = None):
	setPixels(jsonObj, r, g, b, brightness)
	unicorn.show()

	if speed != None and speed != '' :
		sleep(speed)
		unicorn.clear()
		crntT = threading.currentThread()
		while getattr(crntT, "do_run", True) :
			setPixels(jsonObj, r, g, b, brightness)
			unicorn.show()
			sleep(speed)
			unicorn.clear()
			unicorn.show()
			sleep(speed)

def halfBlink():
        unicorn.show()
        sleep(0.8)
        unicorn.clear()
        unicorn.show()
        sleep(0.2)   

def countDown(time):
        zero = getIcon('0')
        one = getIcon('1')
        two = getIcon('2')
        three = getIcon('3')
        four = getIcon('4')
        five = getIcon('5')
        six = getIcon('6')
        seven = getIcon('7')
        eight = getIcon('8')
        nine = getIcon('9')
        jsonObj = getIcon('arrow-down')
        showTime = time - 10
        while(showTime > 0):
                setPixels(jsonObj, 255, 255, 0, 0.5)
                unicorn.show()
                sleep(1)
                unicorn.clear()
                unicorn.show()
                sleep(1)
                showTime = showTime - 2
        setPixels(nine, 255, 255, 0, 0.5)
        halfBlink()
        setPixels(eight, 255, 255, 0, 0.5)
        halfBlink()
        setPixels(seven, 255, 255, 0, 0.5)
        halfBlink()
        setPixels(six, 255, 255, 0, 0.5)
        halfBlink()
        setPixels(five, 255, 255, 0, 0.5)
        halfBlink()
        setPixels(four, 255, 255, 0, 0.5)
        halfBlink()
        setPixels(three, 255, 255, 0, 0.5)
        halfBlink()
        setPixels(two, 255, 255, 0, 0.5)
        halfBlink()
        setPixels(one, 255, 255, 0, 0.5)
        halfBlink()
        setPixels(zero, 255, 255, 0, 0.5)
        halfBlink()
        setDisplay('', 255, 0, 0, 0.5, 1)
        halfBlink()
        unicorn.clear()
        unicorn.off()

def getIcon(icon):
        try:
                f = open(f"./icons/{unicorn.get_type()}/{icon}.json", "r")
                return json.loads(f.read())
        except ValueError:
                return False
        except IOError:
                return False

def switchOn() :
	red = randint(10, 255)
	green = randint(10, 255)
	blue = randint(10, 255)
	blinkThread = threading.Thread(target=setDisplay, args=('', red, green, blue, '', ''))
	blinkThread.do_run = True
	blinkThread.start()

def switchOff() :
	global blinkThread, globalBlue, globalGreen, globalRed
	globalRed = 0
	globalGreen = 0
	globalBlue = 0
	if blinkThread != None :
		blinkThread.do_run = False
	unicorn.clear()
	unicorn.off()

def shutdownPi() :
        global blinkThread
        blinkThread = threading.Thread(target=countDown, args=(60,))
        blinkThread.do_run = True
        blinkThread.start()
        os.system("shutdown +1 'Shutdown trigger via API... Shutting down in 2 minute'")

def setTimestamp() :
	global globalLastCalled
	globalLastCalled = datetime.now()

def set

# API Initialization
@app.route('/api/on', methods=['GET'])
def apiOn() :
	global globalLastCalledApi
	globalLastCalledApi = '/api/on'
	switchOff()
	switchOn()
	setTimestamp()
	return jsonify({})

@app.route('/api/off', methods=['GET'])
def apiOff() :
	global crntColors, globalLastCalledApi
	globalLastCalledApi = '/api/off'
	crntColors = None
	switchOff()
	setTimestamp()
	return jsonify({})

@app.route('/api/shutdown', methods=['DELETE'])
def turnOff() :
	switchOff()
	shutdownPi()
	return make_response(jsonify({"message": "Shutdown Triggered!"}))

@app.route('/api/countdown', methods=['GET'])
def apiCountDown():
        global blinkThread
        blinkThread = threading.Thread(target=countDown, args=(14,))
        blinkThread.do_run = True
        blinkThread.start()
        return make_response(jsonify({"message": "14 second countdown started"}))

@app.route('/api/icons', methods=['GET'])
def getIcons():
        files = glob.glob(f"./icons/{unicorn.get_type()}/*.json")
        icons = []
        for file in files:
                icons.append(file.split('/')[len(file.split('/'))-1].split('.')[0])
        return make_response(jsonify(icons))

# This method is added for homekit compatibility
@app.route('/api/switch/hsv', methods=['POST'])
def apiSwitchHsv() :
	global blinkThread, globalLastCalledApi
	globalLastCalledApi = '/api/switch/hsv'
	switchOff()
	content = request.json
	h = content.get('hue', 180)
	s = content.get('saturation', 100)
	v = content.get('value', 100)
	rgb = tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
	brightness = content.get('brightness', 0.5)
	speed = content.get('speed', '')
	blinkThread = threading.Thread(target=setDisplay, args=("", rgb[0], rgb[1], rgb[2], brightness, speed))
	blinkThread.do_run = True
	blinkThread.start()
	setTimestamp()
	return make_response(jsonify())

# This is the original method for setting the display
@app.route('/api/switch/rgb', methods=['POST'])
def apiSwitchRgb() :
	global blinkThread, globalLastCalledApi
	globalLastCalledApi = '/api/switch/rgb'
	switchOff()
	content = request.json
	red = content.get('red', '')
	green = content.get('green', '')
	blue = content.get('blue', '')
	brightness = content.get('brightness', '')
	speed = content.get('speed', '')
	blinkThread = threading.Thread(target=setDisplay, args=("", red, green, blue, brightness, speed))
	blinkThread.do_run = True
	blinkThread.start()
	setTimestamp()
	return make_response(jsonify())

# Added this to allow for simple icons/pixel art
@app.route('/api/switch/icon', methods=['POST'])
def apiSwitchIcon() :
	global blinkThread, globalLastCalledApi
	globalLastCalledApi = '/api/switch/icon'
	switchOff()
	content = request.json
	icon = content.get('icon', '')
	red = content.get('red', '')
	green = content.get('green', '')
	blue = content.get('blue', '')
	brightness = content.get('brightness', '')
	speed = content.get('speed', '')
	jsonObj = getIcon(icon)
	if not jsonObj:
                return make_response(jsonify({'error': 'Invalid Icon name', 'message': f"No icon file matches ./icons/{unicorn.get_type()}/{icon}.json... Maybe think about creating it?" }), 500)
	blinkThread = threading.Thread(target=setDisplay, args=(jsonObj, red, green, blue, brightness, speed))
	blinkThread.do_run = True
	blinkThread.start()
	setTimestamp()
	return make_response(jsonify())

# This allows for development of new icons so you
# can test the raw JSON before you create an icon
# json file.
@app.route('/api/switch/json', methods=['POST'])
def apiSwitchJson() :
        global blinkThread, globalLastCalledApi
        globalLastCalledApi = '/api/switch/json'
        switchOff()
        content = request.json
        jsonObj = content.get('json', '')
        valid, message = validateJson(jsonObj) 
        if not valid:
                return make_response(jsonify({'error': 'Invalid Json', 'message': message}), 500)
        red = content.get('red', '')
        green = content.get('green', '')
        blue = content.get('blue', '')
        brightness = content.get('brightness', '')
        speed = content.get('speed', '')
        blinkThread = threading.Thread(target=setDisplay, args=(jsonObj, red, green, blue, brightness, speed))
        blinkThread.do_run = True
        blinkThread.start()
        setTimestamp()
        return make_response(jsonify())

@app.route('/api/status', methods=['GET'])
def apiStatus() :
	global globalBlue, globalGreen, globalRed, globalLastCalled, globalLastCalledApi
	cpu = CPUTemperature()
	return jsonify({ 'red': globalRed, 'green': globalGreen, 'blue': globalBlue, 'lastCalled': globalLastCalled, 'cpuTemp': cpu.temperature, 'lastCalledApi': globalLastCalledApi })


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=False)
