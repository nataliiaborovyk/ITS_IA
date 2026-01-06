import numpy as np

lanci = np.random.randint(0, 2, size=100)   # questo è frequentista: guardo i dati

media = np.mean(lanci)
print(media)

for n in [10, 100, 1000, 10000]:
    lanci = np.random.randint(0, 2, size=n)
    print(n, np.mean(lanci))
