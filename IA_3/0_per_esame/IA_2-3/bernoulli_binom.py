

import matplotlib.pyplot as plt
from scipy.stats import bernoulli, binom
import numpy as np


#bernoulli
p = 0.3  # prob successo

x_bern = [0,1] # variabile aleatoria

y_bern = bernoulli.pmf(x_bern, p)

plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.stem(x_bern, y_bern)   # grafico a steli
plt.xticks([0,1])    # mostra tutte le etichette: 0, 1
plt.xlabel('x')
plt.ylabel('P(X=x)')
plt.title('Bernouli p=0.3')
plt.ylim(0,1)   # Imposta i limiti dell’asse y

#binomiale
n = 10
x_binom = np.arange(0, n+1)   #crea una lista di numeri da 0 a n (incluso).
# posso scrivere anche x_binom = range(0, n+1)

y_binom = binom.pmf(x_binom, n, p)  # calcola distribuzione binomiale completa
# binom.pmf(k, n, p) - calcola la probabilita teorica

plt.subplot(1,2,2)
plt.stem(x_binom, y_binom)
plt.xticks(range(0, n+1))
plt.xlabel('Numero sucessi')
plt.ylabel('P(X=x)')
plt.title('Binomiale')
plt.ylim(0,max(y_binom)+0.05)
plt.tight_layout()   #  Sistema automaticamente spazi e margini
plt.show()
 

# es2

# bern
p = 0.5
x_bern = [0,1]
y_bern = bernoulli.pmf(x_bern, p)

plt.figure(figsize=(10,4))
plt.subplot(1,2,1)
plt.stem(x_bern, y_bern)
plt.xticks([0,1])
plt.xlabel('x')
plt.ylabel('P(x)')
plt.title('bernoulli')
plt.ylim(0,1)

# bin
n=10
x_bin = np.arange(0, n+1)
y_bin = binom.pmf(x_bin, n, p)

plt.subplot(1,2,2)
plt.stem(x_bin, y_bin)
plt.xticks(range(0,n+1))
plt.xlabel('x')
plt.ylabel('P(x)')
plt.title('binomiale')
plt.ylim(0,max(y_bin)+0.05)
plt.tight_layout()
plt.show()


# PMF	binom.pmf(k, n, p)
# CDF	binom.cdf(k, n, p)
# PPF	binom.ppf(q, n, p)
# RVS	binom.rvs(n, p, size=m)

# Parametri:
#     n = numero prove
#     p = probabilità di successo
#     k = numero successi