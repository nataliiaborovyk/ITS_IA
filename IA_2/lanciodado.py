#!/usr/bin/env python
# coding: utf-8

# # Definizione dello spazio campionario per un dado

# In[21]:


import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


# In[22]:


S_dado = {1, 2, 3, 4, 5, 6}
print(f"Spazio campionario S = {S_dado}")
print(f"Cardinalità |S| = {len(S_dado)}")


# # Simulazione di 1000 lanci

# In[38]:


n_lanci = 5000

lanci = np.random.randint(1, 7, size=n_lanci)


# # Conteggio frequenze

# In[39]:


frequenze = Counter(lanci)
print(f"\nFrequenze assolute dopo {n_lanci} lanci:")
for faccia in sorted(frequenze.keys()):
    freq_rel = frequenze[faccia] / n_lanci
    print(f"  Faccia {faccia}: {frequenze[faccia]} volte (frequenza relativa: {freq_rel:.3f})")


# In[40]:


# Visualizzazione delle frequenze\n",
plt.figure(figsize=(10, 6))
facce = sorted(frequenze.keys())
conteggi = [frequenze[f] for f in facce]

plt.bar(facce, conteggi, color='steelblue', alpha=0.7, edgecolor='black')
plt.axhline(y=n_lanci/6, color='red', linestyle='--', label='Valore atteso (1/6)')
plt.xlabel('Faccia del Dado', fontsize=12)
plt.ylabel('Frequenza Assoluta', fontsize=12)
plt.title(f'Distribuzione di {n_lanci} Lanci di un Dado', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.show()

print("\n💡 Osservazione: All'aumentare del numero di lanci, le frequenze relative")
print("   tendono a 1/6 ≈ 0.167 per ogni faccia (Legge dei Grandi Numeri)")


# In[ ]:




