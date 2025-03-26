"""
ECEG 201 Fall 2024

PINS IN USE
>NeoPixel
->board.D5 (within neoPixelFunctions library)
>Hall effect sensor
->board.D16 (A2)

This script will test the four integrated hardware units on your DAMNED PCB:
the ESP WiFi, the NeoPixel RGB LED ring, the stepper motor, and the Hall sensor
We will use several custom libraries created for this course as well as several
standard Adafruit CircuitPython libraries
"""
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

#Here I'm doing setup and just doing everything that only needs/should be done once

#NeoPixel brightness level (0 - 1.0)
NEO_BRIGHTNESS = 0.8
neoFun.set_brightness(NEO_BRIGHTNESS)

#Create a motor object
kit = MotorKit()
# define the input for the Hall effect sensor.  This is hardwired to D16 (A2) of the Feather
# the Hall sensor output is typicall high
# in the presence of a magnetic field the Hall sensor output is low
Hall = DigitalInOut(board.D16)
Hall.direction = Direction.INPUT

# create edge detectors for the range where the magnet triggers the Hall sensor
edge1 = 0
edge2 = 0
# step counter for motor
stepCount = 0


# turn off any LEDs that may have been left on from the previous code execution
neoFun.set_ring_color((0,0,0))


print('\n---------------------------------------\n')
print('Begin NeoPixel ring functionality test.')
print('\n---------------------------------------\n')
#The ring should turn red, then green, then blue
#This confirms all three elements of each LED are working
neoFun.set_ring_color((200,0,0))
time.sleep(0.5)
neoFun.set_ring_color((0,200,0))
time.sleep(0.5)
neoFun.set_ring_color((0,0,200))
time.sleep(0.5)
neoFun.set_ring_color((0,0,0))
time.sleep(0.5)
#Flash the neoPixel to indicate that NeoPixel startup is done
for x in range(10):
    neoFun.set_ring_color((0,0,0))
    time.sleep(.05)
    neoFun.set_ring_color((0,20,0))
    time.sleep(.05)
    neoFun.set_ring_color((0,0,0))
    x -= 1
print('\n---------------------------------------\n')
print('End NeoPixel ring functionality test.')
print('\n---------------------------------------\n')
time.sleep(2)

# create a function to set up and test the WiFi functionality
def wifiTest():
    print("ESP32-S3 WebClient Test")

    print(f"My MAC address: {[hex(i) for i in wifi.radio.mac_address]}")

    print("Available WiFi networks:")
    for network in wifi.radio.start_scanning_networks():
        print("\t%s\t\tRSSI: %d\tChannel: %d" % (str(network.ssid, "utf-8"),
                                             network.rssi, network.channel))
    wifi.radio.stop_scanning_networks()

    print(f"Connecting to {os.getenv('CIRCUITPY_WIFI_SSID')}")
    wifi.radio.connect(os.getenv("CIRCUITPY_WIFI_SSID"), os.getenv("CIRCUITPY_WIFI_PASSWORD"))
    print(f"Connected to {os.getenv('CIRCUITPY_WIFI_SSID')}")
    print(f"My IP address: {wifi.radio.ipv4_address}")

    ping_ip = ipaddress.IPv4Address("8.8.8.8")
    ping = wifi.radio.ping(ip=ping_ip)

    # retry once if timed out
    if ping is None:
        ping = wifi.radio.ping(ip=ping_ip)

    if ping is None:
        print("Couldn't ping 'google.com' successfully")
    else:
        # convert s to ms
        print(f"Pinging 'google.com' took: {ping * 1000} ms")

    pool = socketpool.SocketPool(wifi.radio)
    requests = adafruit_requests.Session(pool, ssl.create_default_context())

    return pool, requests

print("Now testing WiFi")
pool, requests = wifiTest()
print('\n---------------------------------------\n')
print("WiFi test complete.")
print('\n---------------------------------------\n')

print('\n---------------------------------------\n')
print("Begin testing Hall sensor / home motor arm.")
print('\n---------------------------------------\n')

while True:
    kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    if Hall.value:
        neoFun.set_ring_color((255,0,0))
        #print("i = ",i," INACTIVE")
    else:
        neoFun.set_ring_color((0,255,0))
        print("Initial edge detected!")
        #time.sleep(2)
        #print("i = ",i," ACTIVATED")
        break

# motor has paused at the end of the Hall sensor, in theory
# move back several steps which should eliminate the magnetic field/Hall active edge
# 20 steps was chosen because after testing multiple times it was found that the
# active zone was never more than about 14.  20 seemed like a safe bet in case
# the first edge was detected at the *end* of the Hall active zone
for i in range(20):
    kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)

# now step forward, SLOWLY (with pauses between each step) and locate the two edges
# of the active Hall zone
for i in range(45):
    if Hall.value:
        neoFun.set_ring_color((255,0,0))
        if edge1 != 0 and edge2 == 0:
            edge2 = stepCount - 1
            print("Edge2 found!")
            #time.sleep(2)
            break
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        stepCount = stepCount + 1
        time.sleep(0.5)
    else:
        neoFun.set_ring_color((0,255,0))
        if edge1 == 0:
            edge1 = stepCount
            print("Edge1 found!")
            #time.sleep(2)
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
        stepCount = stepCount + 1
        time.sleep(0.5)
    if i == 44:
        if edge2 == 0:
            print("Edge2 never found!")

home = edge2 - edge1
print("Found home to be ",home," steps")

# move the motor arm CCW back "home" steps
# but remove four steps due to hysterisus
for i in range(home-4):
    kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)

time.sleep(0.1)

# move back to 12 o'clock position
for i in range(50):
    kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)

# sleep briefly just to make sure the motor arm has settled and it doesn't move from home
time.sleep(0.5)
# release the motor (deenergize coils) to eliminate current draw and heating
kit.stepper1.release()

print('\n---------------------------------------\n')
print('Congratulations!  Your DAMNED passed all tests and is fully functional.')
print('\n---------------------------------------\n')


print('\n---------------------------------------\n')
print('Now entering infinite loop to animate LEDs.')
print('\n---------------------------------------\n')


# now run in an infinite loop of snake animations
while(1):
    neoFun.animate_snake((0,20,188),6,0,24)
    #myMotor.move_arm_degrees(360)
    neoFun.animate_snake((255,20,0),6,0,24)
    #myMotor.move_arm_degrees(-360)
