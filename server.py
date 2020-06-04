#!/usr/bin/env python

import json

import os
import threading
from time import sleep
from datetime import datetime
from gpiozero import CPUTemperature
from lib.unicorn_wrapper import UnicornWrapper
from flask import Flask, jsonify, make_response, request, send_from_directory
from random import randint
from jsmin import jsmin

blinkThread = None
globalRed = 0
globalGreen = 0
globalBlue = 0
globalBrightness = 0
globalLastCalled = None
globalLastCalledApi = None
globalStatus = None
globalStatusOverwrite = false

app = Flask(__name__, static_folder='front-end/build')

# Initalize the Unicorn hat
unicorn = UnicornWrapper()

#get the width and height of the hardware and set it to portrait if its not
width, height = unicorn.getShape()

class MyFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
            with self.app_context():
                startupRainbow()
        super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

app = MyFlaskApp(__name__)

def setColor(r, g, b, brightness = 0.5, speed = None):
        global crntColors
        setPixels(r, g, b, brightness)
        unicorn.show()

        if speed != None and speed != '' :
                crntT = threading.currentThread()
                unicorn.clear()
                while getattr(crntT, "do_run", True):
                        setPixels(r, g, b, brightness)
                        unicorn.show()
                        sleep(speed)
                        unicorn.clear()
                        unicorn.show()
                        sleep(speed)

def setPixels(r, g, b, brightness = 0.5):
        global globalBrightness, globalBlue, globalGreen, globalRed
        
        globalRed = r
        globalGreen = g
        globalBlue = b

        if brightness is not None:
                globalBrightness = brightness
                unicorn.setBrightness(brightness)
        
        unicorn.setColour(r,g,b)

def switchOn():
    rgb = unicorn.hsvIntToRGB(randint(0,360),100,100)
    blinkThread = threading.Thread(target=setColor, args=(rgb[0], rgb[1], rgb[2]))
    blinkThread.do_run = True
    blinkThread.start()

def switchOff():
    global blinkThread, globalBlue, globalGreen, globalRed
    globalRed = 0
    globalGreen = 0
    globalBlue = 0
    if blinkThread != None :
        blinkThread.do_run = False
    unicorn.clear()
    unicorn.off()

def halfBlink():
        unicorn.show()
        sleep(0.8)
        unicorn.clear()
        unicorn.show()
        sleep(0.2)   

def countDown(time):
    showTime = time - 12
    brightness = 0.5
    while(showTime > 0):
            b = brightness
            for x in range(4):
                b = b - x
                setPixels(255, 255, 0, b)
                unicorn.show()
                sleep(0.5)
                unicorn.clear()
            unicorn.show()
            sleep(2)
            showTime = showTime - 2
    for i in range(10):
            setPixels(255, 0, 0, 0.5)
            halfBlink()
    setColor(255, 0, 0, 0.5)
    halfBlink()
    unicorn.clear()
    unicorn.off()

def shutdownPi():
    global blinkThread
    blinkThread = threading.Thread(target=countDown, args=(60,))
    blinkThread.do_run = True
    blinkThread.start()
    os.system("shutdown +1 'Shutdown trigger via API... Shutting down in 2 minute'")

def displayRainbow(step, brightness, speed, run = None, hue = None):
        global crntColors
        if hue == None:
                hue = 0
        if step is None:
                step = 1
        if speed is None:
                speed is 0.2
        if brightness is None:
                brightness = 0.5
        crntT = threading.currentThread()
        while getattr(crntT, "do_run", True):
                unicorn.setColour(RGB = unicorn.hsvIntToRGB(hue,100,100))
                sleep(speed)
                if hue >= 360:
                        hue = 0
                        if run is not None:
                                run = run - 1
                                if run <= 0:
                                        switchOff()
                else:
                        hue = hue + step

def setTimestamp():
    global globalLastCalled
    globalLastCalled = datetime.now()

# API Initialization
@app.route('/', methods=['GET'])
def root():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/on', methods=['GET'])
def apiOn():
    global globalStatus, globalLastCalledApi
    globalStatus = 'on'
    globalLastCalledApi = '/api/on'
    switchOff()
    switchOn()
    setTimestamp()
    return jsonify({})

@app.route('/api/off', methods=['GET'])
def apiOff():
    global crntColors, globalStatus, globalLastCalledApi
    globalStatus = 'off'
    globalLastCalledApi = '/api/off'
    crntColors = None
    switchOff()
    setTimestamp()
    return jsonify({})

@app.route('/api/switch', methods=['POST'])
def apiSwitch():
    global blinkThread, globalStatus, globalLastCalledApi
    globalLastCalledApi = '/api/switch'
    switchOff()
    content = json.loads(jsmin(request.get_data(as_text=True)))
    red = content.get('red', None)
    green = content.get('green', None)
    blue = content.get('blue', None)
    if red is None or green is None or blue is None:
        return make_response(jsonify({'error': 'red, green and blue must be present and can\' be empty'}), 500)

		if red == 0 and green == 144 and blue == 0:
				globalStatus = 'Available'
		elif red == 255 and green == 191 and blue == 0:
				globalStatus = 'Away'
		elif red == 179 and green == 0 and blue == 0:
				globalStatus = 'Busy'
		else:
				globalStatus = None

    brightness = content.get('brightness', None)
    speed = content.get('speed', None)
    blinkThread = threading.Thread(target=setColor, args=(red, green, blue, brightness, speed))
    blinkThread.do_run = True
    blinkThread.start()
    setTimestamp()
    return make_response(jsonify())

@app.route('/api/rainbow', methods=['POST'])
def apiDisplayRainbow():
    global blinkThread, globalStatus, globalLastCalledApi
		globalStatus = 'rainbow'
    globalLastCalledApi = '/api/rainbow'
    switchOff()
    data = request.get_data(as_text=True)
    content = json.loads(jsmin(request.get_data(as_text=True)))
    hue = content.get('hue', 0)
    step = content.get('step', None)
    brightness = content.get('brightness', None)
    speed = content.get('speed', None)
    blinkThread = threading.Thread(target=displayRainbow, args=(step, brightness, speed, None, hue))
    blinkThread.do_run = True
    blinkThread.start()
    setTimestamp()
    return make_response(jsonify())

@app.route('/api/status', methods=['GET'])
def apiStatus():
    global globalStatus, globalBlue, globalGreen, globalRed, globalBrightness, \
                globalLastCalled, globalLastCalledApi, width, height, unicorn

    cpu = CPUTemperature()
    return jsonify({ 'red': globalRed, 'green': globalGreen, 
                'blue': globalBlue, 'brightness': globalBrightness, 
                'lastCalled': globalLastCalled, 'cpuTemp': cpu.temperature,
                'lastCalledApi': globalLastCalledApi, 'height': height,
                'width': width, 'unicorn': unicorn.getType(), 'status': globalStatus })

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

def startupRainbow():
        global blinkThread
        blinkThread = threading.Thread(target=displayRainbow, args=(10, 1, 0.1, 1))
        blinkThread.do_run = True
        blinkThread.start()

if __name__ == '__main__':
        app.run(host='0.0.0.0', debug=False)
