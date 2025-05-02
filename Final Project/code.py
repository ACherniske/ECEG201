import os
import board
import ipaddress
import ssl
import wifi
import socketpool
import adafruit_requests
import time
import random
from digitalio import DigitalInOut, Direction, Pull
import analogio
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper
import audiocore
import audiobusio
import BopItFunc
import wifiFunctions as WifiFunc
import neoPixelFunctions as NeoFunc

# Wifi/Thingspeak Setup
internet = WifiFunc.wifiObject()
THINGSPEAK_CHANNEL = '2945278'
THINGSPEAK_API_KEY = '4NDZLK80SP9ORQ21'

# Neopixel Setup
NEO_Brightness = 0.9
NeoFunc.set_brightness(NEO_Brightness)

# Audio Setup
i2s_tx=board.TX, 
i2s_clock=board.D10, 
i2s_word_select=board.D11

# Input Setup
AButton = analogio.AnalogIn(board.A0)

Spin = DigitalInOut(board.A1)
Spin.direction = Direction.INPUT

Twist = DigitalInOut(board.A2)
Twist.direction = Direction.INPUT

# Motor Setup
kit = MotorKit()

# --- Action Map ---
ACTION_MAP = {
    0: "NONE",
    1: "BOP",
    2: "PULL",
    3: "FLICK",
    4: "TWIST",  # hall_1
    5: "SPIN"   # hall_2
}

seed, max_index = BopItFunc.generate_seed()

print("Now testing WiFi")
pool, requests = BopItFunc.wifiTest()
print('\n---------------------------------------\n')
print("WiFi test complete.")
print('\n---------------------------------------\n')

BopItFunc.idle_state(AButton, Spin, Twist)

