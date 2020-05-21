#!sudo /usr/bin/env python

import os
import json
from jsmin import jsmin
import threading
import glob
from lib.unicorn_wrapper import UnicornWrapper
from time import sleep
from datetime import datetime
from gpiozero import CPUTemperature

from flask import Flask, jsonify, make_response, request, redirect, url_for, send_from_directory, render_template
from random import randint

# Initalize the Unicorn hat
unicorn = UnicornWrapper()

blinkThread = None
globalRed = 0
globalGreen = 0
globalBlue = 0
globalBrightness = 0
globalIcon = 'none'
globalShutdown= None
globalLastCalled = None
globalLastCalledApi = None

#get the width and height of the hardware and set it to portrait if its not
width, height = unicorn.getShape()

class MyFlaskApp(Flask):
    def run(self, host=None, port=None, debug=None, load_dotenv=True, **options):
        if not self.debug or os.getenv('WERKZEUG_RUN_MAIN') == 'true':
            with self.app_context():
                startupRainbow()
        super(MyFlaskApp, self).run(host=host, port=port, debug=debug, load_dotenv=load_dotenv, **options)

app = MyFlaskApp(__name__)

def validateJson(j):
        try:
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
        except KeyError as err:
                return False, f"An error occured, Missing JSON Key: {err}"

def setPixels(r, g, b, brightness = 0.5, jsonObj = None):
        global globalIcon, globalBrightness, globalBlue, globalGreen, globalRed
        
        globalRed = r
        globalGreen = g
        globalBlue = b

        if brightness is not None:
                globalBrightness = brightness
                unicorn.setBrightness(brightness)

        if jsonObj is not None:
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
                                unicorn.setPixel(x, y, red, green, blue)
        else:
                globalIcon="none"
                unicorn.setColour(r,g,b)

def setDisplay(r, g, b, brightness = 0.5, speed = None, jsonObj = None):
        global crntColors, globalIcon, globalBrightness, globalBlue, globalGreen, globalRed
        globalBrightness = brightness
        globalRed = -1
        globalGreen = -1
        globalRed = -1
        globalIcon = "Rainbow"

        setPixels(r, g, b, brightness, jsonObj)
        unicorn.show()

        if speed != None and speed != '' :
                sleep(speed)
                unicorn.clear()
                crntT = threading.currentThread()
                while getattr(crntT, "do_run", True) :
                        setPixels(r, g, b, brightness, jsonObj)
                        unicorn.show()
                        sleep(speed)
                        unicorn.clear()
                        unicorn.show()
                        sleep(speed)

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

def halfBlink():
        unicorn.show()
        sleep(0.8)
        unicorn.clear()
        unicorn.show()
        sleep(0.2)   

def countDown(time):
    crntT = threading.currentThread()
    showTime = time - 12
    while getattr(crntT, "do_run", True) and showTime > 0:
            setPixels(255, 255, 0, 0.5, jsonObj = getIcon("arrow-down"))
            unicorn.show()
            sleep(1)
            unicorn.clear()
            unicorn.show()
            sleep(1)
            showTime = showTime - 2
    i = 10
    while getattr(crntT, "do_run", True) and i <= 0:
            i = i - 1
            obj = getIcon(f"numbers/{i}")
            setPixels(255, 255, 0, 0.5, jsonObj=obj)
            halfBlink()
    setDisplay(255, 0, 0, 0.5)
    halfBlink()
    unicorn.clear()
    unicorn.off()

def getIcon(icon):
        try:
                f = open(f"./icons/{unicorn.getType()}/{icon}.json", "r")
                return json.loads(jsmin(f.read()))
        except ValueError:
                return False
        except IOError:
                return False

