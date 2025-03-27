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

Hall = DigitalInOut(board.D16)
Hall.direction = Direction.INPUT
kit = MotorKit()

"""while True:
    if Hall.value:
        neoFun.set_ring_color((255,0,0))
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    else:
        neoFun.set_ring_color((0,255,0))
        kit.stepper1.release()
"""
def home_Motor():
    while Hall.value:
        neoFun.set_ring_color((255,0,0))
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

    neoFun.set_ring_color((0,255,0))
    kit.stepper1.release()

while True:
    home_Motor()