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


#Define I/O pins for game inputs
Twist = DigitalInOut(board.D16)
Twist.direction = Direction.INPUT

Spin = DigitalInOut(board.D17)
Spin.direction = Direction.INPUT

Button = analogio.AnalogIn(board.A1)


#Setup for peripherals
kit = MotorKit()

i2s_tx = board.TX
i2s_clock = board.D10
i2s_word_select = board.D11

#Initialize variables
score = 0
game_over = False
current_level = 1
timeput_duration = 3
last_hall_command = None

#1,2,3 are analog buttons 4,5 are hall effect sensors
commands = ["bop", "pull", "flick", "twist", "spin"]

