import matplotlib.pyplot as plt
from scipy.stats import binom
from scipy.special import comb
import numpy as np
from math import comb as comb2

p = 1/6
k = 0
n = 7

result = binom.pmf(k, n, p)
print(result)

result2 = 35*(1/6)**3*(5/6)**4
print(result2)

result3 = comb(n, k, exact=True)
# exact=True restituisce risultato come numero intero, non come numero decimale (float)
print(result3)   

result4 = comb2(n, k)
print(result4) 
