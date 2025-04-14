import matplotlib.pyplot as plt
import matplotlib.cbook as cbook

Vin = [3,3.5,3.75,4,4.25,4.5,6,7,8,9]
Vout = [2.731,3.143,3.401,3.7,3.877,3.954,3.955,3.948,3.938,3.926]

plt.plot(Vin,Vout,'b^')
plt.xlabel('V in (V)')
plt.ylabel('V out (V)')
plt.axhline(3.84, 0, 9, label='4% reduction of desired Vout = 4V', color = 'red', linestyle = 'dashed')
plt.legend()
plt.grid()
plt.title('LDO Regulator Dropout Behavior', fontweight='bold')
plt.show()
