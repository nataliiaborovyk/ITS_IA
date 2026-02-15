import math

# 13
n, k, p = 20, 18, 0.98
prob = math.comb(n, k) * (p**k) * ((1-p)**(n-k))
print(prob)

# 14
n, p = 15, 0.97
k = 14
prob_14 = math.comb(n, k) * (p**k) * ((1-p)**(n-k))
k = 15
prob_15 = math.comb(n, k) * (p**k) * ((1-p)**(n-k))

prob_tot = prob_14 + prob_15
print(prob_tot)

# 15

lam = 6
k=4
p_eq4 = (lam**k) * math.exp(-lam) / math.factorial(k)
p_le2 = sum((lam**k) * math.exp(-lam) / math.factorial(k) for k in range(0, 3))
k=0
p_eq0 = (lam**k) * math.exp(-lam) / math.factorial(k)
p_ge1 = 1 - p_eq0
print(p_eq4, p_le2, p_ge1)

#16 

lam = 4
p_lemax_2 = sum((lam**k) * math.exp(-lam) / math.factorial(k) for k in range(0, 3))
