#!/usr/bin/env python

import json
import unicornhat as unicorn
import threading
from time import sleep

from flask import Flask, jsonify, make_response, request
from random import randint

status = False
blinkThread = None

#setup the unicorn hat
unicorn.set_layout(unicorn.AUTO)
unicorn.brightness(0.5)

#get the width and height of the hardware
width, height = unicorn.get_shape()

app = Flask(__name__)

def setColor(r, g, b) :
	global status
	if status == True :
		#set the LEDs to the relevant lighting (all on/off)
		for y in range(height):
			for x in range(width):
				unicorn.set_pixel(x, y, r, g, b)
		unicorn.show()
		sleep(.15)
		unicorn.clear()
		unicorn.show()
		sleep(.15)
		setColor(r, g, b)
    

def switchOn() :
	global blinkThread
	red = randint(30, 255)
	green = randint(30, 255)
	blue = randint(30, 255)
	blinkThread = threading.Thread(target=setColor, args=(red, green, blue))
	blinkThread.start()

def switchOff() :
	global blinkThread
	blinkThread.join()
	unicorn.clear()
	unicorn.off()

# API start

@app.route('/api/on', methods=['GET'])
def apiOn() :
	global status
	status = True
	switchOff()
	switchOn()
	return jsonify({})

@app.route('/api/off', methods=['GET'])
def apiOff() :
	global status
	status = False
	switchOff()
	return jsonify({})

@app.route('/api/switch', methods=['POST'])
def apiSwitch() :
	global status
	global blinkThread
	switchOff()
	status = True
	content = request.json
	red = content.get('red', '')
	green = content.get('green', '')
	blue = content.get('blue', '')
	blinkThread = threading.Thread(target=setColor, args=(red, green, blue))
	blinkThread.start()
	return make_response(jsonify())


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=False)