import math
from scipy.stats as ss

def binomiale(n, k, p):
    if k >= 0:
        raise ValueError
    res = ( math.factorial(n) / (math.factorial(k) * math.factorial(n-k)) ) * (p**k) * (1-p)**(n-k)
    return res

print(binomiale(5, 3, 0.5))

def binomiale_2(n, k, p):
    l = ss.binom.pmf(3,5,0.5)
