import time
import board
import analogio

# Setup the analog input pin
analog_in = analogio.AnalogIn(board.A1)

def get_voltage(pin):
    """Returns the voltage from the specified analog pin."""
    return (pin.value * 3.3) / 65536  # Convert 16-bit analog reading to voltage

while True:
    voltage = get_voltage(analog_in)
    print("Voltage: {:.2f} V".format(voltage)) #print voltage with 2 decimal points
    time.sleep(0.5)  # Wait for 0.5 seconds before the next reading


import time
import board
import analogio
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

# Setup the analog input pin
analog_in = analogio.AnalogIn(board.A1)
kit = MotorKit()

def get_voltage(pin):
    """Returns the voltage from the specified analog pin."""
    return (pin.value * 3.3) / 65536  # Convert 16-bit analog reading to voltage

while True:
    voltage = get_voltage(analog_in)
    print("Voltage: {:.2f} V".format(voltage)) #print voltage with 2 decimal points
    time.sleep(0.1)  # Wait for 0.5 seconds before the next reading
    if voltage*10 >= 1:
        print("spinning")
    else: 
        print("not spinning")

analog_in = analogio.AnalogIn(board.A1)

while True:
    voltage = bopIt.get_voltage(analog_in)
    print("Voltage: {:.2f} V".format(voltage))

    if voltage >= 2.0:
        print("Bop It")
    elif voltage >= 0.75 and voltage < 2.0:
        print("Pull It")
    elif voltage >= 0.2 and voltage < 0.75:
        print("Flick It")
    else:
        print("None")

    time.sleep(0.1)  # Wait for 0.5 seconds before the next reading