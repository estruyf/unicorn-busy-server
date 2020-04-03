#!/usr/bin/env python

import json
import unicornhat as unicorn
import threading
from time import sleep

from flask import Flask, jsonify, make_response, request
from random import randint

blinkThread = None

#setup the unicorn hat
unicorn.set_layout(unicorn.AUTO)
unicorn.brightness(0.5)

#get the width and height of the hardware
width, height = unicorn.get_shape()

app = Flask(__name__)

def setColor(r, g, b, brightness, speed) :
	if brightness != '' :
		unicorn.brightness(brightness)

	crntT = threading.currentThread()
	while getattr(crntT, "do_run", True) :
		for y in range(height):
			for x in range(width):
				unicorn.set_pixel(x, y, r, g, b)
		unicorn.show()
		if speed != '' :
			sleep(speed)
			unicorn.clear()
			unicorn.show()
			sleep(speed)
			setColor(r, g, b, brightness, speed)
		
def switchOn() :
	red = randint(10, 255)
	green = randint(10, 255)
	blue = randint(10, 255)
	blinkThread = threading.Thread(target=setColor, args=(red, green, blue, '', ''))
	blinkThread.do_run = True
	blinkThread.start()

def switchOff() :
	global blinkThread
	if blinkThread != None :
		blinkThread.do_run = False
	unicorn.clear()
	unicorn.off()

# API Initialization
@app.route('/api/on', methods=['GET'])
def apiOn() :
	switchOff()
	switchOn()
	return jsonify({})

@app.route('/api/off', methods=['GET'])
def apiOff() :
	switchOff()
	return jsonify({})

@app.route('/api/switch', methods=['POST'])
def apiSwitch() :
	global blinkThread
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
	return make_response(jsonify())


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=False)