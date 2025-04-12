import time
import board
import busio
import digitalio
import adafruit_mcp9808   # load MCP9808 sensor library
import adafruit_ahtx0    # load AHT20 sensor library

# initialize sensors from the imported modules
i2c = board.I2C()
mcp = adafruit_mcp9808.MCP9808(i2c)
aht = adafruit_ahtx0.AHTx0(i2c)

# define a write enable toggle GPIO pin
switch = digitalio.DigitalInOut(board.D9)
# set the digital pin as receiving input
switch.direction = digitalio.Direction.INPUT
# set the pin to pull high if nothing is connected
switch.pull = digitalio.Pull.UP

# create a new file on the Feather to store our sensor data
f = open('two_sensors.csv', 'a')

# This next loop captures 30 data points, one every second.  Change the values
# in the range() statement and time.sleep to change data acquisition parameters
for m in range(30):
    x = aht.temperature  # read the AHT20 temperature
    y = mcp.temperature   # read the MCP9808 temperature
    # print the measurements in the serial monitor
    print('Second: ', m)
    print('AHT20 Temperature: ', x, '°C')
    print('MCP9808 Temperature: ', y, '°C')
    # write the measurements to the CSV file you created on the Feather
    # separate time and the two measurements by commas
    f.write(str(m))
    f.write(", ")
    f.write(str(x))
    f.write(", ")
    f.write(str(y))
    f.write("\n")   # write a new line character
    time.sleep(1)  # hold until time to collect next point
f.close()