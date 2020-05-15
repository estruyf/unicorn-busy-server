import time
import spidev
import unicornhat
from unicornhatmini import UnicornHATMini

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
        else:
            self.hat = None
            self.type = 'none'
        self.brightness = 0.5
        self.rotation = 0
    
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

if unicornmini:
        unicorn = UnicornWrapper('mini')
else:
        unicorn = UnicornWrapper('phat')

#get the width and height of the hardware
width, height = unicorn.get_shape()

r=255
g=0
b=0
unicorn.clear()
for y in range(height):
    for x in range(width):
        unicorn.set_pixel(x, y, r, g, b)
unicorn.show()
time.sleep(5)