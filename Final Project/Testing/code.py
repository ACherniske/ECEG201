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

while True:
    bopIt.home_Motor()
    time.sleep(0.1)