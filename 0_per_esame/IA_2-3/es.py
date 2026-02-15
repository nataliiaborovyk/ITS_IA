import numpy as np


valori = np.array([1.1, 3.1, 4.2, 4.6, 5.0, 5.2, 5.3, 6.5, 8.4, 9.6])
print(len(valori))

media = valori.mean()
print(media)

var = valori.std(ddof=1)**2 # calcola deviazione standart campionaria
print(var)

std = np.sqrt(sum(valori - valori.mean()) / (len(valori)-1) )
print(std)