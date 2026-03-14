import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
import math

mu = 0
sigma = 3

valori_X = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)

pdf = norm.pdf(valori_X, mu, sigma)

pdf_normal = 1/(np.sqrt(2*np.pi)*sigma) * np.exp(-(valori_X-mu)**2/(2*sigma**2))

cdf = norm.cdf(valori_X, loc=mu, scale=sigma)


ppf = norm.ppf(0.95, mu, sigma)
ppf = norm.ppf(0.95)



plt.figure(figsize=(10,6))
plt.subplot(1,2,1)
plt.plot(valori_X, pdf)

plt.title('Gausiana')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid()

plt.subplot(1,2,2)
plt.plot(valori_X, cdf)

plt.title('Gausiana')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid()
plt.show()


# PDF	norm.pdf(x, loc=mu, scale=sigma)
# CDF	norm.cdf(x, loc=mu, scale=sigma)
# PPF	norm.ppf(p, loc=mu, scale=sigma)
# RVS	norm.rvs(loc=mu, scale=sigma, size=n)