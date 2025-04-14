import matplotlib
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()
with cbook.get_sample_data(file_path) as file:
    data = np.loadtxt(file,delimiter=',')

time = data[:,0]
voltage = data[:,1]
ACcoupledVoltage = voltage - np.mean(voltage)
np.square(ACcoupledVoltage)
np.mean(np.square(ACcoupledVoltage))
Vrms = np.sqrt(np.mean(np.square(ACcoupledVoltage)))

plt.plot(time,ACcoupledVoltage)
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.text(1.4e-08,0.0729,'Vrms = ' + str(round(Vrms*1000,2)) + 'mV')
plt.grid()
plt.title('Output Ripple Voltage', fontweight='bold')
plt.show()