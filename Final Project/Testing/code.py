import time
import board
import analogio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
import neoPixelFunctions as neoFun

neoFun.set_ring_color((0,0,0))

kit = MotorKit()

Hall = DigitalInOut(board.D16)
Hall.direction = Direction.INPUT

while True:
    if Hall.value:
        neoFun.set_ring_color((255,0,0))
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)
    else:
        neoFun.set_ring_color((0,255,0))
        kit.stepper1.release()
