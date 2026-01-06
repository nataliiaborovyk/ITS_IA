














import matplotlib.pyplot as plt
import numpy as np

X = np.random.uniform(0, 1, 100)
Y = np.random.uniform(0, 1, 100)
fig, ax = plt.subplots() # Oggetti di tipo figura e asse per il grafico 
ax.scatter(X, Y)
plt.savefig('../../visual/lab/matplotlib_scatter.png')
plt.show()





X = np.arange(10)
Y = np.random.uniform(0, 10, 10)
fig, ax = plt.subplots() # Oggetti di tipo figura e asse per il grafico 
ax.bar(X, Y)
plt.savefig('../../visual/lab/matplotlib_bar.png')
plt.show()











