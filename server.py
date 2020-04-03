#!/usr/bin/env python

import json
import unicornhat as unicorn
from time import sleep

from flask import Flask, jsonify, make_response, request
from random import randint

status = False

#setup the unicorn hat
unicorn.set_layout(unicorn.AUTO)
unicorn.brightness(0.5)

#get the width and height of the hardware
width, height = unicorn.get_shape()

app = Flask(__name__)

def setColor(r, g, b) :
	if status == True :
		#set the LEDs to the relevant lighting (all on/off)
		for y in range(height):
			for x in range(width):
				nextX = x + 1
				if nextX > width :
					nextX = 0
				unicorn.set_pixel(x, y, r, g, b)
				unicorn.set_pixel(nextX, y, 0, 0, 0)
				unicorn.show()
				sleep(.1)
		setColor(r, g, b)
    

def switchOn() :
	r = randint(30, 255)
	g = randint(30, 255)
	b = randint(30, 255)
	setColor(r, g, b)

def switchOff() :
	unicorn.off()

# API start

@app.route('/api/on', methods=['GET'])
def apiOn() :
  status = True
  switchOn()
  return jsonify({})

@app.route('/api/off', methods=['GET'])
def apiOff() :
	status = False
	switchOff()
	return jsonify({})

@app.route('/api/switch', methods=['POST'])
def apiSwitch() :
	status = True
	content = request.json
	red = content.get('red', '')
	green = content.get('green', '')
	blue = content.get('blue', '')
	setColor(red, green, blue)
	return make_response(jsonify())


@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug=False)