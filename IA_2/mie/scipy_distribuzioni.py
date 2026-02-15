

# Bernoulli
from scipy.stats import bernoulli

bernoulli.pmf(1, p=0.5)
bernoulli.rvs(p=0.5, size=10)


# Binomiale
from scipy.stats import binom

binom.pmf(k=3, n=10, p=0.3)
binom.cdf(3, n=10, p=0.3)


# Poisson
from scipy.stats import poisson

poisson.pmf(2, mu=3)
poisson.cdf(2, mu=3)

# (mu = λ)

# Esponenziale
from scipy.stats import expon
x=1
λ=4
expon.pdf(x, scale=1/λ)
expon.cdf(x, scale=1/λ)


# Uniforme continua
from scipy.stats import uniform
a=3
b=5
uniform.pdf(x, loc=a, scale=b-a)