def switchOn():
    global blinkThread, globalBlue, globalGreen, globalRed
    rgb = unicorn.hsvIntToRGB(randint(0,360),100,100)
    blinkThread = threading.Thread(target=setDisplay, args=(rgb[0], rgb[1], rgb[2]))
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
    global blinkThread, globalShutdown, globalBlue, globalGreen, globalRed 
    globalShutdown = "Shutting Down!"
    globalRed = None
    globalBlue = None
    globalGreen = None
    blinkThread = threading.Thread(target=countDown, args=(60,))
    blinkThread.do_run = True
    blinkThread.start()
    os.system("shutdown +2 'Shutdown trigger via API... Shutting down in 2 minute'")

def cancelShutdown() :
    global blinkThread, globalShutdown, globalBlue, globalGreen, globalRed 
    globalShutdown = None
    globalRed = None
    globalBlue = None
    globalGreen = None
    os.system("shutdown -c 'Shutdown cancelled!... Carry on folks!'")
    blinkThread.do_run = False
    unicorn.clear()
    unicorn.off()
    switchOn()

def setTimestamp() :
    global globalLastCalled
    globalLastCalled = datetime.now()

# API Initialization
@app.route('/api/on', methods=['GET'])
def apiOn() :
    global globalLastCalledApi, globalShutdown
    if globalShutdown:
        return jsonify({"message": "Shutting Down!"})
    globalLastCalledApi = '/api/on'
    switchOff()
    switchOn()
    setTimestamp()
    return jsonify({})

@app.route('/api/off', methods=['GET'])
def apiOff() :
    global crntColors, globalLastCalledApi, globalShutdown
    if globalShutdown:
        return jsonify({"message": "Shutting Down!"})
    globalLastCalledApi = '/api/off'
    crntColors = None
    switchOff()
    setTimestamp()
    return jsonify({})

@app.route('/api/shutdown', methods=['DELETE'])
def turnOff() :
    global globalLastCalledApi, globalShutdown
    if globalShutdown:
        return jsonify({"message": "Shutting Down!"})
    globalLastCalledApi = '/api/shutdown'
    setTimestamp()
    switchOff()
    shutdownPi()
    return make_response(jsonify({"message": "Shutdown Triggered!"}))

@app.route('/api/countdown', methods=['GET'])
def apiCountDown():
    global blinkThread, globalShutdown
    if globalShutdown:
        return jsonify({"message": "Shutting Down!"})
    blinkThread = threading.Thread(target=countDown, args=(14,))
    blinkThread.do_run = True
    blinkThread.start()
    return make_response(jsonify({"message": "14 second countdown started"}))

@app.route('/api/icons', methods=['GET'])
def getIcons():
    path = f"./icons/{unicorn.getType()}/"
    files = glob.glob(f"{path}**/*.json", recursive=True)
    icons = []
    for file in files:
            icons.append(file.replace(path, "").split('.')[0])
    return make_response(jsonify({"unicorn": unicorn.getType(), "height": height, "width": width, "icons": icons}))

# This method is added for homekit compatibility
@app.route('/api/display/hsv', methods=['POST'])
def apiDisplayHsv():
    global blinkThread, globalLastCalledApi, globalShutdown
    if globalShutdown:
        return jsonify({"message": "Shutting Down!"})
    globalLastCalledApi = '/api/display/hsv'
    switchOff()
    content = json.load(jsmin(request.get_data()))
    hue = content.get('hue', 0)
    saturation = content.get('saturation', 0)
    value = content.get('value', 0)
    rgb = unicorn.hsvIntToRGB(hue, saturation, value)
    brightness = content.get('brightness', 0.5)
    speed = content.get('speed', '')
    blinkThread = threading.Thread(target=setDisplay, args=(rgb[0], rgb[1], rgb[2], brightness, speed))
    blinkThread.do_run = True
    blinkThread.start()
    setTimestamp()
    return make_response(jsonify())

