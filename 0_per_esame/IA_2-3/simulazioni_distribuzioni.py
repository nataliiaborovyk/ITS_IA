import numpy as np

# ============================================================
# ESERCIZIO:
# Un paziente ha una probabilità del 30% di rispondere a un trattamento.
# Simula 1000 pazienti e calcola:
# - quante risposte positive si ottengono
# - la frequenza empirica (vista dai dati, non teorica) di successo
# ============================================================

# Binomiale(n=1, p) = Bernoulli(p)

# np.random.binomial(n, p, size)  -> Simula esperimenti casuali
# Significa:
#     n  numero_prove → quante prove per ogni esperimento
#     p → probabilità di successo
#     size → quanti esperimenti indipendenti vuoi simulare

n = 100000
p = 0.3

risposte = np.random.binomial(1, p, n)
successi = risposte.sum()

frequenza = successi / n   # - la frequenza empirica di successo

print(frequenza)



# ============================================================
# ESERCIZIO:
# In un reparto un tampone rapido intercetta il virus nel 80% dei casi.
# Se si eseguono 20 tamponi su pazienti infetti, qual è la probabilità di
# ottenere esattamente 15 risultati positivi?
# Inoltre simula 10.000 prove e confronta la probabilità teorica con quella simulata.
# ============================================================

from scipy.stats import binom

p = 0.8
n = 20

k = 15

res_teor = binom.pmf(k, n, p)
print(res_teor)

simulazioni = 10000  # ripeto 10000 volte esperimento che ha 20 prove dentro esperimento
esperimenti = np.random.binomial(n, p, simulazioni )
prob_emp = np.mean(esperimenti==15)
print(prob_emp)