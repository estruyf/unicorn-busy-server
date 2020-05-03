#!/usr/bin/env python

import json
import unicornhat as unicorn
import threading
from time import sleep
from datetime import datetime
from gpiozero import CPUTemperature

from flask import Flask, jsonify, make_response, request
from random import randint

blinkThread = None
globalRed = 0
globalGreen = 0
globalBlue = 0
globalLastCalled = None
globalLastCalledApi = None

#setup the unicorn hat
unicorn.set_layout(unicorn.AUTO)
unicorn.brightness(0.5)

#get the width and height of the hardware
width, height = unicorn.get_shape()

app = Flask(__name__)

def setColor(icon, r, g, b, brightness, speed) :
	global crntColors, globalBlue, globalGreen, globalRed
	globalRed = r
	globalGreen = g
	globalBlue = b

	if brightness != '' :
		unicorn.brightness(brightness)
	
	if icon == "dnd":
		dnd(r, g, b)
		globalIcon="dnd"
	elif icon == "phone":
		phone(r, g, b)
		globalIcon="phone"
	elif icon == "pencil":
		pencil(r, g, b)
		globalIcon="pencil"
	elif icon == "exclaim":
		exclaim(r, g, b)
		globalIcon="exclaim"
	else:
		globalIcon="none"
		for y in range(height):
			for x in range(width):
				unicorn.set_pixel(x, y, r, g, b)
	unicorn.show()

	if speed != '' :
		sleep(speed)
		unicorn.clear()
		crntT = threading.currentThread()
		while getattr(crntT, "do_run", True) :
			
			if icon == "dnd":
				dnd(r, g, b)
				globalIcon="dnd"
			elif icon == "phone":
				phone(r, g, b)
				globalIcon="phone"
			elif icon == "pencil":
				pencil(r, g, b)
				globalIcon="pencil"
			elif icon == "exclaim":
				exclaim(r, g, b)
				globalIcon="exclaim"
			else:
				globalIncon="none"
				for y in range(height):
					for x in range(width):
						unicorn.set_pixel(x, y, r, g, b)
			unicorn.show()
			sleep(speed)
			unicorn.clear()
			unicorn.show()
			sleep(speed)
		
def dnd(r, g, b):
	unicorn.set_pixel(0,0,0,0,0)
	unicorn.set_pixel(0,1,r,g,b)
	unicorn.set_pixel(0,2,r,g,b)
	unicorn.set_pixel(0,3,0,0,0)
	unicorn.set_pixel(1,0,r,g,b)
	unicorn.set_pixel(1,1,r,g,b)
	unicorn.set_pixel(1,2,r,g,b)
	unicorn.set_pixel(1,3,r,g,b)
	unicorn.set_pixel(2,0,r,g,b)
	unicorn.set_pixel(2,1,r,g,b)
	unicorn.set_pixel(2,2,r,g,b)
	unicorn.set_pixel(2,3,r,g,b)
	unicorn.set_pixel(3,0,255,255,255)
	unicorn.set_pixel(3,1,255,255,255)
	unicorn.set_pixel(3,2,255,255,255)
	unicorn.set_pixel(3,3,255,255,255)
	unicorn.set_pixel(4,0,255,255,255)
	unicorn.set_pixel(4,1,255,255,255)
	unicorn.set_pixel(4,2,255,255,255)
	unicorn.set_pixel(4,3,255,255,255)
	unicorn.set_pixel(5,0,r,g,b)
	unicorn.set_pixel(5,1,r,g,b)
	unicorn.set_pixel(5,2,r,g,b)
	unicorn.set_pixel(5,3,r,g,b)
	unicorn.set_pixel(6,0,r,g,b)
	unicorn.set_pixel(6,1,r,g,b)
	unicorn.set_pixel(6,2,r,g,b)
	unicorn.set_pixel(6,3,r,g,b)
	unicorn.set_pixel(7,0,0,0,0)
	unicorn.set_pixel(7,1,r,g,b)
	unicorn.set_pixel(7,2,r,g,b)
	unicorn.set_pixel(7,3,0,0,0)

def phone(r, g, b):
	unicorn.set_pixel(0,0,0,0,0)
	unicorn.set_pixel(0,1,0,0,0)
	unicorn.set_pixel(0,2,r,g,b)
	unicorn.set_pixel(0,3,r,g,b)
	unicorn.set_pixel(1,0,0,0,0)
	unicorn.set_pixel(1,1,r,g,b)
	unicorn.set_pixel(1,2,r,g,b)
	unicorn.set_pixel(1,3,r,g,b)
	unicorn.set_pixel(2,0,r,g,b)
	unicorn.set_pixel(2,1,r,g,b)
	unicorn.set_pixel(2,2,r,g,b)
	unicorn.set_pixel(2,3,r,g,b)
	unicorn.set_pixel(3,0,r,g,b)
	unicorn.set_pixel(3,1,r,g,b)
	unicorn.set_pixel(3,2,0,0,0)
	unicorn.set_pixel(3,3,0,0,0)
	unicorn.set_pixel(4,0,r,g,b)
	unicorn.set_pixel(4,1,r,g,b)
	unicorn.set_pixel(4,2,0,0,0)
	unicorn.set_pixel(4,3,0,0,0)
	unicorn.set_pixel(5,0,r,g,b)
	unicorn.set_pixel(5,1,r,g,b)
	unicorn.set_pixel(5,2,r,g,b)
	unicorn.set_pixel(5,3,r,g,b)
	unicorn.set_pixel(6,0,0,0,0)
	unicorn.set_pixel(6,1,r,g,b)
	unicorn.set_pixel(6,2,r,g,b)
	unicorn.set_pixel(6,3,r,g,b)
	unicorn.set_pixel(7,0,0,0,0)
	unicorn.set_pixel(7,1,0,0,0)
	unicorn.set_pixel(7,2,r,g,b)
	unicorn.set_pixel(7,3,r,g,b)

