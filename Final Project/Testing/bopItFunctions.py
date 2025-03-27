from digitalio import DigitalInOut, Direction, Pull
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

Hall = DigitalInOut(board.D16)
Hall.direction = Direction.INPUT
kit = MotorKit()
analog_in = analogio.AnalogIn(board.A1)

def get_voltage(pin): # Specify Analog Pin
    return (pin.value * 3.3) / 65536  # Convert 16-bit analog reading to voltage

def home_Motor():
    while Hall.value:
        #neoFun.set_ring_color((255,0,0)) Commented out Implementation
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

    #neoFun.set_ring_color((0,255,0)) Commented out Implementation
    kit.stepper1.release()

def detect_Button(analog_read_function, thresholds=(1.0, 1.5, 2.0)): # (0,1,2)
    # ex. detect_Button(get_voltage(analog_in), (1.0, 1.5, 2.0))
    voltage = analog_read_function()
    button_pressed = None  # Initialize button_pressed to None

    if voltage >= thresholds[2]:
        button_pressed = 1
    elif thresholds[1] <= voltage < thresholds[2]:
        button_pressed = 2
    elif thresholds[0] <= voltage < thresholds[1]:
        button_pressed = 3

    return button_pressed
