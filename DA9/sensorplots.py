import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import filedialog
import matplotlib.cbook as cbook


root = tk.Tk()
root.withdraw()

file_pathDA9 = filedialog.askopenfilename(title="Select DA9 Data File")
if file_pathDA9:
    with cbook.get_sample_data(file_pathDA9) as file:
        DA9data = np.loadtxt(file, delimiter=',')

    DA9data = np.loadtxt(r"DA9\two_sensors.csv", delimiter=',')

    time = DA9data[:, 0]
    ahtTemp = DA9data[:, 1]
    mcpTemp = DA9data[:, 2]

    # --- Figure 1: Temperature Plot ---
    fig1, ax1 = plt.subplots()  # Create the first figure and axes
    ax1.plot(time, mcpTemp, label='MCP9808',color='blue')
    ax1.plot(time, ahtTemp, label='AHT20', color='red')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Temperature (°C)')
    ax1.grid(True)
    ax1.set_title('Temperature (°C) of MCP9808 and AHT20', fontweight='bold')
    ax1.legend()

    # --- Figure 2: Baseline Data Plot ---

    # Standard Deviation, Mean, Coefficient of Variation

    ahtSTD, ahtMEAN, ahtCV = np.std(ahtTemp), np.mean(ahtTemp), np.std(ahtTemp) / np.mean(ahtTemp) * 100
    mcpSTD, mcpMEAN, mcpCV = np.std(mcpTemp), np.mean(mcpTemp), np.std(mcpTemp) / np.mean(mcpTemp) * 100 

    # Drift Calculation
    ahtCoefficients = np.polyfit(time[0:119], ahtTemp[0:119], 1)
    mcpCoefficients = np.polyfit(time[0:119], mcpTemp[0:119], 1)

    ahtDrift = ahtCoefficients[0]
    mcpDrift = mcpCoefficients[0]

    # Fit the data to a polynomial
    ahtFit = np.poly1d(ahtCoefficients)
    mcpFit = np.poly1d(mcpCoefficients)

    fig2, ax2 = plt.subplots()  # Create the second figure and axes
    ax2.plot(time[0:119],mcpTemp[0:119], label='MCP9808', color='blue')
    ax2.plot(time[0:119],ahtTemp[0:119], label='AHT20', color='red')
    ax2.text(0.1, 0.45, f'Coefficient of Variation AHT20: {round(ahtCV, 2)}%', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
    ax2.text(0.1, 0.68, f'Coefficient of Variation MCP9808: {round(mcpCV, 2)}%', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
    ax2.text(0.1, 0.5, f'Drift of AHT20: {round(ahtDrift*60, 3)} °C/min', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
    ax2.text(0.1, 0.73, f'Drift of MCP9808: {round(mcpDrift*60, 3)} °C/min', transform=plt.gca().transAxes, fontsize=10, verticalalignment='top')
    ax2.plot(time[0:119], mcpFit(time[0:119]), label='MCP9808 Fit', color='blue', linestyle='--')
    ax2.plot(time[0:119], ahtFit(time[0:119]), label='AHT20 Fit', color='red', linestyle='--')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Temperature (°C)')
    ax2.grid(True)
    ax2.set_title('Baseline Temperature (°C) of MCP9808 and AHT20', fontweight='bold')
    ax2.legend()

    # --- Figure 3: Response Time ---

    ahtMaxIndex = np.argmax(ahtTemp) # Index of the maximum value for AHT20
    ahtMinIndex = np.argmin(ahtTemp) # Index of the minimum value for AHT20

    mcpMaxIndex = np.argmax(mcpTemp) # Index of the maximum value for MCP9808
    mcpMinIndex = np.argmin(mcpTemp) # Index of the minimum value for MCP9808

    def normalize(array, min_val, max_val):
        """Normalizes the array to a range of 0 to 1."""
        return (array - min_val) / (max_val - min_val)

    def unnormalize(array, min_val, max_val):
        """Unnormalizes the array to the original range."""
        return array * (max_val - min_val) + min_val

    offset = np.mean(ahtTemp[0:119]) # Offset for AHT20

    aht_Norm = normalize(ahtTemp, ahtTemp[ahtMinIndex], ahtTemp[ahtMaxIndex]) # AHT20 data (normalized)
    aht_offset_Norm = normalize(offset, ahtTemp[ahtMinIndex], ahtTemp[ahtMaxIndex]) # Offset for AHT20 (normalized)
    aht_time_Norm = normalize(time[ahtMaxIndex:299], time[ahtMaxIndex], time[299]) # Time for AHT20 (normalized)
    aht_Temptau = unnormalize(aht_offset_Norm + 1/np.e, ahtTemp[ahtMinIndex], ahtTemp[ahtMaxIndex]) # Unnormalize the 1/e point for AHT20

    mcp_Norm = normalize(mcpTemp, mcpTemp[mcpMinIndex], mcpTemp[mcpMaxIndex]) # MCP9808 data (normalized)
    mcp_offset_Norm = normalize(offset, mcpTemp[mcpMinIndex], mcpTemp[mcpMaxIndex]) # Offset for MCP9808 (normalized)
    mcp_time_Norm = normalize(time[mcpMaxIndex:299], time[mcpMaxIndex], time[299]) # Time for MCP9808 (normalized)
    mcp_Temptau = unnormalize(mcp_offset_Norm + 1/np.e, mcpTemp[mcpMinIndex], mcpTemp[mcpMaxIndex]) # Unnormalize the 1/e point for MCP9808

    def find_closest_index(array, array_Start, array_End, value):
        """Finds the Closest index of a value in an array between two indices.

        Args:
            array (array): Data input
            array_Start (Integer): Starting index of the array
            array_End (Intger): Ending index of the array
            value (Float): Value to find the closest index for

        Returns:
            closest_index (Integer): Index of the closest value
        """
        closest_index = -1
        min_difference = float("inf")
        for i in range(array_Start, array_End):
            difference = abs(array[i] - value)
            if difference < min_difference:
                min_difference = difference
                closest_index = i
        return closest_index

    aht_ClosestIndex = find_closest_index(ahtTemp, ahtMaxIndex, 299, aht_Temptau) #Index of the closest value to the 1/e point for AHT20
    aht_Tau = normalize(time[aht_ClosestIndex], time[ahtMaxIndex], time[299]) # Tau value for AHT20 (normalized)

    mcp_ClosestIndex = find_closest_index(mcpTemp, mcpMaxIndex, 299, mcp_Temptau) #Index of the closest value to the 1/e point for MCP9808
    mcp_Tau = normalize(time[mcp_ClosestIndex], time[mcpMaxIndex], time[299]) # Tau value for MCP9808 (normalized)

    fig3, ax3 = plt.subplots()  # Create the third figure and axes
    ax3.plot(aht_time_Norm, aht_Norm[ahtMaxIndex:299], label='AHT20', color='red')
    ax3.plot(mcp_time_Norm, mcp_Norm[mcpMaxIndex:299], label='MCP9808', color='blue')

    ax3.axhline(aht_offset_Norm, color='green', linestyle='--', label='Offset')
    ax3.axhline(aht_offset_Norm+(1/np.e), color='red', linestyle='--')
    ax3.axvline(aht_Tau, color='red', linestyle='--')
    ax3.plot(aht_Tau, aht_offset_Norm+(1/np.e), marker='o', color='red', label='AHT20 1/e point')

    ax3.axhline(mcp_offset_Norm, color='green', linestyle='--')
    ax3.axhline(mcp_offset_Norm+(1/np.e), color='blue', linestyle='--')
    ax3.axvline(mcp_Tau, color='blue', linestyle='--')
    ax3.plot(mcp_Tau, mcp_offset_Norm+(1/np.e), marker='o', color='blue', label='MCP9808 1/e point')

    ax3.set_ylim(0,1)
    ax3.set_xlim(0,1)
    ax3.set_xlabel('Normalized Time')
    ax3.set_ylabel('Normalized Temperature')
    ax3.grid(True)
    ax3.set_title('Response Time of MCP9808 and AHT20', fontweight='bold')
    ax3.legend()

    fig4, ax4 = plt.subplots()  # Create the fourth figure and axes
    ax4.plot(time, ahtTemp, label='AHT20', color='red')
    ax4.plot(time, mcpTemp, label='MCP9808', color='blue')
    ax4.axhline(aht_Temptau, color='red', linestyle='--', label='AHT Temp Tau')
    ax4.axhline(mcp_Temptau, color='blue', linestyle='--', label='MCP Temp Tau')

    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Temperature (°C)')
    ax4.grid(True)
    ax4.set_title('MCP9808 and AHT20 Temperatures and Decay Times', fontweight='bold')
    ax4.legend()

    plt.show()


else:
   print("No file selected.")