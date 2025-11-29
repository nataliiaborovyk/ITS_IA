import random
from collections import Counter
lista = []
diz = {}
for i in range(100):
    x = random.randint(1, 6)
    y = random.randint(1, 6)
    z = x + y
    lista.append(z)
    if z in diz:
        diz[z] += 1
    else:
        diz[z] = 1
max_v = 0
max_k = None
for k, v in diz.items():
    if v > max_v:
        max_v = v
        max_k = k
c = Counter(lista)
m = c.most_common()

print(lista)
print(len(lista))
print(lista.count(7))
print(m)
print(diz)
print(f"Valore {max_k}, è uscito {max_v} volte")