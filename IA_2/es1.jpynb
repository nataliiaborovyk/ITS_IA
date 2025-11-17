import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

S_dado = {1, 2, 3, 4, 5, 6}
print(f"Spazio campionario S = {S_dado}")
print(f"Cardinalità |S| = {len(S_dado)}")

n_lanci = 10
lanci:list = np.random.randint(1, 7, size=n_lanci)

frequenze = Counter(lanci) # conta quante volte appare ogni faccia del dado.
print(f"\nFrequenze assolute dopo {n_lanci} lanci:")
for faccia in sorted(frequenze.keys()):
    freq_rel = frequenze[faccia] / n_lanci
    print(f"Faccia {faccia}: {frequenze[faccia]} volte (frequenza relativa: {freq_rel:.3f})")

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
