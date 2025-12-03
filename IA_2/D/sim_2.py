import math
from scipy.stats import binom

def binomiale(n, k, p):
    if k >= 0:
        raise ValueError
    res = ( math.factorial(n) / (math.factorial(k) * math.factorial(n-k)) ) * (p**k) * (1-p)**(n-k)
    return res

print(binomiale(5, 3, 0.5))

def binomiale_2(k, n, p):
    l = binom.pmf(k,n,p)
    return l

    
print(binomiale_2(3,5,0.5))
