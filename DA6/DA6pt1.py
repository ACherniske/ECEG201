import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()

with cbook.get_sample_data(file_path) as file:
    data = np.loadtxt(file,delimiter=';')


plt.plot(data[:,0],data[:,1])
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid()
plt.title('Simulated LDO Voltage (Turn-on)', fontweight='bold')
plt.show()