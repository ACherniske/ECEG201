import matplotlib
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

root = tk.Tk()
root.withdraw()

# first load the DA5 data into a variable
# this data should be from an oscilloscope that uses a comma as a delimiter
file_pathDA5 = filedialog.askopenfilename()
with cbook.get_sample_data(file_pathDA5) as file:
    DA5data = np.loadtxt(file,delimiter=',')

# next, load the DA1 data into a variable
# this data should be from a KiCad which uses a semicolon as a delimiter
file_pathDA1 = filedialog.askopenfilename()
with cbook.get_sample_data(file_pathDA1) as file:
    DA1data = np.loadtxt(file,delimiter=';')

plt.subplot(211)

timeDA5 = DA5data[:,0]
voltageDA5 = DA5data[timeDA5>0,2]
timeDA5 = timeDA5[timeDA5>0]

plt.plot(timeDA5,voltageDA5)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid()
plt.title('Measured LDO Voltage (Turn-on)', fontweight='bold')

plt.subplot(212)

timeDA1 = DA1data[:,0]
voltageDA1 = DA1data[:,1]
plt.plot(timeDA1,voltageDA1)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid()
plt.title('Simulated LDO Voltage (Turn-on)', fontweight='bold')

plt.suptitle('Measured vs Simulated turn on time of Damned LDO', fontweight='bold')

plt.show()