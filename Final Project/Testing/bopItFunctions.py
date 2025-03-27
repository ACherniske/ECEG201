def get_voltage(pin): # Specify Analog Pin
    return (pin.value * 3.3) / 65536  # Convert 16-bit analog reading to voltage

def home_Motor():
    while Hall.value:
        #neoFun.set_ring_color((255,0,0)) Commented out Implementation
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

    #neoFun.set_ring_color((0,255,0)) Commented out Implementation
    kit.stepper1.release()

def read_3_buttons(analog_read_function, thresholds=(1.0, 1.5, 2.0)): # (0,1,2)
    voltage = analog_read_function()
    button_pressed = None  # Initialize button_pressed to None

    if voltage >= thresholds[2]:
        button_pressed = 1
    elif thresholds[1] <= voltage < thresholds[2]:
        button_pressed = 2
    elif thresholds[0] <= voltage < thresholds[1]:
        button_pressed = 3

    return button_pressed
