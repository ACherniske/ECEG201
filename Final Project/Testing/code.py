import os
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import board
import time
from digitalio import DigitalInOut, Direction, Pull
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import neoPixelFunctions as neoFun
import bopItFunctions as bopIt
import audiocore
import audiobusio
import analogio

analog_in = analogio.AnalogIn(board.A1)

while True:
    voltage = bopIt.get_voltage(analog_in)
    print("Voltage: {:.2f} V".format(voltage))

    if voltage >= 2.0:
        print("Button 1")
    elif voltage >= 0.75 and voltage < 2.0:
        print("Button 2")
    elif voltage >= 0.2 and voltage < 0.75:
        print("Button 3")
    else:
        print("None")

    time.sleep(0.1)  # Wait for 0.5 seconds before the next reading


