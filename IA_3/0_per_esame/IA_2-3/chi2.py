import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import chi2

# gradi di libertà
nu = 3

# valori su cui valutare la pdf
valori_x = np.linspace(0, 15, 400)

# pdf della chi-quadro
pdf = chi2.pdf(valori_x, nu)

plt.figure(figsize=(10,6))
plt.plot(valori_x, pdf)

plt.title('Distribuzione Chi-quadro')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid()
plt.show()