def pencil(r, g, b):
	unicorn.set_pixel(0,0,255,0,0)
	unicorn.set_pixel(0,1,255,0,0)
	unicorn.set_pixel(0,2,255,0,0)
	unicorn.set_pixel(0,3,0,0,0)
	unicorn.set_pixel(1,0,r,g,b)
	unicorn.set_pixel(1,1,r,g,b)
	unicorn.set_pixel(1,2,r,g,b)
	unicorn.set_pixel(1,3,0,0,0)
	unicorn.set_pixel(2,0,r,g,b)
	unicorn.set_pixel(2,1,r,g,b)
	unicorn.set_pixel(2,2,r,g,b)
	unicorn.set_pixel(2,3,0,0,0)
	unicorn.set_pixel(3,0,r,g,b)
	unicorn.set_pixel(3,1,r,g,b)
	unicorn.set_pixel(3,2,r,g,b)
	unicorn.set_pixel(3,3,0,0,0)
	unicorn.set_pixel(4,0,r,g,b)
	unicorn.set_pixel(4,1,r,g,b)
	unicorn.set_pixel(4,2,r,g,b)
	unicorn.set_pixel(4,3,0,0,0)
	unicorn.set_pixel(5,0,204,153,0)
	unicorn.set_pixel(5,1,204,153,0)
	unicorn.set_pixel(5,2,204,153,0)
	unicorn.set_pixel(5,3,0,0,0)
	unicorn.set_pixel(6,0,0,0,0)
	unicorn.set_pixel(6,1,204,153,0)
	unicorn.set_pixel(6,2,0,0,0)
	unicorn.set_pixel(6,3,0,0,0)
	unicorn.set_pixel(7,0,0,0,0)
	unicorn.set_pixel(7,1,r,g,b)
	unicorn.set_pixel(7,2,r,g,b)
	unicorn.set_pixel(7,3,r,g,b)

def exclaim(r, g, b):
	unicorn.set_pixel(0,0,0,0,0)
	unicorn.set_pixel(0,1,r,g,b)
	unicorn.set_pixel(0,2,r,g,b)
	unicorn.set_pixel(0,3,0,0,0)
	unicorn.set_pixel(1,0,0,0,0)
	unicorn.set_pixel(1,1,r,g,b)
	unicorn.set_pixel(1,2,r,g,b)
	unicorn.set_pixel(1,3,0,0,0)
	unicorn.set_pixel(2,0,0,0,0)
	unicorn.set_pixel(2,1,r,g,b)
	unicorn.set_pixel(2,2,r,g,b)
	unicorn.set_pixel(2,3,0,0,0)
	unicorn.set_pixel(3,0,0,0,0)
	unicorn.set_pixel(3,1,r,g,b)
	unicorn.set_pixel(3,2,r,g,b)
	unicorn.set_pixel(3,3,0,0,0)
	unicorn.set_pixel(4,0,0,0,0)
	unicorn.set_pixel(4,1,r,g,b)
	unicorn.set_pixel(4,2,r,g,b)
	unicorn.set_pixel(4,3,0,0,0)
	unicorn.set_pixel(5,0,0,0,0)
	unicorn.set_pixel(5,1,0,0,0)
	unicorn.set_pixel(5,2,0,0,0)
	unicorn.set_pixel(5,3,0,0,0)
	unicorn.set_pixel(6,0,0,0,0)
	unicorn.set_pixel(6,1,r,g,b)
	unicorn.set_pixel(6,2,r,g,b)
	unicorn.set_pixel(6,3,0,0,0)
	unicorn.set_pixel(7,0,0,0,0)
	unicorn.set_pixel(7,1,r,g,b)
	unicorn.set_pixel(7,2,r,g,b)
	unicorn.set_pixel(7,3,0,0,0)

def switchOn() :
	red = randint(10, 255)
	green = randint(10, 255)
	blue = randint(10, 255)
	blinkThread = threading.Thread(target=setColor, args=('', red, green, blue, '', ''))
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
        os.system("shutdown /s /t 1")

def setTimestamp() :
	global globalLastCalled
	globalLastCalled = datetime.now()

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

@app.route('/api/shutdown', method=['DELETE'])
def turnOff() :
        switchOff()
        shutdownPi()

@app.route('/api/switch', methods=['POST'])
def apiSwitch() :
	global blinkThread, globalLastCalledApi
	globalLastCalledApi = '/api/switch'
	switchOff()
	content = request.json
	red = content.get('red', '')
	green = content.get('green', '')
	blue = content.get('blue', '')
	brightness = content.get('brightness', '')
	speed = content.get('speed', '')
	blinkThread = threading.Thread(target=setColor, args=(red, green, blue, brightness, speed))
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
