import gpiozero as gpio
import signal
import os

relay = gpio.LED(23)
power = gpio.Button(22, pull_up=False)

print('taking control of relay')
relay.on()

def unplugged():
    power.when_deactivated = None
    print('power unplugged')
    os.system("pkill midori")
    os.system("(sleep 1 && sudo shutdown now) &")

power.when_deactivated = unplugged
signal.pause()
