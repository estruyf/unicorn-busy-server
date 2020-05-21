from time import sleep
from lib.unicorn_wrapper import UnicornWrapper

print("Starting Unicorn test...")
unicorn = UnicornWrapper()

print("Starting rainbow test (will take 36 seconds...")
hue = 0
while hue <= 360:
    unicorn.setColour(RGB = unicorn.hsvIntToRGB(hue,100,100))
    sleep(0.1)
    hue = hue + 1
print("Starting white test (will take 5 seconds...")
unicorn.setColour(255,255,255)
sleep(5)
unicorn.clear()
unicorn.show()

print("Unicorn test complete")