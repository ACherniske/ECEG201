# ECEG 201
# DA9 I2C sensor testing

import time
import board
import busio
import adafruit_mcp9808  # load MCP9808 sensor library
import adafruit_ahtx0   # load AHT20 sensor library

# initialize the I2C bus
i2c = board.I2C()

# initialize sensors using the imported libraries
mcp = adafruit_mcp9808.MCP9808(i2c)
aht = adafruit_ahtx0.AHTx0(i2c)


bogus = 1   # This is used to halt execution later
while bogus == 1:
    # Now we'll capture data from both sensors
    # This next step pauses the code and waits for you to start your I2C monitor
    # Once you've got that running, hit any key in the CircuitPython serial monitor to continue
    # with the I2C temperature read
    input('Start your protocol analyzer monitoring.  When you\'re ready, press Enter to continue.')
    x = mcp.temperature  # read the temperature from the MCP9808
    y = aht.temperature  # read the temperature from the AHT20
    # Print out the data on the serial monitor
    #print('MCP9808 Temperature: ', x, '°C')
    print('MCP9808 Temperature: ', round(x,1), '°C')
    print('AHT20 Temperature: ', round(y,1), '°C')
    tempF = x * 9 / 5 + 32
    print('MCP9808 Temperature: {} °C / {} °F '.format(round(x,1), round(tempF,1)))
    print('AHT20 Temperature: {} °C / {} °F '.format(round(y,1), round(y * 9 / 5 + 32,1)))
    bogus = 0