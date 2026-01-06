import numpy as np
import matplotlib.pyplot as plt

numero_lanci = 10000

risultati_dati1 = np.random.randint(1,7,size=numero_lanci)
risultati_dati2 = np.random.randint(1,7,size=numero_lanci)
risultati_dati3 = np.random.randint(1,7,size=numero_lanci)

somma_risultati = risultati_dati1 + risultati_dati2 + risultati_dati3

# 2. Contiamo le frequenze di ogni faccia
# unique restituisce i valori unici (1,2,3,4,5,6) e quante volte appaiono, con return_counts=True ci dice appunto quante volte è uscito ogni risultato
facce,frequenze = np.unique(somma_risultati, return_counts=True)
# values, counts = np.unique(a, return_counts=True)


plt.figure()
plt.bar
(facce,frequenze)

plt.xlabel('Risultati del lancio del dado')
plt.ylabel('Quante volte sono usciti')
plt.show
() 