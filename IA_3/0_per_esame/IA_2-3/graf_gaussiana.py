import numpy as np
import numpy as np                      # Per creare array di numeri
import matplotlib.pyplot as plt         # Per fare i grafici
from scipy.stats import norm            # Per la normale (gaussiana)

mu = 100                                # Media
varianza = 10                           # Varianza
sigma = np.sqrt(varianza)               # Deviazione standard (radice della varianza)

x = np.linspace(mu - 4*sigma, mu + 4*sigma, 1000)  # Asse x (intervallo ampio)
y = norm.pdf(x, loc=mu, scale=sigma)    # Densità della N(mu, sigma^2)

plt.figure()                            # Crea una nuova figura
plt.plot(x, y)                          # Disegna la curva
plt.title("Gaussiana: mu=100, varianza=10")  # Titolo
plt.xlabel("x")                         # Etichetta asse x
plt.ylabel("f(x)")                      # Etichetta asse y
plt.grid(True)                          # Griglia
plt.show()   

