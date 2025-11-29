













import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)
fig, ax = plt.subplots() # Oggetti di tipo figura e asse per il grafico 
ax.plot(x, y)
plt.savefig('../../visual/lab/matplotlib_sine_line.png')
plt.show()






x = np.random.randn(10000) # 10000 punti distribuiti secondo una gaussiana (standard normal distribution)
                           # centrata sullo zero e con varianza uguale a 1. 
                           # Es. -0.455, 0.947, -1.123, ..., 1.675)
plt.hist(x, 100)           # numero di punti raggruppati in 100 intervalli (bins) 
plt.title(r'Normal distribution with $\mu=0, \sigma=1$')
plt.savefig('../../visual/lab/matplotlib_histogram.png')
plt.show()











