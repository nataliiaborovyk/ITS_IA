import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import expon

# parametro lambda
lambda_ = 0.5

# per esponenziale i valori partono da 0
valori_X = np.linspace(0, 10, 200)

# pdf teorica
pdf = expon.pdf(valori_X, scale=1/lambda_)
# scale = 1 / λ ,  loc = 0 di default

pdf_exp = lambda_ * np.exp(-lambda_ * valori_X)


cdf = expon.cdf(valori_X, scale=1/lambda_)

cdf_exp = 1 - np.exp(-lambda_ * valori_X)


ppf = expon.ppf(0.9, scale=1/lambda_)

plt.figure(figsize=(10,6))
plt.subplot(1,2,1)
plt.plot(valori_X, pdf)

plt.title('Distribuzione Esponenziale (lambda = 0.5)')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid()

plt.subplot(1,2,2)
plt.plot(valori_X, cdf)

plt.title('Distribuzione Esponenziale (lambda = 0.5)')
plt.xlabel('x')
plt.ylabel('F(x)')
plt.grid()
plt.show()



# PDF	expon.pdf(x, scale=1/lambda_)
# CDF	expon.cdf(x, scale=1/lambda_)
# PPF	expon.ppf(p, scale=1/lambda_)
# RVS	expon.rvs(scale=1/lambda_, size=n)

#  Parametri:
#     λ = tasso
#     scale = 1 / λ
#     loc = 0 (default, quasi mai lo tocchi)