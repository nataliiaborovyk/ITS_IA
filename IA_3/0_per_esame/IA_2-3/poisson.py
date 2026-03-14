from scipy.stats import poisson


# esattamente 3 chiamate
lambda_call = 5

prob_3 = poisson.pmf(3, lambda_call)
# poisson.pmf(k, lambda) calcola (P (X = k) ).
print(prob_3)

# almeno 4 chiamate
prob_alm_4 = 1 - poisson.cdf(3, lambda_call)
# poisson.cdf(k, lambda) calcola (P (X ≤ k) ).
print(prob_alm_4)

import math

lamb = 5
k = 3

prob = lamb**3 * math.exp(-lamb) / math.factorial(k)
print(prob)


# PMF	poisson.pmf(k, mu)
# CDF	poisson.cdf(k, mu)
# PPF	poisson.ppf(q, mu)
# RVS	poisson.rvs(mu, size=n)

# Parametri:
#     mu = valore medio λ