def init();
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