# La variabile casuale X assume i valori 0,1,2 con probabilità rispettive p(0)=0.2; p(1)=0.5; p(2)=0.3. Calcola la media E[X] , la varianza Var(X) e la
# deviazione standard (σ ).

import numpy as np

valori = np.array([0,1,2])
prob = np.array([0.2, 0.5, 0.3])
ex = (valori*prob).sum()
ex2 = (valori**2*prob).sum()
var = ex2 - ex**2
std = np.sqrt(var)
print(ex, ex2, std)


# 2 media, mediana
val = np.array([2,3,7,10,12])
print(val.mean())

print(np.median(val))


# 3 moda
from collections import Counter

data = [1,2,2,3,3,3,4]
cnt = Counter(data)
mode = cnt.most_common(1)[0][0]  
# most_common(n) restituisce: una lista di n coppie
# cnt.most_common(1) -> [(3,3)]
# [0]  ->  Prendi il primo elemento della lista:
# [0] di nuovo -> Prendi il primo elemento della tupla:
print(mode)

