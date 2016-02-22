import numpy as np
import matplotlib.pyplot as plt

powercurve = np.loadtxt('V80_powercurve.txt')
les = np.loadtxt('V80_power_LES.txt', skiprows = 1)

plt.plot(powercurve[:,0],powercurve[:,1]) 
plt.plot(les[:,0],les[:,1]/1000.,'dk') 

plt.show()



