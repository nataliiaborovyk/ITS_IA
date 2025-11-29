import os
import numpy as np
import matplotlib.pyplot as plt

# Dati
x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

# Figura e asse
fig, ax = plt.subplots()
ax.plot(x, y)

# Percorso corretto, indipendente da dove lanci lo script
base_dir = os.path.dirname(__file__)           # cartella dove si trova questo file .py
save_path = os.path.join(base_dir, '../visual/matplotlib_line.png')

os.makedirs(os.path.dirname(save_path), exist_ok=True)   # Crea la cartella visual se non esiste

plt.savefig(save_path)
print(f"matplotlib_line salvata in {save_path}")
plt.show()
