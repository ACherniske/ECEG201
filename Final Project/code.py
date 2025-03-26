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
    print("Voltage: {:.2f} V".format(voltage))

    if voltage >= 2.0:
        print("Button 1")
    elif voltage >= 1.5 and voltage < 2.0:
        print("Button 2")
    elif voltage >= 1.0 and voltage < 1.5:
        print("Button 3")
    else:
        print("None")

    time.sleep(0.5)  # Wait for 0.5 seconds before the next reading