@app.route('/api/display/rainbow', methods=['POST'])
def apiDisplayRainbow():
    global blinkThread, globalLastCalledApi, globalShutdown
    if globalShutdown:
        return jsonify({"message": "Shutting Down!"})
    switchOff()
    content = json.load(jsmin(request.get_data()))
    hue = content.get('hue', 0)
    step = content.get('step', None)
    brightness = content.get('brightness', None)
    speed = content.get('speed', None)
    blinkThread = threading.Thread(target=displayRainbow, args=(step, brightness, speed, None, hue))
    blinkThread.do_run = True
    blinkThread.start()
    setTimestamp()
    return make_response(jsonify())

# This is the original method for setting the display
@app.route('/api/display/rgb', methods=['POST'])
def apiDisplayRgb():
    global blinkThread, globalLastCalledApi, globalShutdown
    if globalShutdown:
        return jsonify({"message": "Shutting Down!"})
    globalLastCalledApi = '/api/display/rgb'
    switchOff()
    content = json.load(jsmin(request.get_data()))
    r = content.get('red', '')
    g = content.get('green', '')
    b = content.get('blue', '')
    brightness = content.get('brightness', None)
    speed = content.get('speed', None)
    blinkThread = threading.Thread(target=setDisplay, args=(r, g, b, brightness, speed))
    blinkThread.do_run = True
    blinkThread.start()
    setTimestamp()
    return make_response(jsonify())

# Added this to allow for simple icons/pixel art
@app.route('/api/display/icon', methods=['POST'])
def apiDisplayIcon():
    global blinkThread, globalLastCalledApi, globalShutdown
    if globalShutdown:
        return jsonify({"message": "Shutting Down!"})
    globalLastCalledApi = '/api/display/icon'
    switchOff()
    content = json.load(jsmin(request.get_data()))
    icon = content.get('icon', None)
    red = content.get('red', '')
    green = content.get('green', '')
    blue = content.get('blue', '')
    brightness = content.get('brightness', None)
    speed = content.get('speed', None)
    jsonObj = getIcon(icon)
    if not jsonObj:
                return make_response(jsonify({'error': 'Invalid Icon name', 'message': f"No icon file matches ./icons/{unicorn.getType()}/{icon}.json... Maybe think about creating it?" }), 500)
    blinkThread = threading.Thread(target=setDisplay, args=(red, green, blue, brightness, speed, jsonObj))
    blinkThread.do_run = True
    blinkThread.start()
    setTimestamp()
    return make_response(jsonify())

# This allows for development of new icons so you
# can test the raw JSON before you create an icon
# json file.
@app.route('/api/display/json', methods=['POST'])
def apiDisplayJson():
    global blinkThread, globalLastCalledApi, globalShutdown
    if globalShutdown:
        return jsonify({"message": "Shutting Down!"})
    globalLastCalledApi = '/api/display/json'
    switchOff()
    content = json.load(jsmin(request.get_data()))
    jsonObj = jsmin(content.get('json', ''))
    valid, message = validateJson(jsonObj) 
    if not valid:
            return make_response(jsonify({'error': 'Invalid Json', 'message': message}), 500)
    red = content.get('red', '')
    green = content.get('green', '')
    blue = content.get('blue', '')
    brightness = content.get('brightness', None)
    speed = content.get('speed', None)
    blinkThread = threading.Thread(target=setDisplay, args=( red, green, blue, brightness, speed, jsonObj))
    blinkThread.do_run = True
    blinkThread.start()
    setTimestamp()
    return make_response(jsonify())

@app.route('/api/status', methods=['GET'])
def apiStatus():
    global globalBlue, globalGreen, globalRed, globalBrightness, globalIcon, \
                globalLastCalled, globalLastCalledApi, width, height, unicorn
    cpu = CPUTemperature()
    return jsonify({ 'red': globalRed, 'green': globalGreen, 
                'blue': globalBlue, 'brightness': globalBrightness, 
                'icon': globalIcon, 'lastCalled': globalLastCalled, 
                'cpuTemp': cpu.temperature, 'lastCalledApi': globalLastCalledApi,
                'height': height, 'width': width, 'unicorn': unicorn.getType() })

