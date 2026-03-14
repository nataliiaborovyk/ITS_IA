# lancio un dado

sigma = [1,2,3,4,5,6]
scelta = [5]

p=len(scelta)/len(sigma)
print(p)

import random

# lancio moneta
sigma2 = ['testa', 'croce']
lancio1 = random.choice(sigma2)
print(lancio1)

lancio2 = random.randint(0,1)
if lancio1==1:
    print('testa')
else:
    print('croce')

#10 lanci moneta
moneta = ['testa', 'croce']
esito=[]
for _ in range(10):
    lancio = random.choice(moneta)
    esito.append(lancio)
print(esito)

# lancio di 2 dadi
n = 100
esito2 = []

for _ in range(n):
    lancio_d1 = random.randint(1,6)
    lancio_d2 = random.randint(1,6)
    somma = lancio_d1 + lancio_d2
    esito2.append(somma)
print(esito2)

print(esito2.count(7))

