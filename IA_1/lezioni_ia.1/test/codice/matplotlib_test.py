import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)
fig, ax = plt.subplots() # Oggetti di tipo figura e asse per il grafico 
ax.plot(x, y)

plt.savefig('../visual/matplotlib_line.png')
print("matplotlib_line salvata in ../visual")
plt.show()