import numpy as np
import matplotlib.pyplot as plt

lanci_dado = np.random.randint(1, 7, size=6000)


valori, conteggi = np.unique(lanci_dado, return_counts=True)  
# valori    = [x1, x2, ...]  -> quali valori sono usciti senza ripetizioni
# conteggi = [y1, y2, ...]  ->  quante volte è uscito ciascun valore 

# frequenza relativa = (numero di volte che succede) / (numero totale di prove) ->  “che frazione del totale”
y = conteggi / len(lanci_dado)
print(y)



plt.hist(lanci_dado, bins=6)
plt.show()
