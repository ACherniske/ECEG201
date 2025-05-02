import BopItFunc
import analogio
from digitalio import DigitalInOut, Direction, Pull
import board
import time

buttons = analogio.AnalogIn(board.A0)
Hall1 = DigitalInOut(board.A1)
Hall1.direction = Direction.INPUT
Hall1.pull = Pull.UP
Hall2 = DigitalInOut(board.A2)
Hall2.direction = Direction.INPUT
Hall2.pull = Pull.UP


while True:
    get_Voltage = (buttons.value * 3.3) / 65536  # Convert 16-bit analog reading to voltage
    print(get_Voltage)

"""def wait(button, Hall1, Hall2):
    while True:
        button = BopItFunc.detect_Button(BopItFunc.get_voltage(button), (.2, .7, 1.2))
        if button != 0:
            return button
        hall_value = BopItFunc.detect_hall(Hall1, Hall2)
        if hall_value != 0:
            return hall_value
        time.sleep(0.1)

while True:
    inputs = wait(buttons, Hall1, Hall2)
    print("Inputs: ", inputs)
    hall = BopItFunc.detect_hall(Hall1, Hall2)
    print("Hall: ", hall)
    time.sleep(0.1)"""