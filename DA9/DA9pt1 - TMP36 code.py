# ECEG 201
# DA9 TMP36 testing
#
# if you need a refresher you can find information on Circuit Python here
# https://learn.adafruit.com/welcome-to-circuitpython/overview
# https://learn.adafruit.com/circuitpython-essentials

# first load the libraries we need.
# https://learn.adafruit.com/welcome-to-circuitpython/circuitpython-libraries
#
# Note that the ESP32-S3 has analog in channels (ADC, or analog to digital converter)
# but it does NOT have a DAC (digital to analog converter).  Hence, our Feather
# cannot output true analog signals.  Forunately, we do not need to output an analog
# signal here, just a binary "high" or "low" so we'll repurpose one of the analog "Ax"
# pins on the DAMNED PCB to act as a digital pin.  
import time
import board
from analogio import AnalogIn
from digitalio import DigitalInOut, Direction
import neopixelFunctions  # import functions to light the ring

analog_in = AnalogIn(board.A1)  # set the analog input pin to A1
digital_out = DigitalInOut(board.D18) # D18 is shared with A0
digital_out.direction = Direction.OUTPUT
# Curious about why D18 is the same thing as A0?  Check out this link:
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-pins-and-modules


# Here we use one of the example circuit python scripts to create our own function
# https://learn.adafruit.com/circuitpython-essentials/circuitpython-analog-in
# Convert the digital value to a voltage...
# Since the analog to digital converter on the ESP32-S3 has 12 bits of resoltuion,
# a voltage of 0V gives 0 and the maximum voltage of 3.3 V should give 2^12 = 4096.
# However CircuitPython scales all inputs to 16 bits, 2^16 = 65536.
# Read more about that:
# https://docs.circuitpython.org/en/latest/shared-bindings/analogio/index.html#analogio.AnalogIn
def get_voltage(pin):
    return (pin.value * 3.3) / 65536
def tmp36c(voltage):
    """
    Converts the voltage reading from a TMP36 temperature sensor to Celsius.

    The TMP36 provides a voltage output that is linearly proportional to the
    temperature in Celsius.  The formula to convert voltage to Celsius is:

        Celsius = (Voltage - 0.5V) / 0.01V/°C

    Args:
        voltage (float): The voltage reading from the TMP36 sensor in volts.

    Returns:
        float: The temperature in degrees Celsius.
    """
    celsius = (voltage - 0.5) / 0.01
    return celsius

def tmp36f(voltage):
    """
    Converts the voltage reading from a TMP36 temperature sensor to Fahrenheit.

    This function first converts the voltage to Celsius and then converts
    the Celsius temperature to Fahrenheit using the standard formula:

        Fahrenheit = (Celsius * 9/5) + 32

    Args:
        voltage (float): The voltage reading from the TMP36 sensor in volts.

    Returns:
        float: The temperature in degrees Fahrenheit.
    """
    celsius = tmp36c(voltage)  # Reuse the Celsius conversion
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

while True:  # loop forever
    # this next section averages the signal "avg" times to get rid of noise.
    # The noise will be reduced by sqrt(sum).
    # Try to change the value of "avg" and see how it affects the readings you get.
    x = 0   # set counter value to zero
    avg = 200
    for m in range(1, avg):   # loop avg times adding a new reading each time
        x = x + get_voltage(analog_in)  # add the voltage
        time.sleep(.001)  # pause for a brief moment to let voltage change
    meas = x/avg
    # divide by the number of measurements to get the average
    # note that this is just one way to clean up noise on inputs and it is
    # expensive in terms of processing time and power.
	# Note also that this slows down the measurement so if you are looking at
	# changing signals it can create odd effects.  Is this a problem for the
	# ramp test you are asked to do?

    # The print and delay are debugging statements you can comment
    # out after you get things working.  Look at the measured
    # value on the serial window.
    print(meas)
    print(tmp36c(meas))
    print(tmp36f(meas))
    time.sleep(0.005) # pause for half a second

    # Now we are going to see if the measured value is above the threshold and
    # if it is, turn on the LED ring by calling a predefined function and toggle
    # a digital output pin high.
    setval = 1.5   # the voltage value to debug the initial circuit
    """if meas > setval:
        digital_out.value = True # set the digital output high
        neopixelFunctions.set_ring_color((255,255,255)) # turn on the LED ring
        neopixelFunctions.set_brightness(0.3)
    else:
        digital_out.value = False # set the digital output low
        neopixelFunctions.set_ring_color((0,0,0))  # turn the LED ring off
    """

    if (tmp36f(meas)) > 85: # Check if the Measured temperature in deg F is greater than 85
        print(chr(sum(range(ord(min(str(not())))))))
        digital_out.value = True # set the digital output high
        neopixelFunctions.set_ring_color((255,255,255)) # turn on the LED ring
        neopixelFunctions.set_brightness(0.3)
    else:
        digital_out.value = False # set the digital output low
        neopixelFunctions.set_ring_color((0,0,0))  # turn the LED ring off