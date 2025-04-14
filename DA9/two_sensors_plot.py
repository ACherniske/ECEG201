import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.cbook as cbook

"""root = tk.Tk()
root.withdraw()

file_pathDA9 = filedialog.askopenfilename(title="Select DA9 Data File")
if file_pathDA9:
    with cbook.get_sample_data(file_pathDA9) as file:
        DA9data = np.loadtxt(file, delimiter=',')
"""
DA9data = np.loadtxt(r"DA9\two_sensors.csv", delimiter=',')

time = DA9data[:, 0]
AHTTemp = DA9data[:, 1]
MCPTemp = DA9data[:, 2]
AHTSTD, AHTMEAN, AHTCV = np.std(AHTTemp), np.mean(AHTTemp), np.std(AHTTemp) / np.mean(AHTTemp) * 100
MCPSTD, MCPMEAN, MCPCV = np.std(MCPTemp), np.mean(MCPTemp), np.std(MCPTemp) / np.mean(MCPTemp) * 100
AHTCoefficients = np.polyfit(time[0:119], AHTTemp[0:119], 1)
MCPFCoefficients = np.polyfit(time[0:119], MCPTemp[0:119], 1)
AHTDrift = AHTCoefficients[0]
MCPDrift = MCPFCoefficients[0]
AHTFit = np.poly1d(AHTCoefficients)
MCPFit = np.poly1d(MCPFCoefficients)

# --- Figure 1: Temperature Plot ---
fig1, ax1 = plt.subplots()  # Create the first figure and axes
ax1.plot(time, MCPTemp, label='MCP9808')
ax1.plot(time, AHTTemp, label='AHT20')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Temperature (°C)')
ax1.grid(True)
ax1.set_title('Temperature (°C) of MCP9808 and AHT20', fontweight='bold')
ax1.legend()

# --- Figure 2: Baseline Data Plot ---
fig2, ax2 = plt.subplots()  # Create the second figure and axes
ax2.plot(time[0:119],MCPTemp[0:119], label='MCP9808', color='blue')
ax2.plot(time[0:119],AHTTemp[0:119], label='AHT20', color='red')
ax2.text(0.1, 0.45, f'Coefficient of Variation AHT20: {round(AHTCV, 2)}%', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
ax2.text(0.1, 0.68, f'Coefficient of Variation MCP9808: {round(MCPCV, 2)}%', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
ax2.text(0.1, 0.5, f'Drift of AHT20: {round(AHTDrift*60, 3)} °C/min', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
ax2.text(0.1, 0.73, f'Drift of MCP9808: {round(MCPDrift*60, 3)} °C/min', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
ax2.plot(time[0:119], MCPFit(time[0:119]), label='MCP9808 Fit', color='blue', linestyle='--')
ax2.plot(time[0:119], AHTFit(time[0:119]), label='AHT20 Fit', color='red', linestyle='--')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Temperature (°C)')
ax2.grid(True)
ax2.set_title('Baseline Temperature (°C) of MCP9808 and AHT20', fontweight='bold')
ax2.legend()

# --- Figure 3: Response Time ---    

AHTMaxIndex = np.argmax(AHTTemp)
AHTMinIndex = np.argmin(AHTTemp) #index of min temp of AHTTemp
norm_AHTTemp = (AHTTemp - AHTTemp[AHTMinIndex]) / (AHTTemp[AHTMaxIndex] - AHTTemp[AHTMinIndex])

offset = np.mean(AHTTemp[0:119])
norm_Offset = (offset - AHTTemp[AHTMinIndex]) / (AHTTemp[AHTMaxIndex] - AHTTemp[AHTMinIndex])

temptau = (norm_Offset+1/np.e) * (AHTTemp[AHTMaxIndex] - AHTTemp[AHTMinIndex]) + AHTTemp[AHTMinIndex]

closest_index = -1
minDifference = float("inf")
for i in range(AHTMaxIndex, 299):
    difference = abs(AHTTemp[i] - temptau)
    if difference < minDifference:
        minDifference = difference
        closest_index = i


fig3, ax3 = plt.subplots()  # Create the third figure and axes
ax3.plot((time[AHTMaxIndex:299]-AHTMaxIndex)/(np.max(time)-AHTMaxIndex), norm_AHTTemp[AHTMaxIndex:299], label='AHT20', color='blue')
ax3.axhline(norm_Offset, color='green', linestyle='--', label='Offset')
ax3.axhline(norm_Offset+(1/np.e), color='red', linestyle='--', label='1/e point')
ax3.axvline((time[closest_index]-AHTMaxIndex)/(np.max(time)-AHTMaxIndex), color='red', linestyle='--', label='1/e point')


ax3.set_ylim(0,1)
ax3.set_xlim(0,1)


plt.show()
#else:
   #print("No file selected.")