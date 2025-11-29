














import matplotlib.pyplot as plt
import numpy as np

Z =np.random.uniform(0, 1, 4)
fig, ax = plt.subplots() # Oggetti di tipo figura e asse per il grafico 
ax.pie(Z)
plt.savefig('../../visual/lab/matplotlib_pie.png')
plt.show()






Z =np.random.uniform(0, 1, (100, 3))
print(Z[:,:1])
fig, ax = plt.subplots() # Oggetti di tipo figura e asse per il grafico 
# fig, ax1 = plt.subplots() # Oggetti di tipo figura e asse per il grafico 
# fig, ax2 = plt.subplots() # Oggetti di tipo figura e asse per il grafico 
# fig, ax3 = plt.subplots() # Oggetti di tipo figura e asse per il grafico 
# ax.boxplot(Z)
# ax1.boxplot(Z[:,:1])
# ax2.boxplot(Z[:,1:2])
# ax3.boxplot(Z[:,2:3])
# plt.show()
ax.boxplot(Z)
plt.savefig('../../visual/lab/matplotlib_boxplot.png')
plt.show()











