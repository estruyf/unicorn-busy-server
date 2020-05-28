#!/usr/bin/env python
import contextlib
import io
import colorsys
import spidev
import unicornhat
from unicornhatmini import UnicornHATMini

class UnicornWrapper:
    def __init__(self, hat = None):
        if hat is None:
            try:
                spidev.SpiDev(0,0)
                hat = 'mini'
            except FileNotFoundError:
                hat = 'phat'

        if hat == 'mini':
            self.hat = UnicornHATMini()
            self.type = hat
            self.hat.set_brightness(0.5)
            self.hat.set_rotation(90)
        elif hat == 'dummy':
            self.hat = None
            self.type = 'none'
        else:
            self.hat = unicornhat
            self.type = hat
            self.hat.set_layout(unicornhat.PHAT)
            self.hat.brightness(0.5)
            self.hat.rotation(90)
        self.brightness = 0.5
        self.rotation = 0
        self.width, self.height = self.hat.get_shape()

    def getType(self):
        return self.type

    def getHat(self):
        return self.hat

    def clear(self):
        return self.hat.clear()

    def getShape(self):
        return self.hat.get_shape()

    def setAll(self, r, g, b):
        self.hat.set_all(r, g, b)

    def getBrightness(self):
        if self.type == 'phat':
            return self.hat.get_brightness()
        
        return self.brightness
    
    def setBrightness(self, brightness):
        self.brightness = brightness

        if self.type == 'phat':
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                self.hat.brightness(brightness)
        elif self.type == 'mini':
            self.hat.set_brightness(brightness)
    
    def setPixel(self, x, y, r, g, b):
        self.hat.set_pixel(x, y, r, g, b)
    
    def setColour(self, r = None, g = None, b = None, RGB = None):
        if RGB is not None:
            r = RGB[0]
            g = RGB[1]
            b = RGB[2] 
        self.hat.clear()
        for x in range(self.width):
            for y in range(self.height):
                self.setPixel(x, y, r, g, b)
        self.hat.show()
    
    def setRotation(self, r=0):
        if self.type == 'phat':
            self.hat.rotation(r)
        elif self.type == 'mini':
            self.hat.set_rotation(r)
        self.rotation = r
    
    def getRotation(self):
        return self.rotation
    
    def show(self):
        self.hat.show()

    def off(self):
        self.hat.clear()
        self.hat.show()
    
    # Colour converstion operations as we only understand RGB
    def hsvIntToRGB(self, h, s, v):
        h = h / 360
        s = s /100
        v = v / 100
        return tuple(round(i * 255) for i in colorsys.hsv_to_rgb(h,s,v))
    
    def htmlToRGB(self, html):
        if len(html) is 6:
            r = int(f"{html[0]}{html[1]}", 16)
            g = int(f"{html[2]}{html[3]}", 16)
            b = int(f"{html[4]}{html[5]}", 16)
        elif len(html) > 6:
            r = int(f"{html[1]}{html[2]}", 16)
            g = int(f"{html[3]}{html[4]}", 16)
            b = int(f"{html[5]}{html[6]}", 16)
        else:
            raise Exception("The Hex value is not in the correct format it should RRGGBB or #RRGGBB the same as HTML")
        return tuple(r,g,b)