#Non Api routes for the frontend
@app.route('/', methods=['GET'])
def root():
    global globalShutdown
    return render_template("index.html", shutdown=globalShutdown)

@app.route('/off', methods=['GET'])
def offCall():
    global globalShutdown, globalLastCalledApi
    if globalShutdown:
        return render_template("index.html", shutdown=globalShutdown)
    globalLastCalledApi='Frontend: Off'
    switchOff()
    return render_template("index.html", off="off", shutdown=globalShutdown)

@app.route('/on', methods=['GET'])
def onCall():
    global globalShutdown, globalLastCalledApi, globalBlue, globalGreen, globalRed
    if globalShutdown:
        return render_template("index.html", shutdown=globalShutdown)
    globalLastCalledApi='Frontend: On'
    switchOff()
    switchOn()
    return render_template("index.html", on="on", r=globalRed, g=globalGreen, b=globalBlue, shutdown=globalShutdown)

@app.route('/busy', methods=['POST'])
def busyCall():
    global globalShutdown, globalLastCalledApi, blinkThread
    if globalShutdown:
        return render_template("index.html", shutdown=globalShutdown)
    globalLastCalledApi='Frontend: Busy'
    switchOff()
    jsonObj = getIcon("dnd")
    blinkThread = threading.Thread(target=setDisplay, args=(255, 0, 0, 0.7, 1, jsonObj))
    blinkThread.do_run = True
    blinkThread.start()
    setTimestamp()
    return render_template("index.html", busy="busy", shutdown=globalShutdown)

@app.route('/available', methods=['POST'])
def availableCall():
    global globalShutdown, globalLastCalledApi, blinkThread
    if globalShutdown:
        return render_template("index.html", shutdown=globalShutdown)
    globalLastCalledApi='Frontend: Busy'
    switchOff()
    blinkThread = threading.Thread(target=setDisplay, args=(0, 255, 0, 0.5))
    blinkThread.do_run = True
    blinkThread.start()
    setTimestamp()
    return render_template("index.html", available="available", shutdown=globalShutdown)

@app.route('/away', methods=['POST'])
def awayCall():
    global globalShutdown, globalLastCalledApi, blinkThread
    if globalShutdown:
        return render_template("index.html", shutdown=globalShutdown)
    globalLastCalledApi='Frontend: Away'
    switchOff()
    blinkThread = threading.Thread(target=setDisplay, args=(255, 255, 0, 0.5))
    blinkThread.do_run = True
    blinkThread.start()
    setTimestamp()
    return render_template("index.html", away="away", shutdown=globalShutdown)

@app.route('/rainbow', methods=['POST'])
def rainbowCall():
    global blinkThread, globalLastCalledApi
    if globalShutdown:
        return render_template("index.html", shutdown=globalShutdown)
    globalLastCalledApi='Frontend: Rainbow'
    switchOff()
    blinkThread = threading.Thread(target=displayRainbow, args=(1, 0.5, 0.2, None, 0))
    blinkThread.do_run = True
    blinkThread.start()
    setTimestamp()
    return render_template("index.html", rainbow="rainbow", shutdown=globalShutdown)

@app.route('/shutdown', methods=['POST'])
def shutdownCall():
    global globalShutdown, globalLastCalledApi, globalBlue, globalGreen, globalRed
    if globalShutdown:
        return render_template("index.html", shutdown=globalShutdown)
    globalLastCalledApi='Frontend: Shutdown'
    switchOff()
    shutdownPi()
    setTimestamp()
    return render_template("index.html", shutdown=globalShutdown)

@app.route('/cancel-shutdown', methods=['POST'])
def cancelShutdownCall():
    global globalShutdown, globalLastCalledApi, globalBlue, globalGreen, globalRed
    globalLastCalledApi='Frontend: Cancel Shutdown'
    switchOff()
    cancelShutdown()
    setTimestamp()
    return render_template("index.html", off="off", shutdown=globalShutdown)

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
